import datetime as dt
import os
import sys
import threading
import time

os.makedirs("temp", exist_ok=True)

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
 

"""def autoScroll(webDrvr, scrollAmnt):
    
    ActionChains(webDrvr)\
        .scroll_by_amount(0, scrollAmnt)\
        .perform()
        
    time.sleep(10)    
    



service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://Bing.com/search?q=you")

autoScroll(driver, 500)
"""
