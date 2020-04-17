from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from time import sleep
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
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
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
def reg_twitch():
    dd = random.randint(1, 28)
    mm = random.randint(1, 12)
    yyyy = random.randint(1980,2000)
    username = 'KEKCHEBURECK123'
    password = 'Zaq_12345Zaq_12345'
    driver = start_driver()
    actions = ActionChains(driver)
    driver.get('https://www.twitch.tv/signup')
    driver.find_element_by_xpath('//*[@id="signup-username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password-input"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="password-input-confirmation"]').send_keys(password)
    select = Select(driver.find_element_by_tag_name('select'))
    select.select_by_index(mm)
    actions.send_keys(Keys.TAB,dd, Keys.TAB, yyyy,Keys.TAB,'test@gearage.ru')
    actions.perform()
    sleep(random.uniform(9.0,15.0))
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/form/div/div[5]/button').click()
    return driver

def reg_rito():
    dd = random.randint(1, 28)
    mm = random.randint(1, 12)
    yyyy = random.randint(1980,2000)
    driver = start_driver()
    actions = ActionChains(driver)
    driver.get('https://beta.playvalorant.com/en-us/')
    driver.find_element_by_xpath('//*[@id="gatsby-focus-wrapper"]/section[1]/div[2]/aside/div/div[2]/div[1]/button/p/span[2]').click()
    sleep(random.uniform(8.0,12.0))
    driver.find_element_by_tag_name('input').send_keys('test@gearage.ru', Keys.ENTER)
    sleep(random.uniform(5.0,10.0))
    driver.find_element_by_tag_name('input').send_keys(dd, mm, yyyy, Keys.ENTER)
    sleep(random.uniform(5.0,7.0))
    driver.find_element_by_tag_name('input').send_keys('KEKCHEBURECK', Keys.ENTER)
    sleep(random.uniform(10.0,15.0))
    driver.find_element_by_tag_name('input').send_keys('Zaq_12345',Keys.TAB, 'Zaq_12345', Keys.ENTER)
    sleep(random.uniform(1.0,5.0))
    driver.find_element_by_tag_name('input').click()
    actions.send_keys(Keys.ENTER)
    actions.perform()
    return driver

if __name__ == "__main__":
        reg_twitch()

