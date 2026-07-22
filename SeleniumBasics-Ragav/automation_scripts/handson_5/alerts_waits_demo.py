import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"
SUCCESS_BUTTONS = (By.XPATH, "//button[contains(translate(normalize-space(.), "
                   "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'success')]")
SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")


def open_bootstrap_alerts(driver):
    driver.get(PLAYGROUND_URL)
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Bootstrap Alerts"))
    ).click()


def visible_success_button(driver):

    buttons = driver.find_elements(*SUCCESS_BUTTONS)
    visible = [button for button in buttons if button.is_displayed() and button.is_enabled()]
    if not visible:
        return False
    return next((button for button in visible if "normal" in button.text.lower()), visible[0])


def click_success_and_wait(driver):
    wait = WebDriverWait(driver, 15)
    button = wait.until(visible_success_button)
    wait.until(EC.element_to_be_clickable(button)).click()
    return wait.until(EC.visibility_of_element_located(SUCCESS_ALERT))


def print_page_diagnostics(driver):

    labels = [button.text.strip() for button in driver.find_elements(By.TAG_NAME, "button")]
    print(f"Current URL: {driver.current_url}")
    print(f"Buttons found: {labels}")


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    try:
        open_bootstrap_alerts(driver)

        print("TASK 36 — EXPLICIT WAIT")
        try:
            alert = click_success_and_wait(driver)
        except TimeoutException:
            print_page_diagnostics(driver)
            raise
        assert "success" in alert.text.lower()
        print(f"✓ Success alert verified: {alert.text}")

        print("TASK 37 — SLEEP VS EXPLICIT WAIT")
        driver.refresh()
        started = time.perf_counter()

        sleep_wait = WebDriverWait(driver, 15)
        sleep_button = sleep_wait.until(visible_success_button)
        sleep_wait.until(EC.element_to_be_clickable(sleep_button)).click()
        sleep_alert = sleep_wait.until(EC.visibility_of_element_located(SUCCESS_ALERT))
        time.sleep(3)
        sleep_duration = time.perf_counter() - started
        # Do not assert here: the autoclosing message may already be fading out.
        # That nondeterminism is exactly why time.sleep() is a bad test strategy.
        sleep_result = "visible" if "success" in sleep_alert.text.lower() else "already fading/hidden"

        driver.refresh()
        started = time.perf_counter()
        alert = click_success_and_wait(driver)
        assert "success" in alert.text.lower()
        explicit_duration = time.perf_counter() - started
        print(f"Fixed sleep: {sleep_duration:.2f}s ({sleep_result})")
        print(f"Explicit wait: {explicit_duration:.2f}s (success alert found)")
        print("Explicit waits finish as soon as their condition is met and are more reliable.")

        print("TASK 38 — CLICKABLE CONDITION")
        driver.refresh()

        clickable_wait = WebDriverWait(driver, 15)
        clickable_button = clickable_wait.until(visible_success_button)
        clickable_wait.until(EC.element_to_be_clickable(clickable_button)).click()
        print("visibility_of_element_located: displayed in the page")
        print("element_to_be_clickable: displayed and enabled before clicking")

        print("TASK 39 — FLUENT WAIT")
        driver.get(PLAYGROUND_URL + "table-sort-search-demo")
        fluent_wait = WebDriverWait(
            driver, timeout=10, poll_frequency=0.5,
            ignored_exceptions=(NoSuchElementException,),
        )
        row = fluent_wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#example tbody tr"))
        )
        print(f"FluentWait found table row: {row.text}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
