import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-allow-origins=*")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)
    driver.implicitly_wait(5)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass

def click_submit(driver):
    btn = driver.find_element(By.NAME, "submit_btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    driver.execute_script("arguments[0].click();", btn)

def get_alert_text(driver):
    WebDriverWait(driver, 8).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    return text

def test_empty_product(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "brand").send_keys("FakeDairy")
    driver.find_element(By.NAME, "description").send_keys("Found chalk powder in the milk packets.")
    click_submit(driver)
    assert get_alert_text(driver) == "Product Name cannot be empty."

def test_short_description(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "product_name").send_keys("Milk")
    driver.find_element(By.NAME, "brand").send_keys("FakeDairy")
    driver.find_element(By.NAME, "description").send_keys("Bad milk.") # Only 9 chars
    click_submit(driver)
    assert get_alert_text(driver) == "Description must be at least 15 characters long to be helpful."

def test_valid_submission(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "product_name").send_keys("Milk")
    driver.find_element(By.NAME, "brand").send_keys("FakeDairy")
    driver.find_element(By.NAME, "description").send_keys("Found chalk powder in the milk packets.")
    click_submit(driver)
    
    WebDriverWait(driver, 8).until(EC.url_contains("/submit"))
    assert "/submit" in driver.current_url
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Thank you for your vigilance!" in body_text
    assert "Milk" in body_text
