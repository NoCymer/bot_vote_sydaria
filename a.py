# Generated by Selenium IDE
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from loguru import logger

# Configure Loguru to write logs to a file
logger.add("/home/gxku/Documents/pythonProject/app.log")

def setup_method():
    logger.info("Setting up the method")
    profile = FirefoxProfile('/home/gxku/snap/firefox/common/.mozilla/firefox/kwi4w3f0.script')
    options = Options()
    options.profile = profile
    options.add_argument('-headless')  # Enable headless mode
    driver = webdriver.Firefox(options=options)
    vars = {}
    return driver, vars

def teardown_method(driver):
    logger.info("Tearing down the method")
    # Comment the following line if you don't want the browser to close at the end
    # driver.quit()

def wait_for_window(driver, vars, timeout=2):
    time.sleep(round(timeout / 1000))
    wh_now = driver.window_handles
    wh_then = vars["window_handles"]
    if len(wh_now) > len(wh_then):
        return set(wh_now).difference(set(wh_then)).pop()

def run_sydariavote(driver, vars):
    logger.info("Starting the method")
    driver.get("https://sydaria.fr/vote")
    driver.set_window_size(550, 691)
    driver.find_element(By.ID, "stepNameInput").click()
    driver.find_element(By.ID, "stepNameInput").send_keys("NeggutsMS13")
    driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(2)").click()
    vars["window_handles"] = driver.window_handles

    while True:
        try:
            # Try to click immediately, without waiting for the element to be clickable
            driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(1)").click()
            logger.info("Button clicked successfully")
            break  # If the click is successful, break the loop
        except ElementClickInterceptedException:
            # If the element is not clickable, wait 5 minutes before trying again
            logger.info("Element not clickable, waiting for 5 minutes before retrying")
            time.sleep(5 * 60)

    vars["win4419"] = wait_for_window(driver, vars, 2000)
    vars["root"] = driver.current_window_handle
    driver.switch_to.window(vars["win4419"])
    driver.find_element(By.ID, "voteBtn").click()
    driver.close()
    driver.switch_to.window(vars["root"])
    logger.info("Method completed")

def main():
    driver, vars = setup_method()
    try:
        while True:
            run_sydariavote(driver, vars)
            logger.info("Waiting for 1h30m before next vote")
            time.sleep(1.5 * 60 * 60)  # Wait for 1h30m
    finally:
        teardown_method(driver)

if __name__ == "__main__":
    main()