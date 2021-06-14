from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By

from Yad2Post import Yad2Post
import TargetSecurityTriggeredException

FIREFOX_BINARY="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
USER_INTERACTION_DELAY = 200

class Yad2Page:
    url = None
    driver = None

    def __init__(this, url):
        this.url = url

    def load(this,user_interact):
        options = Options()
        options.headless = not user_interact
        options.binary = FIREFOX_BINARY
        options.add_argument("--window-size=1920,1200")


        driver = webdriver.Firefox(options=options)
        driver.get(this.url)

        show_up_timeout = USER_INTERACTION_DELAY if user_interact else 10
        try:
            element = WebDriverWait(driver, show_up_timeout).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/h4")))
        except:
            raise TargetSecurityTriggeredException()

        this.driver = driver 
        return Yad2Post(driver,this.url)

    def close(this):
            this.driver.quit()
