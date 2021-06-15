#from ElementSelector import ElementSelector
from random import randrange
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
from ElementTextValueExtractor import XpathElementTextValueExtractor
from Es import Es
import time

class Yad2Post:
    
    driver = None
    url = None

    field_to_extractor = {}
    field_to_value = {}

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

    details_list = []
    amenities = []

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.declare_needed_data()

        self.load_extended_details()
        self.load_amenities()
        self.load_seller_contact_info()

    def declare_needed_data(self):
        
        self.field_to_extractor["title"] = XpathElementTextValueExtractor(self.driver,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/h4")
        self.field_to_extractor["city"] = XpathElementTextValueExtractor(self.driver,         "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[2]")
        self.field_to_extractor["neighborhood"] = XpathElementTextValueExtractor(self.driver, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[1]")
        self.field_to_extractor["floor"] = XpathElementTextValueExtractor(self.driver,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[1]/dd")
        self.field_to_extractor["rooms"] = XpathElementTextValueExtractor(self.driver,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[2]/dd")
        self.field_to_extractor["area"] = XpathElementTextValueExtractor(self.driver,         "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[3]/dd")
        self.field_to_extractor["price"] = XpathElementTextValueExtractor(self.driver,        "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/strong")
        self.field_to_extractor["description"] = XpathElementTextValueExtractor(self.driver,  "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/div/div/p")
        self.field_to_extractor["contact_name"] = XpathElementTextValueExtractor(self.driver, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span[2]")
        self.field_to_extractor["description"] = XpathElementTextValueExtractor(self.driver,  "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[2]")


    def load_extended_details(self):        
        detail_items_selector = (
            Es(self.driver)
            .select(By.XPATH, "/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/ul")
            .select(By.CLASS_NAME,"item")
        )

        titles = map(lambda html_element: html_element.text,detail_items_selector.select(By.CLASS_NAME, "title").get_selection())
        values = map(lambda html_element: html_element.text,detail_items_selector.select(By.CLASS_NAME, "value").get_selection())

        for title,value in zip(titles,values):
            self.details_list.append(f"{title} - {value}")     

        # details_wrapper = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/ul")
        # details = details_wrapper.find_elements_by_class_name("item")
        
        # for detail in details:
        #     detail_title = detail.find_element_by_class_name("title").text
        #     detail_value = detail.find_element_by_class_name("value").text
        #     self.details_list.append(f"{detail_title} - {detail_value}")

    def load_amenities(self):
        amenities_container = self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[3]/div")
        amenities = amenities_container.find_elements_by_css_selector("[class^='info']")

        
        # y2i_check2
        # y2i_close
        for amenity in amenities:
            amenity_icon = amenity.find_element_by_tag_name("i")
            if amenity_icon.get_attribute("class") == "y2i_check2":
                amenity_text = amenity.find_element_by_tag_name("span").text
                self.amenities.append(amenity_text)

    def load_seller_contact_info(self):
        contactSellerButton = self.driver.find_element_by_xpath("//*[@id=\"lightbox_contact_seller_0\"]")
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
        details = '\r\n'.join(self.details_list)
        formattedMessage = template.format(title=self.title, city=self.city,neighborhood=self.neighborhood,rooms=self.rooms,floor=self.floor,area=self.area,price=self.price,description=self.description,contactName=self.contact_name,contact_number=self.contact_number,url=self.url,amenities_list=amenities_string,details_list=details)
        return formattedMessage


    def __str__(self):    
        template = "{title}, {neighborhood} {city}\r\n{rooms}חדרים , {floor} קומה , {area} מ\"ר\r\n{details_list}\r\n{price}\r\n{description}\r\n{amenities_list}\r\n{contactName} - {contact_number}\r\n{url}"
        amenities_string = ', '.join(self.amenities)
        details = '\r\n'.join(self.details_list)
        formattedMessage = template.format(title=self.title, city=self.city,neighborhood=self.neighborhood,rooms=self.rooms,floor=self.floor,area=self.area,price=self.price,description=self.description,contactName=self.contact_name,contact_number=self.contact_number,url=self.url,amenities_list=amenities_string,details_list=details)
        return formattedMessage


    