import os
import sys
import threading
import time
import datetime as dt

os.makedirs("temp", exist_ok=True)

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service

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
