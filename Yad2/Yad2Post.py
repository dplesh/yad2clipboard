#from ElementSelector import ElementSelector
from HtmlQuery.HtmlQuery import HtmlQuery # pylint: disable=import-error
from random import randrange
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
import time

class Yad2Post:
    
    driver = None
    url = None
    
    city =         None
    title =        None
    neighborhood = None
    rooms =        None
    floor =        None
    area =         None
    price =        None
    description =  None
    contact_name =  None

    contact_number = None

    details = []
    amenities = []

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.get_basic_data()

        self.load_extended_details()
        self.load_amenities()
        self.load_seller_contact_info()

    def get_basic_data(self):
        
        self.title = HtmlQuery(self.driver).select(By.XPATH,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/h4").execute()[0].text
        self.city = HtmlQuery(self.driver).select(By.XPATH,         "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[2]").execute()[0].text
        self.neighborhood = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[1]").execute()[0].text
        self.floor = HtmlQuery(self.driver).select(By.XPATH,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[1]/dd").execute()[0].text
        self.rooms = HtmlQuery(self.driver).select(By.XPATH,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[2]/dd").execute()[0].text
        self.area = HtmlQuery(self.driver).select(By.XPATH,         "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[3]/dd").execute()[0].text
        self.price = HtmlQuery(self.driver).select(By.XPATH,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/strong").execute()[0].text
        self.description = HtmlQuery(self.driver).select(By.XPATH,  "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/div/div/p").execute()[0].text
        self.contact_name = HtmlQuery(self.driver).select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span[2]").execute()[0].text


    def load_extended_details(self):        
        detail_items_selector = (
            HtmlQuery(self.driver)
            .select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/ul")
            .select(By.CLASS_NAME,"item")
        )

        titles = map(lambda html_element: html_element.text,detail_items_selector.select(By.CLASS_NAME, "title").execute())
        values = map(lambda html_element: html_element.text,detail_items_selector.select(By.CLASS_NAME, "value").execute())

        self.details = list(zip(titles,values))

    def load_amenities(self):
        
        def amenity_element_contains_check_icon(amenity):
                check_icon_found = ( 
                    HtmlQuery(amenity)
                    .select(By.TAG_NAME, "i")
                    .where(lambda i_tag: i_tag.get_attribute("class") == "y2i_check2")
                    .execute()
                )
                return len(check_icon_found) > 0
        
        query = (
            HtmlQuery(self.driver)
            .select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[3]/div") # select amenities container
            .select(By.CSS_SELECTOR, "[class^='info']") # select all amenity elements
            .where(amenity_element_contains_check_icon)
            .select(By.TAG_NAME, "span")
            )

        self.amenities = list(map(lambda element: element.text, query.execute()))

    def load_seller_contact_info(self):
        contactSellerButton = HtmlQuery(self.driver).select(By.XPATH, "//*[@id=\"lightbox_contact_seller_0\"]").execute()[0]
        wait_sec = randrange(2,6)
        print("Waiting for {wait_sec} seconds".format(wait_sec=wait_sec))
        time.sleep(wait_sec)
        contactSellerButton.click()
        try :
            self.contact_number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"lightbox_phone_number_0\"]"))).text
            print ("Phone number successfully got")
        except:
            print ("Phone number unavailable.")

    def format_post_string(self, template):       
        amenities_string = ', '.join(self.amenities)
        details = '\r\n'.join([(f"{title} - {value}") for (title, value) in self.details])
        formattedMessage = template.format(title=self.title, city=self.city,neighborhood=self.neighborhood,rooms=self.rooms,floor=self.floor,
                                            area=self.area,price=self.price,description=self.description,contactName=self.contact_name,
                                            contact_number=self.contact_number,url=self.url,amenities_list=amenities_string,details=details)
        return formattedMessage

    def __str__(self):    
        template = "{title}, {neighborhood} {city}\r\n{rooms}חדרים , {floor} קומה , {area} מ\"ר\r\n{details}\r\n{price}\r\n{description}\r\n{amenities_list}\r\n{contactName} - {contact_number}\r\n{url}"
        amenities_string = ', '.join(self.amenities)
        details = '\r\n'.join([(f"{title} - {value}") for (title, value) in self.details])
        formattedMessage = template.format(title=self.title, city=self.city,neighborhood=self.neighborhood,rooms=self.rooms,floor=self.floor,
                                            area=self.area,price=self.price,description=self.description,contactName=self.contact_name,
                                            contact_number=self.contact_number,url=self.url,amenities_list=amenities_string,details=details)
        return formattedMessage