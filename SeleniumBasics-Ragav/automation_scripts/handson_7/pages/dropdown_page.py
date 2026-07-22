"""Page Object for Select Dropdown List."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DropdownPage(BasePage):
    DAY_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name):
        dropdown = Select(self.wait_until_clickable(self.DAY_DROPDOWN))
        dropdown.select_by_visible_text(day_name)
        return dropdown.first_selected_option.text

