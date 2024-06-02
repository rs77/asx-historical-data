import os
import time
import glob
import shutil
import csv
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from datetime import date, datetime, timedelta
from decimal import Decimal
from re import sub
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from typing import List, Dict, Optional, KeysView, Tuple

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cwd: str = os.getcwd()


def select_option(browser: WebDriver, id: str):
    """
    Selects the given option in the Security list
    :param browser:
    :param id:
    :return:
    """
    security_el: WebElement = browser.find_element(By.XPATH, "//select[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_ddlAllSecurityType_field']")
    # work through the select options
    security_opts: List[WebElement] = security_el.find_elements(By.TAG_NAME, 'option')
    for o in security_opts:
        if id in o.text:
            o.click()
            # click download button
            download_btn: WebElement = browser.find_element(By.XPATH, "//input[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_btnAllDownload_implementation_field']")
            download_btn.click()            
            return

def move_file(default_loc, new_loc: str):
    """
    Moves the downloaded file to the correct location
    :param loc:
    :return:
    """
    time.sleep(3)
    csv_files: str = os.listdir(default_loc)
    if len(csv_files) == 0:
        return
    csv_file: str = csv_files[0]
    os.makedirs(os.path.dirname(new_loc), exist_ok=True)
    shutil.move(os.path.join(default_loc, csv_file), new_loc)

def __main__():
    username: str = os.getenv("USERNAME_COMMSEC")
    password: str = os.getenv("PASSWORD_COMMSEC")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    main_dir: str = os.getcwd()
    csv_path: str = os.path.join(main_dir, "csv")
    prefs = {
        "download.default_directory": csv_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # get browser up and running
    browser: WebDriver = Chrome(options=chrome_options)
    browser.implicitly_wait(5)
    # log in to Commsec website
    url: str = 'https://www2.commsec.com.au/Private/Charts/EndOfDayPrices.aspx'    
    browser.get(url)
    user_fld: WebElement = browser.find_element(By.XPATH, "//input[@id='username']")
    user_fld.send_keys(username)
    user_fld.send_keys(Keys.TAB)
    el: WebElement = browser.switch_to.active_element
    el.send_keys(password)
    browser.find_element(By.XPATH, "//button[@id='login']").click()
    time.sleep(3)
    format_el: WebElement = browser.find_element(By.XPATH, 
        "//select[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_ddlAllFormat_field']")
    format_opts: List[WebElement] = format_el.find_elements(By.TAG_NAME, 'option')
    for o in format_opts:
        if 'Stock Easy' in o.text:  # Stock Easy format preferred as it lists the dates as YYYYMMDD
            o.click()
    start_date: date = date(2021, 7, 5)
    end_date: date = date.today()
    while start_date < end_date:
        date_fld: WebElement = browser.find_element(By.XPATH, 
            "//input[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_txtAllDate_field']")
        date_txt: str = start_date.strftime("%d/%m/%Y")
        js_txt: str = f"arguments[0].value = '{date_txt}'"
        browser.execute_script(js_txt, date_fld)
        # check if we already have this date
        eto_loc: str = os.path.join(main_dir, "prices", "etos", f"{start_date:%Y}", f"{start_date:%Y%m%d}.csv")
        eqt_loc: str = os.path.join(main_dir, "prices", "equities", f"{start_date:%Y}", f"{start_date:%Y%m%d}.csv")
        if start_date.isoweekday() < 6:            
            if not os.path.exists(eto_loc):
                select_option(browser, 'ETO')
                move_file(csv_path, eto_loc)
            if not os.path.exists(eqt_loc):
                select_option(browser, 'Equities')
                move_file(csv_path, eqt_loc)
        start_date = start_date + timedelta(days=1)


__main__()
