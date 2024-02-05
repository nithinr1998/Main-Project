import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException  # Add this import
from selenium import webdriver

class Logintest(LiveServerTestCase):

    def setUp(self):
        service = Service(r'D:\mca\gecko\geckodriver.exe')
        self.driver = webdriver.Firefox(service=service)
        self.driver.implicitly_wait(10)
        self.live_server_url = "http://127.0.0.1:8000/login"  # Updated URL

    def tearDown(self):
        self.driver.quit()

    def fill_form(self, email='', password=''):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        driver.find_element(By.ID, "email").send_keys(email)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        driver.find_element(By.ID, "password").send_keys(password)

    def test_correct_credentials_and_search(self):
        self.driver.get(self.live_server_url)
        self.fill_form(email="shyam@gmail.com", password="shyam")
        self.driver.find_element(By.ID, "testid").click()
        self.assertIn("customer/", self.driver.current_url)
        print("Test scenario 'View Profile' passed.")
        seltest_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "abc"))
        )
        seltest_element.click()
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Customer")
        )
        print("Test scenario 'View Profile' passed.")
        time.sleep(5)
if __name__ == '__main__':
    LiveServerTestCase.main()
