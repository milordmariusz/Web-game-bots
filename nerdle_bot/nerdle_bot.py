import json
import os
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from nerdle_cookies import accept_nerdle_cookies
from selenium_driver import get_driver

def close_nerdle_instruction(driver):
    try:
        close_instruction_button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//button[@tabindex="0"]')))
        close_instruction_button.click()
    except:
        pass


def provide_answer(driver, answer):
    actions = ActionChains(driver)
    answer_split = answer.split()
    for x in answer_split:
        actions.send_keys(x)
    actions.perform()
    enter_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="ENTER "]')))
    enter_button.click()


def retrive_solution_from_local_storage(driver):
    gameState = driver.execute_script(f"return window.localStorage.getItem('gameState')")
    gameState_json = json.loads(gameState)
    solution = gameState_json['solution']
    return solution


def main():
    driver = get_driver()
    driver.get("https://nerdlegame.com/")

    accept_nerdle_cookies(driver)

    close_nerdle_instruction(driver)

    random_answer = '21+37=58'

    try:
        provide_answer(driver, random_answer)
    except:
        print("\nToday's quiz has already been completed.\n")
        return

    solution = retrive_solution_from_local_storage(driver)
    
    provide_answer(driver, solution)

    print(f'\nCorrect answer: {solution}\n')
    
    time.sleep(5)

    driver.quit()

if __name__ == '__main__':
    main()