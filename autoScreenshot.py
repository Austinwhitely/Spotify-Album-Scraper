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
from webdriver_manager.chrome import ChromeDriverManager

os.makedirs("temp", exist_ok=True)


def open_web():
    service = Service(ChromeDriverManager().install())
    driver = uc.Chrome(service=service)
    driver.get("https://open.spotify.com/playlist/54EvyvoDP1AZBgfgh5bVP1")
    body = driver.find_element(By.TAG_NAME, "body")

    return body


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
