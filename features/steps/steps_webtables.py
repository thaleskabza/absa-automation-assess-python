import os
import csv
import datetime
import time
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from pages.web_tables_page import WebTablesPage
from models.user_data import UserData

# Configuration
SELENIUM_HUB = os.getenv("SELENIUM_HUB_URL", "http://localhost:4444/wd/hub")
BROWSER = os.getenv("BROWSER_NAME", "chrome").upper()

# Base path for test data
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_BASE_PATH = os.path.join(PROJECT_ROOT, "resources", "testdata")

# Load feature file
scenarios("../web_tables.feature")

# Fixtures
@pytest.fixture
def driver():
    caps = getattr(DesiredCapabilities, BROWSER)
    driver = webdriver.Remote(
        command_executor=SELENIUM_HUB,
        desired_capabilities=caps
    )
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def web_tables(driver):
    return WebTablesPage(driver)

@pytest.fixture
def latest_user():
    """Container for sharing UserData between steps."""
    return {}

# Step Definitions
@given('User navigate to "http://www.way2automation.com/angularjs-protractor/webtables/"')
def navigate_to_page(web_tables):
    web_tables.navigate_to()

@then(parsers.parse('User should see the user list table with headers:\n{headers_table}'))
def verify_headers(web_tables, headers_table):
    """
    Verifies table headers match expected values.
    headers_table is the raw table string from the feature.
    """
    assert web_tables.is_user_list_table_displayed(), "User list table is not displayed!"
    expected = [h.strip() for line in headers_table.split('\n') for h in line.split('|') if h.strip()]
    actual = web_tables.get_header_list()
    assert actual == expected, f"Expected headers {expected}, but got {actual}"
    time.sleep(1)

  
@given(parsers.parse('User clicks "{button_text}" button'))
def click_button(web_tables, driver, button_text):
    """
    Clicks a button by text. Uses specialized logic for 'Add User'.
    """
    if button_text.lower() == "add user":
        web_tables.click_add_user()
        driver.save_screenshot("After_Add1.png")
        time.sleep(1)
    else:
        xpath = f"//button[contains(text(),'{button_text}')]"
        driver.find_element(By.XPATH, xpath).click()
        driver.save_screenshot("After_Add2.png")
        time.sleep(1)

        
@when(parsers.parse('User load user data from CSV file "{file}" row {row:d}'))
def load_user_data(latest_user, file, row):
    """Load user data from CSV into shared container."""
    csv_path = os.path.join(CSV_BASE_PATH, file)
    if not os.path.exists(csv_path):
        pytest.fail(f"CSV file not found at: {csv_path}")
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if row >= len(rows):
                pytest.fail(f"Row {row} not found in CSV (only {len(rows)} rows)")
            data = rows[row]
    except Exception as e:
        pytest.fail(f"Error loading CSV: {e}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_username = f"{data['userName']}_{timestamp}"
    user = UserData(
        first_name=data.get("FirstName",""),
        last_name=data.get("LastName",""),
        username=unique_username,
        password=data.get("Password",""),
        email=data.get("Email",""),
        mobile_phone=data.get("CellPhone",""),
        company=data.get("customer",""),
        role=data.get("Role",""),
    )
    latest_user["data"] = user

@when('User add the latest user')
def add_latest_user(web_tables, latest_user):
    """Adds the loaded user to the table."""
    user = latest_user.get("data")
    if not user:
        pytest.fail("No user data available to add")
    web_tables.add_user(user)

@then('User should see the latest user in the user list')
def verify_latest_user(web_tables, latest_user):
    """Verifies the added user is present in the list."""
    user = latest_user.get("data")
    if not user:
        pytest.fail("No user data available to verify")
    assert web_tables.is_user_present_in_list(user.username), (
        f"User '{user.username}' not found in the table."
    )
