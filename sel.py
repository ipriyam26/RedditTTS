#! ./venv/bin/python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
gave_error = []
i=0
for path in  glob.glob('videos/*.mp4'):
   
    driver.get("https://www.youtube.com/upload")
    driver.implicitly_wait(5)
    elem = driver.find_element_by_xpath("//input[@type='file']")
    try:
        elem.send_keys(f"/Users/ipriyam26/Programing/Reddit/{path}")
        r = randint(105,185)/10.0
        time.sleep(r)
        next_button = driver.find_element_by_xpath('//*[@id="next-button"]')
        next_button.click()
        r= randint(55,75)/10.0
        time.sleep(r)
        next_button.click()
        r= randint(55,75)/10.0
        time.sleep(r)
        next_button.click()
        # next_button = driver.find_element_by_xpath('//*[@id="next-button"]')
        #submit
        time.sleep(5.3)
        driver.find_element_by_xpath('//*[@id="done-button"]').click()
        r = randint(55,75)/10.0
        time.sleep(r)
    except:
        gave_error.append(path)
        print(f"Error aara iska bhai path - {path}")    
while len(gave_error)!=0:
    print(f"Left over:{len(gave_error)}")
    for video in gave_error:
        driver.get("https://www.youtube.com/upload")
        driver.implicitly_wait(5)
        elem = driver.find_element_by_xpath("//input[@type='file']")
        try:
            elem.send_keys(f"/Users/ipriyam26/Programing/Reddit/{video}")
            r = randint(65,105)/10.0
            time.sleep(r)
            box = driver.find_element_by_xpath('//*[@id="scrollable-content"]')
            r = randint(45,105)/10.0
            time.sleep(r)
            box.send_keys(Keys.END)
            r = randint(105,185)/10.0
            time.sleep(r)
            next_button = driver.find_element_by_xpath('//*[@id="next-button"]')
            next_button.click()
            r= randint(55,75)/10.0
            time.sleep(r)
            next_button.click()
            r= randint(55,75)/10.0
            time.sleep(r)
            next_button.click()
            # next_button = driver.find_element_by_xpath('//*[@id="next-button"]')
            #submit
            time.sleep(5)
            driver.find_element_by_xpath('//*[@id="done-button"]').click()
            r = randint(55,75)/10.0
            time.sleep(r)
            gave_error.remove(video)
        except:
            # gave_error.append(path)
            print(f"Error phir aara iska bhai, path - {video}") 
            
driver.close()
