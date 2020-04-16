from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from threading import Thread
import asyncio
import random
import os


class RegieBoard:
    """Creates a Regie instance"""
    def __init__(self, profile_id, loop_timer, headless=False):
        self.headless = headless
        self.profile_id = profile_id
        self.presence_loop_timer = loop_timer
        self.reset_loop_timer = int(loop_timer * 4)
        self.driver = self.start_driver()
        self.loop = asyncio.get_event_loop()

    def start(self):
        """Start Regie instance"""
        #Loop to check presence status
        asyncio.ensure_future(self.check_if_live())
        asyncio.ensure_future(self.reset_channel())
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
        profiles_path = f'{os.getcwd()}/chrome_profiles/ch_p_'
        profile = f'--user-data-dir={profiles_path}{self.profile_id}'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(profile)
        chrome_options.add_argument('log-level=3')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--restore-last-session')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--disable-features=InfiniteSessionRestore')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        if self.headless == True:
            chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(f'{os.getcwd()}/driver/chromedriver.exe', options=chrome_options)
        driver.implicitly_wait(15)
        driver.get(self.get_drop_channel())
        self.check_if_muted()

        return driver

    def get_drop_channel(self):
        """Returns a random channel from cache (accounts/channels_live.txt)"""
        with open(f'{os.getcwd()}accounts/channels_live.txt') as file:
            links_raw = file.readlines()

        drop_channels = []
        for link in links_raw:
            drop_channels.append(link.strip())
        channel = random.choice(drop_channels)
        print(f'get_rand_drop_channel returned {channel}')

        return channel

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


def run(counter, loop_timer):
    asyncio.set_event_loop(asyncio.new_event_loop())
    RegieBoard(counter, loop_timer).start()

def docker_run(counter, loop_timer):
    RegieBoard(counter, loop_timer).start()


def main():
    instance_count = 16
    loop_timer = 1800
    counter = 1
    threads = []
    try:
        #Start Boards
        while counter <= instance_count+1:
            t = Thread(target=run, args=(counter, loop_timer))
            threads.append(t)
            t.start()
            counter += 1
        for t in threads:
            t.join()

    except KeyboardInterrupt:
        #Stop Boards
        while counter <= instance_count+1:
            RegieBoard(counter, loop_timer).stop()
            counter += 1
        for t in threads:
            t.stop()

if __name__ == "__main__":
    main()