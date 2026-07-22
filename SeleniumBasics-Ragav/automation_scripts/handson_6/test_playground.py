import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

WAIT_SECONDS = 15


def wait_for(driver):
    return WebDriverWait(driver, WAIT_SECONDS)


@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):

    driver.get(base_url + "simple-form-demo")
    wait = wait_for(driver)

    field = wait.until(EC.visibility_of_element_located((By.ID, "user-message")))
    field.send_keys(message)
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "showInput")))
    submit_button.click()


    try:
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "message"), message)
        )
    except TimeoutException:
        wait.until(EC.element_to_be_clickable((By.ID, "showInput"))).click()

    wait.until(EC.text_to_be_present_in_element((By.ID, "message"), message))
    displayed_message = driver.find_element(By.ID, "message")
    assert displayed_message.text == message


def test_checkbox_demo(driver, base_url):
    """Select and deselect the first checkbox."""
    driver.get(base_url + "checkbox-demo")
    wait = wait_for(driver)

    checkbox = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//label[normalize-space()='Option 1']/preceding::input[@type='checkbox'][1]",
    )))

    checkbox.click()
    assert checkbox.is_selected(), "Checkbox should be selected after the first click"
    checkbox.click()
    assert not checkbox.is_selected(), "Checkbox should be deselected after the second click"


def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo")
    wait = wait_for(driver)
    day_dropdown = Select(
        wait.until(EC.element_to_be_clickable((By.ID, "select-demo")))
    )
    day_dropdown.select_by_visible_text("Wednesday")

    assert day_dropdown.first_selected_option.text == "Wednesday"
