import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from models.user_data import UserData


class WebTablesPage(BasePage):
    URL = "http://www.way2automation.com/angularjs-protractor/webtables/"

    locators = {
        "table": (
            By.CSS_SELECTOR,
            'table.smart-table.table-striped[table-title="Smart Table example"]'
        ),
        "add_user": (
            By.XPATH,
            "//button[contains(.,' Add User')]"
        ),
        "firstName": (
            By.NAME,
            "FirstName"
        ),
        "lastName": (
            By.NAME,
            "LastName"
        ),
        "userName": (
            By.NAME,
            "UserName"
        ),
        "password": (
            By.NAME,
            "Password"
        ),
        "company_aaa": (
            By.XPATH,
            "//label[contains(text(),'Company AAA')]/input"
        ),
        "company_bbb": (
            By.XPATH,
            "//label[contains(text(),'Company BBB')]/input"
        ),
        "role": (
            By.NAME,
            "RoleId"
        ),
        "email": (
            By.NAME,
            "Email"
        ),
        "cellPhone": (
            By.NAME,
            "Mobilephone"
        ),
        "save": (
            By.XPATH,
            "//button[contains(@class,'btn-success') and normalize-space(text())='Save']"
        ),
        "close_button": (
            By.XPATH,
            "//button[contains(@class,'btn-danger') and normalize-space(text())='Close']"
        ),
    }

    def navigate_to(self):
        self.driver.get(self.URL)
        time.sleep(1)

    def is_user_list_table_displayed(self) -> bool:
        return self.driver.find_element(*self.locators["table"]).is_displayed()

    def get_header_list(self):
        header_elems = self.driver.find_elements(
            By.CSS_SELECTOR,
            "tr.smart-table-header-row th span.header-content"
        )
        return [h.text.strip() for h in header_elems if h.text.strip()]

    def click_add_user(self):
        self.driver.find_element(*self.locators["add_user"]).click()
        time.sleep(1)

    def add_user(self, user: UserData):
        time.sleep(1)
        self.driver.find_element(*self.locators["firstName"]).send_keys(
            user.first_name
        )
        self.driver.find_element(*self.locators["lastName"]).send_keys(
            user.last_name
        )
        self.driver.find_element(*self.locators["userName"]).send_keys(
            user.username
        )
        self.driver.find_element(*self.locators["cellPhone"]).send_keys(
            user.mobile_phone
        )

        if user.password:
            self.driver.find_element(*self.locators["password"]).send_keys(
                user.password
            )
        if user.email:
            self.driver.find_element(*self.locators["email"]).send_keys(
                user.email
            )

        # select customer radio
        cust_locator = (
            By.XPATH,
            f"//label[contains(normalize-space(),'{user.company}')]/input"
        )
        self.driver.find_element(*cust_locator).click()

        # select role
        Select(
            self.driver.find_element(*self.locators["role"])
        ).select_by_visible_text(user.role)

        # click save
        self.driver.find_element(*self.locators["save"]).click()
        time.sleep(1)

    def is_user_present_in_list(self, username: str) -> bool:
        rows = self.driver.find_elements(
            By.CSS_SELECTOR,
            "table.smart-table.table-striped tbody tr"
        )
        return any(username in row.text for row in rows)
