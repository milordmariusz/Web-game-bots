import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def accept_nerdle_cookies(driver):
    try:
        cookies_iframe = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "sp_message_iframe_633250")))
        driver.switch_to.frame(cookies_iframe)
        accept_cookies_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Accept"]')))
        accept_cookies_button.click()
        driver.switch_to.default_content()
    except:
        pass
