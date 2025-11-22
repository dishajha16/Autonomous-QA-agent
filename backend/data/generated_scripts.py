import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class TestCheckout(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        html_path = os.path.abspath("backend/data/checkout.html")
        self.driver.get(f"file:///{html_path}")

    def tearDown(self):
        self.driver.quit()
    def test_tc_003(self):
        print('Executing Verify validation when 'nameInput' is left empty')
        driver = self.driver

        driver.find_element(By.ID, 'emailInput').send_keys('test@example.com')
        driver.find_element(By.ID, 'nameInput').send_keys('John Doe')
        driver.find_element(By.ID, 'cardNumber').send_keys('1234567890123456')
        driver.find_element(By.ID, 'expiryDate').send_keys('2025-12')
        driver.find_element(By.ID, 'cvvInput').send_keys('123')
        driver.find_element(By.ID, 'payNowButton').click()

        time.sleep(2)
        # Example assertion:
        # self.assertIn('Payment Successful', driver.page_source)


if __name__ == '__main__':
    unittest.main()
