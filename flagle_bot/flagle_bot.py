import json
import os
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_driver import get_driver
from flagle_cookies import accept_flagle_cookies


def change_code_to_name(country_code):
    json_file_path = "data/main_round_data.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        countries = json.loads(f.read())
    
    country_name = ""
    for country in countries:
        if country["code"] == country_code:
            country_name = country["name"]
            break
    return country_name


def save_web_logs(driver):
    logs = driver.get_log("performance")
  
    with open("data/network_log.json", "w", encoding="utf-8") as f:
        f.write("[")
        for log in logs:
            network_log = json.loads(log["message"])["message"]
            if("Network.response" in network_log["method"]
                    or "Network.request" in network_log["method"]
                    or "Network.webSocket" in network_log["method"]):
                f.write(json.dumps(network_log)+",")
        f.write("{}]")


def get_flag_url_from_logs():
    json_file_path = "data/network_log.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        logs = json.loads(f.read())

    flag_url = ""
  
    for log in logs:
        try:
            url = log["params"]["request"]["url"]
            if url.endswith(".png") and "https://flagcdn.com/w320" in url:
                flag_url = url
        except Exception:
            pass

    return flag_url


def close_toast(driver):
    try:
        close_toast_button = driver.find_element(By.CLASS_NAME, "Toastify__close-button")
        close_toast_button.click()
    except:
        pass


def press_bonus_round_button(driver):
    bonus_round_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f'//a[normalize-space()="PLAY BONUS ROUND"]')))
    bonus_round_button.click()


def bonus_round_one(driver, country_name):
    press_bonus_round_button(driver)

    correct_country_shape_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//button[@data-country-name='{country_name}']")))
    correct_country_shape_button.click()

    time.sleep(1)

    close_toast(driver)


def bonus_round_two(driver, country_code):
    press_bonus_round_button(driver)

    json_file_path = "data/second_bonus_round_data.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        countries = json.loads(f.read())
    
    countries_neighbours = []
    for country in countries:
        if country["name"] == country_code.upper():
            countries_neighbours = country["neighbors"]
            break

    div_with_flag_buttons = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, f'grid-cols-4')))
    buttons_with_flags = div_with_flag_buttons.find_elements(By.TAG_NAME, "img")
    
    for button_flag in buttons_with_flags:
        button_flag_src = button_flag.get_attribute("src")
        button_country_code = os.path.splitext(os.path.basename(button_flag_src))[0]
        if button_country_code.upper() in countries_neighbours:
            button_flag.click()
            break

    time.sleep(1)

    close_toast(driver)


def bonus_round_three(driver, country_code):
    press_bonus_round_button(driver)

    json_file_path = "data/third_bonus_round_data.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        countries = json.loads(f.read())

    countries_population_answer = ""
    countries_currency_answer = ""

    for country in countries:
        if country["country"] == country_code.upper():
            countries_population_answer = country["population_answer"]
            countries_currency_answer = country["currency_name"]
            break

    answer_buttons = WebDriverWait(driver, 3).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "sc-iAKWXU")))
    for button in answer_buttons:
        button_text = button.text[3:]
        if button_text == countries_population_answer or button_text == countries_currency_answer:
            button.click()
            break

    time.sleep(2)

    close_toast(driver)


def main():
    driver = get_driver()
    driver.get("https://www.flagle.io/")

    accept_flagle_cookies(driver)

    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f'//a[normalize-space()="PLAY BONUS ROUND"]')))
        print("\nToday's quiz has already been completed.\n")
        time.sleep(3)
        driver.quit()
        return
    except: 
        pass

    save_web_logs(driver)
  
    flag_url = get_flag_url_from_logs()

    country_code = os.path.splitext(os.path.basename(flag_url))[0]
    country_name = change_code_to_name(country_code)

    input_element = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "react-select-2-input")))
    input_element.send_keys(country_name, Keys.ENTER)

    close_toast(driver)

    bonus_round_one(driver, country_name)

    bonus_round_two(driver, country_code)

    bonus_round_three(driver, country_code)

    time.sleep(3)

    driver.quit()

if __name__ == '__main__':
    main()