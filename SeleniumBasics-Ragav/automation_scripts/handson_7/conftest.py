"""Shared pytest fixtures for the Hands-On 7 POM test suite."""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.maximize_window()
    yield browser
    browser.quit()

