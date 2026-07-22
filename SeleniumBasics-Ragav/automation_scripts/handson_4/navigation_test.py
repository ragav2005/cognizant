from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
simple_form_link.click()

assert "simple-form-demo" in driver.current_url, "URL does not contain expected substring"
print("Navigated to Simple Form Demo successfully.")

driver.back()


driver.execute_script('window.open("https://www.google.com");')

handles = driver.window_handles
print("Window handles:", handles)

driver.switch_to.window(handles[1])
print("Google tab title:", driver.title)

driver.switch_to.window(handles[0])


screenshot_path = "playground_screenshot.png"
driver.save_screenshot(screenshot_path)
print(f"Screenshot saved to {os.path.abspath(screenshot_path)}")


original_size = driver.get_window_size()
print("Original window size:", original_size)


driver.set_window_size(1280, 800)
print("Adjusted window size to 1280x800")

driver.quit()
