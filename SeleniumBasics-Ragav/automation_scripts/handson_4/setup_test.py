from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)



driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")
print("Page title:", driver.title)

driver.quit()
