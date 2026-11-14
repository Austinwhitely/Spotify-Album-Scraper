import os
import time

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
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.bing.com/search?q=you")
    body = driver.find_element(By.TAG_NAME, "body")

    return body


def autoScroll(webDriver):

    body = open_web()
    is_end_visible = body.find_element(By.CSS_SELECTOR, "bottom-links").is_displayed()

    while not is_end_visible:
        webDriver.implicitly_wait(5)
        screenshot()
        body.send_keys(Keys.PAGE_DOWN)
        is_end_visible = body.find_element(
            By.CSS_SELECTOR, "bottom-links"
        ).is_displayed()
    time.sleep(10)


def screenshot():
    im = ImageGrab.grab(bbox=(147, 245, 1068, 970))
    im.show()
