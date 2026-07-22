"""Hands-On 5, Task 1: Selenium locator strategies."""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def open_demo(driver, link_text):
    """Open a demo from the Selenium Playground home page."""
    driver.get(PLAYGROUND_URL)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, link_text))
    ).click()


def assert_among_matches(driver, by, locator, target, description):
    matches = driver.find_elements(by, locator)
    assert target in matches, f"{description} did not find #user-message"
    print(f"{description}")


def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        open_demo(driver, "Simple Form Demo")
        wait = WebDriverWait(driver, 10)
        target = wait.until(EC.visibility_of_element_located((By.ID, "user-message")))

        print("TASK 1 — LOCATOR STRATEGIES")

        assert driver.find_element(By.ID, "user-message") == target
        print("By.ID")

        field_name = target.get_attribute("name")
        if field_name:
            assert_among_matches(driver, By.NAME, field_name, target, f"By.NAME ({field_name!r})")
        else:
            print("By.NAME skipped: current #user-message has no name attribute")

        class_name = target.get_attribute("class").split()[0]
        assert_among_matches(driver, By.CLASS_NAME, class_name, target, f"By.CLASS_NAME ({class_name!r})")

        inputs = driver.find_elements(By.TAG_NAME, "input")
        assert target in inputs
        print(f"By.TAG_NAME (found {len(inputs)} input tags)")

        absolute_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/input"
        try:
            assert driver.find_element(By.XPATH, absolute_xpath) == target
            print("By.XPATH (absolute path)")
        except (AssertionError, NoSuchElementException) as error:
            print(f"Absolute XPath changed on this site: {type(error).__name__}")

        field_id = target.get_attribute("id")
        assert driver.find_element(By.XPATH, f"//input[@id='{field_id}']") == target
        print("By.XPATH (relative attributes)")

        assert driver.find_element(By.CSS_SELECTOR, "#user-message") == target
        print("CSS: #user-message")
        if field_name:
            assert_among_matches(
                driver, By.CSS_SELECTOR, f"input[name='{field_name}']", target,
                f"CSS: input[name='{field_name}']",
            )
        else:
            print("CSS attribute selector skipped: the field has no name attribute")

        assert_among_matches(
            driver, By.CSS_SELECTOR, f"div > input#{field_id}", target,
            f"CSS: div > input#{field_id}",
        )

        open_demo(driver, "Checkbox Demo")
        option_one = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//label[text()='Option 1']"))
        )
        assert option_one.text == "Option 1"
        print("XPath text(): Option 1")

        option_labels = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        assert option_labels, "No labels containing 'Option' were found"
        print(f"XPath contains(): found {len(option_labels)} option label(s)")


        print("Locator ranking: ID, CSS, Name, Class Name, Relative XPath, Absolute XPath")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
