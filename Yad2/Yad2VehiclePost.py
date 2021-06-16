from random import randrange
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
import time

from .Yad2Post import Yad2Post # pylint: disable=import-error
from selenium.webdriver.common.by import By
from HtmlQuery.HtmlQuery import HtmlQuery # pylint: disable=import-error

class Yad2VehiclePost(Yad2Post):

    title = None
    brand = None
    model = None
    year = None
    hand = None
    price = None
    displacement = None
    location = None
    description = None
    additional_details = []
    contact_name = None
    air_pollution_level = None

    contact_phone_number = None
    

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.load_basic_details()
        self.load_additional_details()
        self.load_pollution_level()
        self.load_seller_contact_info()
    
    def load_basic_details(self):
        self.model = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[1]/span[2]").execute()[0].text
        self.brand = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[1]/span[1]").execute()[0].text
        self.year = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/dl[1]/dd").execute()[0].text
        self.hand = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/dl[2]/dd").execute()[0].text
        self.price = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[3]/strong").execute()[0].text
        self.displacement = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[2]/dl[3]/dd").execute()[0].text
        self.location = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[3]/div[2]/div/div[3]/div[1]/span[2]").execute()[0].text
        self.description = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[1]/div[2]/div/div/p").execute()[0].text
        self.contact_name = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/div[1]/span[2]").execute()[0].text
        self.title = self.model

    def load_additional_details(self):
        detail_title_query = HtmlQuery().select(By.TAG_NAME, "dt")
        detail_value_query = HtmlQuery().select(By.TAG_NAME, "dd").select(By.TAG_NAME, "span")
        
        detail_rows = (
            HtmlQuery(self.driver)
            .select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[1]/div[3]/div[1]/div/div[2]")
            .select(By.TAG_NAME, "dl")
            .construct(detail_title_query, detail_value_query).execute()
        )

        for title, value in detail_rows:
            self.additional_details.append((title,value))
        

    def load_pollution_level(self):
        
        def pollution_arrow_found(pollution_element):
            return len(HtmlQuery(pollution_element).select(By.TAG_NAME, "i").execute()) > 0
        
        self.air_pollution_level = (
            HtmlQuery(self.driver)
            .select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div")
            .select(By.TAG_NAME, "div")
            .where(pollution_arrow_found).execute()[0].text
        )
    
    def load_seller_contact_info(self):
        contactSellerButton = HtmlQuery(self.driver).select(By.XPATH, "//*[@id=\"lightbox_contact_seller_0\"]").execute()[0]
        wait_sec = randrange(2,6)
        print("Waiting for {wait_sec} seconds".format(wait_sec=wait_sec))
        time.sleep(wait_sec)
        contactSellerButton.click()
        try :
            self.contact_phone_number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"lightbox_phone_number_0\"]"))).text
            print ("Phone number successfully got")
        except:
            print ("Phone number unavailable.")

    def __str__(self):    
        template = "{brand} {year}\r\n {model}\r\n{hand} יד , {displacement} סמ\"ק \r\n{price}\r\n{location}\r\n{additional_details}\r\n{description}\r\nרמת זיהום אוויר - {air_pollution_level}\r\n{contact_name} - {contact_phone_number}\r\n{url}"
        return self.format_post_string(template)

    def format_post_string(self, template):
        additional_details_string = '\r\n'.join([(f"{title} - {value}") for (title, value) in self.additional_details])
        formattedMessage = template.format(brand=self.brand, year=self.year,model=self.model,hand=self.hand,displacement=self.displacement,price=self.price,
                                            location=self.location,additional_details=additional_details_string,description=self.description,
                                            air_pollution_level=self.air_pollution_level,url=self.url,contact_name=self.contact_name,contact_phone_number=self.contact_phone_number)
        return formattedMessage