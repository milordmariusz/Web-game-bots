from os import path
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver


def get_driver():
    home_dir = path.expanduser("~")
    user_data_dir = path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver