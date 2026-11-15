import os
import random
import time

import undetected_chromedriver as uc
from PIL import Image, ImageGrab
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import shutil


os.makedirs("temp", exist_ok=True)
url = "https://open.spotify.com/playlist/54EvyvoDP1AZBgfgh5bVP1"


def reset_profile():
    shutil.rmtree("chrome_profile")
    profile_path = os.path.abspath("chrome_profile")
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = uc.Chrome(options=options)
    driver.get(url)

    input("press enter")
    return driver


def open_web():
    profile_path = os.path.abspath("chrome_profile")

    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--start-fullscreen")

    driver = uc.Chrome(options=options)

    driver.get(url)
    driver.execute_script("document.body.style.zoom+'50%'")
    input("enter")
    return driver


def autoScroll(webDriver):
    random_wait = random.randint(1, 10)
    body = open_web()
    is_end_visible = body.find_element(By.CSS_SELECTOR, "bottom-links").is_displayed()

    while not is_end_visible:
        webDriver.implicitly_wait(random_wait)
        screenshot()
        body.send_keys(Keys.PAGE_DOWN)
        is_end_visible = body.find_element(
            By.CSS_SELECTOR, "bottom-links"
        ).is_displayed()
        random_wait = random.randint(1, 10)
    time.sleep(10)


def screenshot():
    im = ImageGrab.grab(bbox=(147, 245, 1068, 970))
    im.show()
