#!/usr/bin/env python3

import os
import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException
from loguru import logger

# Load configuration from external file
config = configparser.ConfigParser()
config.read('config.ini')

logger.add(config['DEFAULT']['LogPath'])

def setup_method():
    logger.info("Setting up the method")
    profile = FirefoxProfile(config['DEFAULT']['FirefoxProfilePath'])
    options = Options()
    options.profile = profile
    options.add_argument('-headless')

    current_working_directory = os.getcwd()

    # Log the current working directory
    logger.info(current_working_directory)
    options.binary_location = config['DEFAULT']['FirefoxBinaryPath']

    try:
        driver = webdriver.Firefox(options=options)
    except WebDriverException as e:
        logger.error(f"Failed to initialize the webdriver: {e}")
        return None, None

    vars = {}
    return driver, vars

def teardown_method(driver):
    logger.info("Tearing down the method")
    if driver:
        driver.quit()

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
    driver.find_element(By.ID, "stepNameInput").send_keys(config['DEFAULT']['Pseudo'])
    driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(2)").click()
    vars["window_handles"] = driver.window_handles

    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(1)").click()
            logger.info("Button clicked successfully")
            break
        except ElementClickInterceptedException:
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
    while True:
        driver, vars = setup_method()
        if driver is None:
            logger.error("Failed to setup the method, waiting for 5 minutes before retrying")
            time.sleep(5 * 60)
            continue

        try:
            run_sydariavote(driver, vars)
            logger.info("Waiting for 1h30m before next vote")
            time.sleep(1.5 * 60 * 60)
        finally:
            teardown_method(driver)

if __name__ == "__main__":
    main()