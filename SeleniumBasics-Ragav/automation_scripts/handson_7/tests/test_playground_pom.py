import pytest

from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage
from pages.simple_form_page import SimpleFormPage


@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo")
    page.enter_message(message)
    page.click_submit()
    assert page.get_displayed_message() == message


def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo")
    page.check_option(0)
    assert page.is_option_checked(0)
    page.uncheck_option(0)
    assert not page.is_option_checked(0)


def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo")
    assert page.select_day("Wednesday") == "Wednesday"


def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo")
    page.fill_form("Ragav", "ragav@example.com", "9876543210", "Chennai")
    page.submit_form()
    assert "thank" in page.get_success_message().lower()
