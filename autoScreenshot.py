import os
import random
import shutil
import time

import undetected_chromedriver as uc
from PIL import Image, ImageGrab
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AutoScreenshotter:
    def __init__(self, url, profile_dir="chrome_profile", temp_dir="temp"):
        self.url = url
        self.profile_path = os.path.abspath(profile_dir)
        self.temp_dir = temp_dir
        self.counter = 0
        self.driver = None
        self.scroll = """
        const elements = document.querySelectorAll('*');
        for (let el of elements) {
            if (el.scrollHeight > el.clientHeight && el.clientHeight > 0) {
                const style = window.getComputedStyle(el);
                if (style.overflowY === 'scroll' || style.overflowY === 'auto') {
                    el.scrollTop = 350;
                    break;
                }
            }
}
"""

        os.makedirs(self.temp_dir, exist_ok=True)

    def reset_profile(self):

        if os.path.exists(self.profile_path):
            shutil.rmtree(self.profile_path)
        self.open_web(False)
        input("Log in, then press any key to continue")

    def open_web(self, fullscreen: bool):
        profile_path = os.path.abspath("chrome_profile")

        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={profile_path}")
        if fullscreen:
            options.add_argument("--start-fullscreen")

        self.driver = uc.Chrome(options=options)
        self.driver.get(self.url)

        time.sleep(4)
        self.driver.execute_script("document.body.style.zoom='85%'")
        self.driver.execute_script(self.scroll)
        input("enter")

    def autoScroll(self):
        random_wait = random.randint(1, 15)
        assert self.driver is not None

        is_end_visible = self.driver.find_element(
            By.CSS_SELECTOR, "bottom-links"
        ).is_displayed()

        while not is_end_visible:
            if self.driver is not None:
                self.driver.implicitly_wait(random_wait)

            self.screenshot()
            self.driver.send_keys(Keys.PAGE_DOWN)
            is_end_visible = self.driver.find_element(
                By.CSS_SELECTOR, "bottom-links"
            ).is_displayed()
            random_wait = random.randint(1, 10)
        time.sleep(10)

    def screenshot(self):
        self.counter += 1
        im = ImageGrab.grab(bbox=(147, 245, 1068, 970))
        im.save(f"temp/screenshot_{self.counter}.png")
