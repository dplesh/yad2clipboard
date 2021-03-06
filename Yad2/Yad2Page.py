from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By

from .Yad2EstatePost import Yad2EstatePost # pylint: disable=import-error
from .Yad2VehiclePost import Yad2VehiclePost # pylint: disable=import-error
from .TargetSecurityTriggeredError import TargetSecurityTriggeredError # pylint: disable=import-error
from .PostFactory import PostFactory

FIREFOX_BINARY="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
USER_INTERACTION_DELAY = 200

class Yad2Page:
    url = None
    driver = None

    def __init__(self, url):
        self.url = url

    def load(self,user_interact):
        factory = (
            PostFactory()
            .register("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[1]/span[1]", Yad2EstatePost)
            .register("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[1]/p[1]", Yad2VehiclePost)
            )
        
        options = Options()
        options.headless = not user_interact
        options.binary = FIREFOX_BINARY
        options.add_argument("--window-size=1920,1200")

        driver = webdriver.Firefox(options=options)
        driver.get(self.url)        

        show_up_timeout = USER_INTERACTION_DELAY if user_interact else 10
        try:
            WebDriverWait(driver, show_up_timeout).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[4]/div")))
        except:
            raise TargetSecurityTriggeredError()

        self.driver = driver 
        post = factory.get_post(driver,self.url)
        return post        

    def close(self):
            self.driver.quit()
