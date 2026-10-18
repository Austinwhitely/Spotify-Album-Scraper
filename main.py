###My essential imports and functions to play with Selenium on Python

import os
import sys
import threading
import time
import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service

ptime = lambda *x, end="\n": print(
    f"{dt.datetime.now().strftime('%m-%d %H:%M:%S')} -", *x, end=end
)

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")


def wait4elementByxPath(webDrvr, xPath):
    present = False
    counter = 0
    obj = None
    while present != True:
        if counter >= 50:
            break
        try:
            time.sleep(1)
            obj = webDrvr.find_element(by=By.XPATH, value=xPath)
            present = True
        except:
            time.sleep(1)
            counter = counter + 1
            continue
    return obj


############################################################


def wait4elementByCss(webDrvr, css_selector):
    present = False
    counter = 0
    obj = None
    while present != True:
        if counter >= 50:
            break
        try:
            time.sleep(1)
            obj = webDrvr.find_element(by=By.CSS_SELECTOR, value=css_selector)
            present = True
        except:
            time.sleep(1)
            counter = counter + 1
            continue
    return obj


############################################################


def LogInto(webDrvr, Username, Password):
    amIlogged = False

    authadress = "https://"
    try:
        webDrvr.get(authadress)

        time.sleep(2)
        driver.find_element(
            by=By.XPATH,
            value="/html/body/nl-root/nl-login/div/div/div/div/div/nl-slide-panel/div/div[1]/div/nl-login-form/form/div[1]/nl-input-add-on/div/input",
        ).send_keys(Username)
        driver.find_element(
            by=By.XPATH,
            value="/html/body/nl-root/nl-login/div/div/div/div/div/nl-slide-panel/div/div[1]/div/nl-login-form/form/div[2]/nl-input-add-on/div/input",
        ).send_keys(Password)
        time.sleep(2)
        driver.find_element(
            by=By.XPATH,
            value="/html/body/nl-root/nl-login/div/div/div/div/div/nl-slide-panel/div/div[1]/div/nl-login-form/form/button",
        ).click()

        wait4elementByxPath(
            webDrvr,
            "/html/body/nl-root/ng-component/main/div/mat-drawer-container/mat-drawer-content/nl-system-dashboard/div/section/nl-summary-box/div/div/div[1]/div[1]",
        )
        amIlogged = True
    except:
        amIlogged = False
        pass

    return amIlogged
