from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from threading import Thread
import asyncio
import random
import os
import sys
import datetime
import platform

if platform.system() == 'Linux':
    os.chdir('/home/apps')
if platform.system() == 'Windows':
    os.chdir(os.getcwd())


async def logger(msg):
    current_time = datetime.datetime.now()
    print(f'[{current_time}] {msg}')


class RegieBoard:
    """Creates a Regie instance"""

    def __init__(self, username, password, loop_timer=1800, headless=False):
        self.username = username
        self.password = password
        print(self.username, self.password)
        self.headless = headless
        self.loop = asyncio.get_event_loop()
        self.presence_loop_timer = loop_timer
        self.reset_loop_timer = int(loop_timer * 4)
        self.check_if_muted_timer = int(loop_timer / 2)

    async def start(self):
        """Start Regie instance"""
        self.start_time = datetime.datetime.now()
        # Start driver
        self.driver = await self.start_driver()
        # Login to Twitch using self.username and self.password
        await self.driver_twitch_login()
        await asyncio.sleep(5)
        # Open drop enabled channel
        self.driver.get(await self.get_drop_channel())
        # Waiting for ADs to play
        await asyncio.sleep(31)
        # Confirm mature stream
        await self.mature_stream_confirm()
        # Unmute video player
        await self.check_if_muted()
        # Loop to check presence status
        asyncio.ensure_future(self.check_if_live())
        asyncio.ensure_future(self.reset_channel())
        asyncio.ensure_future(self.check_if_muted())

    async def slim_start(self):
        """Start Regie without presence loops, return a driver"""
        self.driver = await self.start_driver()
        await logger(f'Slim-starting Regie {self.username}')
        return self.driver

    async def stop(self):
        """Stop Regie instance"""
        self.loop.stop()
        self.driver.quit()
        await logger(f'Stopping Regie {self.username}\nRegie was running since {self.start_time}')

    async def start_driver(self):
        """Start Chromedriver, return driver"""
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
        chrome_options.add_argument(
            '--disable-features=InfiniteSessionRestore')
        chrome_options.add_experimental_option(
            "excludeSwitches", ['enable-automation'])
        if self.headless == True:
            chrome_options.add_argument('--headless')
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
        self.driver = webdriver.Chrome(
            executable_path=driver_dir, options=chrome_options)
        self.driver.implicitly_wait(10)
        return self.driver

    async def driver_twitch_login(self):
        if not self.username or not self.password:
            await logger('Username or password not provided')
            return
        else:
            try:
                self.driver.get('https://www.twitch.tv/login')
                self.driver.find_element_by_xpath(
                    '//*[@id="login-username"]').send_keys(self.username)
                self.driver.find_element_by_xpath(
                    '//*[@id="password-input"]').send_keys(self.password, Keys.ENTER)
                await asyncio.sleep(5)
                try:
                    self.driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]').get_attribute('innerText')
                    await logger('Username or password not correct')
                    exit()
                except:
                    pass
                detect_2fa = await self.detect_2fa()
                if detect_2fa == False:
                    return False
                elif detect_2fa == True:
                    await logger(f'Logged in as username:{self.username}, password:{self.password}')
                    await asyncio.sleep(3)
                    return True
                else:
                    await logger(f'Failed to log in due to 2FA error using username:{self.username}, password:{self.password}')
                    exit()
            except:
                await logger(f'Failed to log in using username:{self.username}, password:{self.password}')
                exit()

    async def detect_2fa(self):
        try:
            mobile_2fa = driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div/span[1]').get_attribute('innerText')
            mobile_2fa_detected = True
            await logger(f'Found mobile 2FA. ({mobile_2fa})')
            exit()
        except:
            mobile_2fa_detected = False
        try:
            email_2fa = driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[1]/div[3]/div/div/div/div[3]/div[1]/p[3]').get_attribute(innerText)
            email_2fa_detected = True
            await logger(f'Found email 2FA. ({email_2fa})')
            exit()
        except:
            email_2fa_detected = False
        if mobile_2fa_detected == True:
            await logger('Detected Mobile 2FA')
            return True
        elif email_2fa_detected == True:
            await logger('Detected Email 2FA')
            return True
        else:
            await logger('No 2FA detected')
            return False

    async def get_drop_channel(self):
        """Returns a random channel from cache (channels_live.txt)"""
        with open('channels_live.txt') as file:
            links_raw = file.readlines()
        drop_channels = []
        for link in links_raw:
            drop_channels.append(link.strip())
        channel = random.choice(drop_channels)
        await logger(f'get_drop_channel returned {channel}')
        return channel

    # Need to rewrite
    async def check_if_live(self):
        """Check if the current channel is live and switch to a new channel if not"""
        while True:
            try:
                self.driver.find_element_by_xpath(
                    '//*[@id="root"]/div/div[2]/div/main/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[3]/div')
                await logger(f'Stream is live')
            except:
                await logger(f'Stream is not live, getting new channel')
                channel = await self.get_drop_channel()
                self.driver.get(channel)
            await self.mature_stream_confirm()
            await self.check_if_muted()
            await asyncio.sleep(self.presence_loop_timer)

    async def mature_stream_confirm(self):
        try:
            mature_btn = self.driver.find_element_by_xpath(
                '//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div/div/div/div[9]/div/div[3]/button')
            mature_btn.click()
            await logger('Mature audience prompt dismissed')
        except:
            await logger('Mature audience prompt not found')
            pass

    async def check_if_muted(self):
        """Check if the stream is muted"""
        asyncio.sleep(self.check_if_muted_timer)
        try:
            self.driver.find_element_by_xpath(
                '//*/button[@aria-label="Unmute (m)"]').send_keys('m')
            await logger('Stream was muted')
        except:
            await logger('Stream not muted')

    async def reset_channel(self):
        """Force move on to a different channel"""
        while True:
            await asyncio.sleep(self.reset_loop_timer)
            channel = await self.get_drop_channel()
            await logger(f'Force-moving to channel {channel}')
            self.driver.get(channel)
            await self.mature_stream_confirm()
            await self.check_if_muted()


def main():
    print('This function is not directly callable, use import regie.')


if __name__ == "__main__":
    main()
