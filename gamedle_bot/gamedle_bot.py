import json
import time

from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_driver():
    options = webdriver.ChromeOptions() 
    userdatadir = path.expandvars(r'%APPDATA%/Local/Google/Chrome/User Data')
    options.add_argument(f"--user-data-dir={userdatadir}")
    driver = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe", chrome_options=options)
    driver.maximize_window()
    return driver


def get_game_title(game_value, games_data):
    for item in games_data:
        if item.get('value') == game_value:
            return item.get('label')
    return ''


def submit_game_guess(driver, game_title, input_field):
    input_field.send_keys(game_title)

    li_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//li[normalize-space()="{game_title}"]')))
    li_element.click()

    guess_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "guess")))
    guess_button.click()


def press_next_button(driver):
    try:
        next_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "next")))
        next_button.click()
    except:
        pass


# def play_unlimited(num_games):
#     driver = get_driver()
#     driver.get("https://www.gamedle.wtf/unlimited")

#     if is_cookie_popup_active(driver):
#         accept_gamedle_cookies(driver)

#     games_json = driver.execute_script(f"return window.localStorage.getItem('gamelist')")
#     games_data = json.loads(games_json)

#     local_storage = "unlimitedBoardAC"

#     guess_game(num_games, driver, games_data, local_storage)

#     time.sleep(1)
#     driver.quit()

    
def guess_game(num_games, driver, games_data, local_storage):
    for _ in range(num_games):
        input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "search")))
        unlimitedBoardAC = driver.execute_script(f"return window.localStorage.getItem('{local_storage}')")
        unlimitedBoardAC_Data = json.loads(unlimitedBoardAC)
        game_value = unlimitedBoardAC_Data['gameLegendAC']['value']
        print(f"Game value: {game_value}")

        game_title = get_game_title(game_value, games_data)
        print(f"Game title: {game_title}")

        next_button = driver.find_element(By.ID, "next")
        restart_button = driver.find_element(By.ID, "restart")

        if next_button.is_displayed():
            next_button.click()

        if restart_button.is_displayed():
            restart_button.click()

        submit_game_guess(driver, game_title, input_field)
        press_next_button(driver)


def play_weekly():
    driver = get_driver()
    driver.get("https://www.gamedle.wtf/unlimitedweekly")

    if is_cookie_popup_active(driver):
        accept_gamedle_cookies(driver)

    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, f'//a[normalize-space()="YOU WON"]')))
    except:
        print("\nWeekly quiz has already been completed.\n")
        time.sleep(1)
        return

    games_json = driver.execute_script(f"return window.localStorage.getItem('gamelist')")
    games_data = json.loads(games_json)

    number_of_games_to_guess =  int(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "max_streaks"))).text.split('/')[1])

    local_storage = "unlimitedWeeklyBoardAC"

    press_next_button(driver)
    guess_game(number_of_games_to_guess, driver, games_data, local_storage)

    time.sleep(4)
    driver.quit()
    
def is_cookie_popup_active(driver):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "sp_message_iframe_809515")))
    except TimeoutException:
        return False
    return True

def accept_gamedle_cookies(driver):
        cookies_iframe = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "sp_message_iframe_809515")))
        driver.switch_to.frame(cookies_iframe)
        accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Accept"]')))
        accept_button.click()
        driver.switch_to.default_content()
        time.sleep(1)

def play_daily_modes(game_mode_url, local_storage_name):
    driver = get_driver()
    driver.get(game_mode_url)

    with open('games.json', encoding="utf8") as f:
        games_data = json.load(f)

    if "first_instructions" in driver.current_url:
        driver.get(game_mode_url)

    if is_cookie_popup_active(driver):
        accept_gamedle_cookies(driver)

    try:
        input_field = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.NAME, "search")))
    except:
        print("\nToday's quiz has already been completed.\n")
        time.sleep(1)
        return
    
    WrittenBoardAC = driver.execute_script(f"return window.localStorage.getItem('{local_storage_name}')")

    unlimitedBoardAC_Data = json.loads(WrittenBoardAC)
    game_value = unlimitedBoardAC_Data['original']['value']
    print(f"Game value: {game_value}")

    game_title = get_game_title(game_value, games_data)
    print(f"Game title: {game_title}")

    submit_game_guess(driver, game_title, input_field)

    time.sleep(3)


def main():

    print("Select in which game mode you want me to guess games:\n")
    game_modes = ["Weekly", "Guess", "Artwork", "Classic"]
    for index, mode in enumerate(game_modes, 1):
        print(f"[{index}] {mode}")
    user_choice = input("\nDecision: ")

    # if user_choice == "1":    
    #     num_games = int(input("Enter the number of games that should be guessed: "))
    #     play_unlimited(num_games)
    if user_choice == "1":
        play_weekly()
    elif user_choice == "2":
        play_daily_modes("https://www.gamedle.wtf/guess", "boardWrittenAC")
    elif user_choice == "3":
        play_daily_modes("https://www.gamedle.wtf/artwork", "boardArtworkAC")
    elif user_choice == "4":
        play_daily_modes("https://www.gamedle.wtf/classic", "boardAC")
    else:
        print("Do następnego.")
        return

if __name__ == '__main__':
    main()