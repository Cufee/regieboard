from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from threading import Thread
import asyncio
import random
import os
os.chdir('/home/apps')

class RegieBoard:
    """Creates a Regie instance"""
    def __init__(self, username, password, loop_timer, headless=False):
        self.username = username
        self.password = password
        self.headless = headless
        self.loop = asyncio.get_event_loop()
        self.presence_lopo_timer = loop_timer
        self.reset_loop_timer = int(loop_timer * 4)
        self.check_if_muted_timer = int(loop_timer / 2)

    def start(self):
        """Start Regie instance"""
        #Start driver
        self.driver = self.start_driver()
        #Get drop channel
        self.driver.get(self.get_drop_channel())
        #Loop to check presence status
        asyncio.ensure_future(self.check_if_live())
        asyncio.ensure_future(self.reset_channel())
        asyncio.ensure_future(self.check_if_muted())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.stop()

    def slim_start(self):
        """Start Regie without loops, return a driver"""
        return self.driver

    def stop(self):
        """Stop Regie instance"""
        self.loop.stop()
        self.driver.quit()

    def start_driver(self):

        chrome_options = webdriver.ChromeOptions()
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
        if self.headless == True:
            chrome_options.add_argument('--headless')

        driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
        driver.implicitly_wait(15)

        return driver


    def driver_twitch_login(self):
        self.driver.get('https://www.twitch.tv/login')
        self.driver.find_element_by_xpath('//*[@id="login-username"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="password-input"]').send_keys(self.password, Keys.ENTER)


    def get_drop_channel(self):
        """Returns a random channel from cache (channels_live.txt)"""
        with open('channels_live.txt') as file:
            links_raw = file.readlines()

        drop_channels = []
        for link in links_raw:
            drop_channels.append(link.strip())
        channel = random.choice(drop_channels)
        print(f'get_rand_drop_channel returned {channel}')

        return channel

    #Need to rewrite
    async def check_if_live(self):
        """Check if the current channel is live and switch to a new channel if not"""
        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[3]/div')
                print(f'check_if_live returned {True}')
            except:
                print(f'check_if_live returned {False}')
                channel = self.get_drop_channel()
                self.driver.get(channel)
                try:
                     self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[9]/div/div[3]/button').click()
                except:
                    pass
            self.check_if_muted()
            await asyncio.sleep(self.presence_loop_timer)

    def check_if_muted(self):
        """Check if the stream is muted"""
        try:
            self.driver.find_element_by_xpath('//*/button[@aria-label="Unmute (m)"]').send_keys('m')
            print('stream was muted')
        except:
            print('Stream not muted')

    async def reset_channel(self):
        """Check if the current channel is live and switch to a new channel if not"""
        while True:
            channel = self.get_drop_channel()
            self.driver.get(channel)
            await asyncio.sleep(self.reset_loop_timer)

def main():
    pass

if __name__ == "__main__":
    main()