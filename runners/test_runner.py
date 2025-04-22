import os
import time
import csv
from datetime import datetime

import pytest
from pytest_bdd import scenarios, parsers, given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from models.user_data import UserData
from pages.web_tables_page import WebTablesPage

# point to your feature file
scenarios(os.path.join(os.path.dirname(__file__), '../features/web_tables.feature'))

@pytest.fixture
def browser():
    hub_url = os.getenv("SELENIUM_HUB_URL", "http://host.docker.internal:4444/wd/hub")
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.set_capability('record_video', True)
    driver = webdriver.Remote(command_executor=hub_url, options=chrome_opts)
    yield driver
    driver.quit()

@pytest.fixture
def web_tables_page(browser):
    return WebTablesPage(browser)

def pytest_bdd_after_scenario(request, feature, scenario):
    browser = request.getfixturevalue('browser')
    session_id = browser.session_id
    print(f"Video recording saved at: /opt/selenoid/videos/{session_id}.mp4")

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    browser = request.getfixturevalue('browser')
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"error_{scenario.name}_{step.name}_{ts}.png"
    browser.save_screenshot(name)
    print(f"Screenshot saved as: {name}")

def load_user_data_from_csv(file_name, row_index):
    path = os.path.join('testdata', file_name)
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        users = [
            UserData(
                first_name=r['FirstName'],
                last_name=r['LastName'],
                username=r['UserName'],
                password=r['Password'],
                company=r['Company'],
                role=r['Role'],
                email=r['Email'],
                mobile_phone=r['Mobilephone']
            )
            for r in reader
        ]
    return users[row_index]

latest_user = None

@given(parsers.parse('User navigate to "{url}"'))
def user_navigate_to(browser, url):
    browser.get(url)
    time.sleep(1)

@then("User should see the user list table with headers:")
def verify_user_list_table_headers(web_tables_page, datatable):
    assert web_tables_page.is_user_list_table_displayed(), "User list table is not displayed"
    expected = [row['Header'] for row in datatable]
    actual = web_tables_page.get_header_list()
    assert actual == expected, f"Expected headers {expected}, got {actual}"

@when(parsers.parse('User click "{button_text}"'))
def user_click_button(browser, web_tables_page, button_text):
    if button_text.lower() == 'add user':
        web_tables_page.click_add_user()
    else:
        browser.find_element(By.XPATH, f"//button[contains(text(),'{button_text}')]").click()
    time.sleep(1)

@when("User add a user with data:")
def add_user_with_data(web_tables_page, datatable):
    global latest_user
    for row in datatable:
        user = UserData(
            first_name=row['firstName'],
            last_name=row['lastName'],
            username=f"{row['userName']}_{int(time.time())}",
            password=row['password'],
            company=row['customer'],
            role=row['role'],
            email=row['email'],
            mobile_phone=row['cellPhone']
        )
        latest_user = user
        web_tables_page.click_add_user()
        web_tables_page.add_user(user)
        web_tables_page.click_save_button()
        time.sleep(1)

@then(parsers.parse('User should see the user "{username}" in the user list with details:'))
def verify_user_in_list(browser, web_tables_page, username, datatable):
    assert web_tables_page.is_user_present_in_list(username), f"User {username} not found"
    rows = browser.find_elements(By.CSS_SELECTOR, "table.smart-table tbody tr")
    row_elem = next(r for r in rows if username in r.text)
    cells = row_elem.find_elements(By.TAG_NAME, "td")
    expected = datatable[0]
    assert cells[0].text == expected['First Name']
    assert cells[1].text == expected['Last Name']
    assert cells[2].text == username
    assert cells[3].text == expected['Customer']
    assert cells[4].text == expected['Role']
    assert cells[5].text == expected['E-mail']
    assert cells[6].text == expected['Cell Phone']
    time.sleep(1)

@given(parsers.parse('User load user data from CSV file "{file_name}" row {row_index:d}'))
def load_user_data(file_name, row_index):
    global latest_user
    latest_user = load_user_data_from_csv(file_name, row_index)
    time.sleep(1)

@when("User add the latest user")
def add_latest_user(web_tables_page):
    web_tables_page.click_add_user()
    web_tables_page.add_user(latest_user)
    web_tables_page.click_save_button()
    time.sleep(1)

@then("User should see the latest user in the user list")
def verify_latest_user_in_list(web_tables_page):
    assert web_tables_page.is_user_present_in_list(latest_user.username), \
        f"Latest user not found: {latest_user.username}"
    time.sleep(1)
