from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def accept_flagle_cookies(driver):
    try:
        accept_cookies_button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, "accept-choices")))
        accept_cookies_button.click()
    except TimeoutException:
        pass