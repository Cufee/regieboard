from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

import asyncio

def start_ch_driver(profile_id, hl=False, debugger=False):
    profiles_path = 'chrome_profiles/ch_p_'
    profile = f'--user-data-dir={profiles_path}{profile_id}'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(profile)
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--restore-last-session')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    if hl == True:
        chrome_options.add_argument('--headless')
    if debugger != False:
        chrome_options.add_argument(f"--remote-debugging-port={debugger}")

    driver = webdriver.Chrome('driver/chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(15)
    return driver

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
    with open('channels_live.txt', "w") as file:
        for link in channel_links:
            file.write("".join(link) + "\n")
    print(f'Cache is now up to date')
    return channel_links

async def update_drop_cache(timer):
    while True:
        channel_search = start_ch_driver(0, True, 9333)
        channel_search.get(cat_url)
        get_drop_channels(channel_search)
        channel_search.quit()
        print(f'Waiting for {timer} seconds')
        await asyncio.sleep(timer)

def main():
    #Category and title keyword settings
    global cat_url
    cat_url = 'https://www.twitch.tv/directory/game/VALORANT'
    global title_keyword
    title_keyword = 'DROP'

    #Starting cache update loop
    cache_timer = 900
    cache_update_loop = asyncio.get_event_loop()
    cache_update_loop.create_task(update_drop_cache(cache_timer))
    try: 
        print(f'Cache loop started, running every {cache_timer} secods')
        cache_update_loop.run_forever()
    except KeyboardInterrupt:
        cache_update_loop.stop()

if __name__ == "__main__":
    main()