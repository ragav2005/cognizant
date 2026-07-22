"""Page Object for Input Form Submit."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InputFormPage(BasePage):
    # The Playground has used several incompatible field IDs/names. These
    # class-level locators intentionally target the form structure instead.
    # This demo's inputs are not wrapped in a semantic <form> on the current
    # site, so select its visible data-entry controls directly.
    FORM_INPUTS = (By.CSS_SELECTOR, "input:not([type='hidden']):not([type='submit']):not([type='button'])")
    REQUIRED_INPUTS = (By.CSS_SELECTOR, "input[required]")
    REQUIRED_SELECTS = (By.CSS_SELECTOR, "select")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(normalize-space(text()), 'Thanks for contacting us')]")

    def _fill(self, field, value):
        field.clear()
        field.send_keys(value)

    def fill_form(self, name, email, phone, address):
        self.wait_for_element(self.FORM_INPUTS)
        fields = [field for field in self.driver.find_elements(*self.FORM_INPUTS)
                  if field.is_displayed() and field.is_enabled()]
        if len(fields) < 4:
            raise RuntimeError("Input Form Submit page did not expose four visible form fields")

        # The first fields are Name, Email, Password/Phone, and Company. Fill
        # them with the assignment data, then give later mandatory controls
        # valid defaults (Website, City, Address, State, Zip, and Country).
        for field, value in zip(fields[:4], (name, email, phone, address)):
            self._fill(field, value)
        for field in fields[4:]:
            if not field.get_attribute("value"):
                input_type = field.get_attribute("type").lower()
                if input_type == "url":
                    field.send_keys("https://example.com")
                elif input_type in ("number", "tel"):
                    field.send_keys("600001")
                else:
                    field.send_keys("Test Value")
        for element in self.driver.find_elements(*self.REQUIRED_SELECTS):
            if element.is_displayed():
                select = Select(element)
                # The placeholder's value differs by site release, so always
                # choose a valid country rather than checking that value.
                select.select_by_visible_text("United States")

    def submit_form(self):
        self.wait_until_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
