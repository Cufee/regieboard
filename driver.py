from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from threading import Thread
import asyncio

import json
import random
from time import sleep


def start_ch_driver(profile_id, hl=False, debugger=False):
    profiles_path = 'chrome_profiles/ch_p_'
    profile = f'--user-data-dir={profiles_path}{profile_id}'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(profile)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--restore-last-session')
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    if hl == True:
        chrome_options.add_argument('--headless')
    if debugger != False:
        chrome_options.add_argument(f"--remote-debugging-port={debugger}")

    driver = webdriver.Chrome('driver/chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(15)
    return driver

def driver_twitch_login(driver, username, password):
    driver.get('https://www.twitch.tv/login')
    driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password-input"]').send_keys(password, Keys.ENTER)


def get_drop_channels(driver):
    all_titles = driver.find_elements_by_xpath('//*/div/a/div/h3')
    channel_indexes = []
    channel_links = []
    for title in all_titles:
        if title_keyword in title.text:
            channel_index = all_titles.index(title)
            channel_indexes.append(channel_index)
    all_names = driver.find_elements_by_xpath('//*/article/div[1]/div/div[1]/div[2]/div/p/a')
    for index in channel_indexes:
        channel_links.append(f'https://twitch.tv/{all_names[index].text}')
    driver.quit()
    with open('accounts/channels_live.txt', "w") as file:
        for link in channel_links:
            file.write("".join(link) + "\n")
    print(f'get_drop_channels returned {channel_links}')
    return channel_links

def update_drop_cache():
    channel_search = start_ch_driver(0, True, 9333)
    channel_search.get(cat_url)
    get_drop_channels(channel_search)

def get_rand_drop_channel():
    #Read the list of DROP enabled channels
    with open('accounts/channels_live.txt') as file:
        links_raw = file.readlines()
        drop_channels = []
        for link in links_raw:
            drop_channels.append(link.strip())
    channel = random.choice(drop_channels)
    print(f'get_rand_drop_channel returned {channel}')
    return channel


def verify_presence(driver):
    unmute_btn = '//*/button[@aria-label="Unmute (m)"]'
    mute_btn = '//*/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[7]/div/div/div[2]/div[1]/div[2]/div/div[1]/button[@aria-label="Mute (m)"]'
    #Play btn //*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[7]/div/div/div[2]/div[1]/div[1]/button
    #Settings btn //*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[7]/div/div/div[2]/div[2]/div[1]/div[2]/div/button
    #Quality btn /html/body/div[1]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[7]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/div/div/div[1]/button
    unmute_btn_bool = check_elem_visible(unmute_btn, driver)
    mute_btn_bool = check_elem_visible(mute_btn, driver)
    if unmute_btn_bool == True:
        print(f'Player muted {unmute_btn_bool}')
        driver.find_element_by_xpath('//*[@id="root"]').send_keys('m')
    else:
        print(f'Player muted {unmute_btn_bool}')

def check_elem_visible(elem, driver):
    try:
        driver.find_element_by_xpath(elem)
        return True
    except:
        return False

def kick_start_bot(profile_id):
    driver = start_ch_driver(profile_id)
    driver.get(get_rand_drop_channel())
    print(f'Driver started: {driver}')
    return driver

def check_if_live(driver):
    try:
        driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[3]/div')
        print(f'check_if_live returned {True}')
        return True
    except:
        print(f'check_if_live returned {False}')
        return False

def bot_live_check(driver):
    #Check if bot is on a LIVE stream
    live = check_if_live(driver)
    if live == True:
        print(f'Driver {driver} is live')
    else:
        print(f'Driver {driver} getting new channel')
        driver.get(get_rand_drop_channel())

def start_bot(live_check_timer, presence_timer, id):
    #Start bot
    driver = kick_start_bot(id)
    while True:
        bot_live_check(driver)
        sleep(live_check_timer)


def main():
    #Category and title keyword settings
    global cat_url
    cat_url = 'https://www.twitch.tv/directory/game/VALORANT'
    global title_keyword
    title_keyword = 'DROP'

    # #Starting cache update loop
    # cache_timer = 3600
    # cache_update_loop = asyncio.get_event_loop()
    # cache_update_loop.create_task(update_drop_cache(cache_timer))
    # cache_update_loop.run_forever()
    # print(f'Cache loop started, running every {cache_timer} secods')

    #Bot settings
    bots_count = 6 #Number of bots to start
    live_check_timer = 60 #How often to check if channel is live
    presence_timer = 360000 #How often to check if player is muted

    counter = 1
    threads = []
    while counter <= bots_count:
        t = Thread(target=start_bot, args=(live_check_timer, presence_timer, counter))
        threads.append(t)
        t.start()
        counter += 1
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    global cat_url
    cat_url = 'https://www.twitch.tv/directory/game/VALORANT'
    global title_keyword
    title_keyword = 'DROP'
    update_drop_cache()