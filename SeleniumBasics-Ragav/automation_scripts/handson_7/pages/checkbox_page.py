"""Page Object for Checkbox Demo."""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckboxPage(BasePage):
    # Option 1 is the first labelled checkbox in the current Playground markup.
    OPTION_BY_INDEX = (By.XPATH, "(//label[contains(normalize-space(), 'Option')]/preceding::input[@type='checkbox'][1])[%s]")

    def _option(self, index):
        locator = (self.OPTION_BY_INDEX[0], self.OPTION_BY_INDEX[1] % (index + 1))
        return self.wait_until_clickable(locator)

    def check_option(self, index):
        option = self._option(index)
        if not option.is_selected():
            option.click()

    def uncheck_option(self, index):
        option = self._option(index)
        if option.is_selected():
            option.click()

    def is_option_checked(self, index):
        return self._option(index).is_selected()

