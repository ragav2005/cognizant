"""Shared pytest fixtures and hooks for Hands-On 6."""

import re

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    """The common URL used by every Selenium Playground test."""
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver(request):
    """Create a new Chrome browser for each test and quit it afterward."""
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.maximize_window()
    request.node.driver = browser  # Lets the failure hook access this test's driver.
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot in this folder whenever a test call fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    browser = getattr(item, "driver", None)
    if browser is not None:
        safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.name)
        browser.save_screenshot(f"{safe_name}_failure.png")

