from os import path
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver


def get_driver():
    home_dir = path.expanduser("~")
    user_data_dir = path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"} # type: ignore
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
    driver.maximize_window()
    return driver