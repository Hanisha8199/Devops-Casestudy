import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text

def test_empty_product(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "brand").send_keys("FakeDairy")
    driver.find_element(By.NAME, "description").send_keys("Found chalk powder in the milk packets.")
    driver.find_element(By.NAME, "submit_btn").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Product Name cannot be empty."

def test_short_description(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "product_name").send_keys("Milk")
    driver.find_element(By.NAME, "brand").send_keys("FakeDairy")
    driver.find_element(By.NAME, "description").send_keys("Bad milk.") # Only 9 chars
    driver.find_element(By.NAME, "submit_btn").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Description must be at least 15 characters long to be helpful."

def test_valid_submission(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "product_name").send_keys("Milk")
    driver.find_element(By.NAME, "brand").send_keys("FakeDairy")
    driver.find_element(By.NAME, "description").send_keys("Found chalk powder in the milk packets.")
    driver.find_element(By.NAME, "submit_btn").click()
    time.sleep(2)
    
    assert "/submit" in driver.current_url
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Thank you for your vigilance!" in body_text
    assert "Milk" in body_text