import os
import time
import glob
import csv
from selenium import webdriver
from selenium.webdriver import Chrome
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
    security_el: WebElement = browser.find_element_by_xpath("//select[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_ddlAllSecurityType_field']")
    # work through the select options
    security_opts: List[WebElement] = security_el.find_elements_by_tag_name('option')
    for o in security_opts:
        if id in o.text:
            o.click()
            # click download button
            download_btn: WebElement = browser.find_element_by_xpath("//input[@name='ctl00$BodyPlaceHolder$EndOfDayPricesView1$btnAllDownload$implementation$field']")
            download_btn.click()
            return


def __main__():
    username: str = os.getenv("USERNAME_COMMSEC")
    password: str = os.getenv("PASSWORD_COMMSEC")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    csv_path: str = os.getcwd() + "/csv"
    prefs = {
        "download.default_directory": csv_path
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # get browser up and running
    browser: WebDriver = Chrome(options=chrome_options)
    browser.implicitly_wait(5)
    # log in to Commsec website
    url: str = 'https://www2.commsec.com.au/Private/Charts/EndOfDayPrices.aspx'
    browser.get(url)
    user_fld: WebElement = browser.find_element_by_xpath("//input[@id='ctl00_cpContent_txtLogin']")
    user_fld.send_keys(username)
    user_fld.send_keys(Keys.TAB)
    el: WebElement = browser.switch_to.active_element
    el.send_keys(password)
    browser.find_element_by_xpath("//input[@id='ctl00_cpContent_btnLogin']").click()
    time.sleep(3)
    format_el: WebElement = browser.find_element_by_xpath(
        "//select[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_ddlAllFormat_field']")
    format_opts: List[WebElement] = format_el.find_elements_by_tag_name('option')
    for o in format_opts:
        if 'Stock Easy' in o.text:  # Stock Easy format preferred as it lists the dates as YYYYMMDD
            o.click()
    start_date: date = date(2017, 1, 1)
    end_date: date = date.today()
    while start_date < end_date:
        date_fld: WebElement = browser.find_element_by_xpath(
            "//input[@id='ctl00_BodyPlaceHolder_EndOfDayPricesView1_txtAllDate_field']")
        date_txt: str = start_date.strftime("%d/%m/%Y")
        js_txt: str = f"arguments[0].value = '{date_txt}'"
        browser.execute_script(js_txt, date_fld)
        # check if we already have this date
        eto_loc: str = f"{os.getcwd()}/prices/etos/*{start_date:%Y%m%d}*"
        eqt_loc: str = f"{os.getcwd()}/prices/equities/*{start_date:%Y%m%d}*"
        if start_date.isoweekday() < 6:
            find_eto_file: List[str] = glob.glob(eto_loc)
            if len(find_eto_file) == 0:
                select_option(browser, 'ETO')
            find_eqt_file: List[str] = glob.glob(eqt_loc)
            if len(find_eqt_file) == 0:
                select_option(browser, 'Equities')
        start_date = start_date + timedelta(days=1)


__main__()