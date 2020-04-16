from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

import asyncio, random, os, datetime, platform

def start_driver():
    """Start Chromedriver, return driver"""
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--restore-last-session')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--disable-application-cache')
    chrome_options.add_argument('--disable-features=InfiniteSessionRestore')
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # if f'{platform.system()}' == 'Linux':
    #     driver_dir = '/usr/bin/chromedriver'
    # if f'{platform.system()}' == 'Windows':
    #     driver_dir = '\\regieboard\\driver\\chromedriver.exe'
    # else:
    #     try:
    #         raise FileNotFoundError
    #     except FileNotFoundError:
    #         await logger(f'Platform is not Linux or Windows. Unable to select driver! {platform.system()}')
    driver_dir = '/usr/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=driver_dir, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

if __name__ == "__main__":
    driver = start_driver()
    link = 'google.com'
    driver.get(link)