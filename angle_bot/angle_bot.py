from svg.path import parse_path
from svg.path.path import Arc
from math import pi
from selenium import webdriver
from os import path
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_driver():
    home_dir = path.expanduser("~")
    user_data_dir = path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def is_cookie_popup_active(driver):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "sp_message_iframe_794238")))
    except TimeoutException:
        return False
    return True

def accept_angle_cookies(driver):
    cookies_iframe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sp_message_iframe_794238")))
    driver.switch_to.frame(cookies_iframe)
    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Accept"]')))
    accept_button.click()
    driver.switch_to.default_content()
    time.sleep(1)

def main():
    driver = get_driver()
    driver.get("https://angle.wtf/")

    if is_cookie_popup_active(driver):
        accept_angle_cookies(driver)

    angle_path_element = driver.find_elements(By.TAG_NAME, "path")

    angle_path = angle_path_element[2].get_attribute("d")

    path_data = angle_path
    path = parse_path(path_data)

    arc_length = 0
    for segment in path:
        if isinstance(segment, Arc):
            arc_length += segment.length()

    angle = int((arc_length * 360)/(2*pi*20))

    print(f"Angle: {angle}")

    input_field = driver.find_element(By.TAG_NAME, "input")
    input_field.send_keys(angle)

    guess_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//button[normalize-space()="Guess!"]')))
    guess_button.click()

    time.sleep(4)

    driver.quit()

if __name__ == '__main__':
    main()