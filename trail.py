#! ./venv/bin/python
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import geckodriver_autoinstaller
from random import randint
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import glob

geckodriver_autoinstaller.install()

profile = webdriver.FirefoxProfile(
    '/Users/ipriyam26/Library/Application Support/Firefox/Profiles/qq6tkzkd.default-release')

profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.update_preferences()
desired = DesiredCapabilities.FIREFOX

driver = webdriver.Firefox(firefox_profile=profile,
                           desired_capabilities=desired)

driver.get("https://www.youtube.com/upload")
driver.implicitly_wait(5)
elem = driver.find_element_by_xpath("//input[@type='file']")
elem.send_keys('/Users/ipriyam26/Programing/Reddit/videos/Build-A-Bear-workers-whats-the-strangest-voice-recording-youve-heard?-1-#short-#shorts.mp4')
time.sleep(5)
box = driver.find_element_by_xpath('//*[@id="scrollable-content"]')
box.send_keys(Keys.END)
time.sleep(600)