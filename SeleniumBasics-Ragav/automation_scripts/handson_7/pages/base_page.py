"""Base class containing browser actions shared by all Page Objects."""

from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def navigate_to(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def wait_for_element(self, locator, timeout=15):
        """Return the first visible match (the site may render hidden duplicates)."""
        return WebDriverWait(self.driver, timeout).until(
            lambda driver: next(
                (element for element in driver.find_elements(*locator)
                 if element.is_displayed()),
                False,
            )
        )

    def wait_until_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            lambda driver: next(
                (element for element in driver.find_elements(*locator)
                 if element.is_displayed() and element.is_enabled()),
                False,
            )
        )
