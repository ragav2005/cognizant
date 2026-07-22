"""Page Object for Simple Form Demo."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        field = self.wait_for_element(self.MESSAGE_INPUT)
        field.clear()
        field.send_keys(text)

    def click_submit(self):
        self.wait_until_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self):
        """Return the displayed message, retrying an occasionally missed first click."""
        try:
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element(*self.DISPLAYED_MESSAGE).text != ""
            )
        except TimeoutException:
            self.click_submit()
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text

