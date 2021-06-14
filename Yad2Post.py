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

    details_list = []
    amneties = []




    def __init__(this, driver, url):
        this.driver = driver
        this.url = url
        
        this.load_basic_info()
        this.load_extended_details()
        this.load_amneties()
        this.load_seller_contact_info()



    def load_basic_info(this):
        this.title =          this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/h4").text
        this.city =           this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[2]").text
        this.neighborhood =   this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/span/span[1]").text
        this.rooms =          this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[1]/dd").text
        this.floor =          this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[2]/dd").text
        this.area =           this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/dl[3]/dd").text
        this.price =          this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[1]/div/div/div[2]/div[2]/div/strong").text
        this.description =    this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/div/div/p").text
        this.contact_name =    this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span[2]").text


    def load_extended_details(this):
        details_wrapper = this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[1]/div/ul")
        details = details_wrapper.find_elements_by_class_name("item")
        
        for detail in details:
            detail_title = detail.find_element_by_class_name("title").text
            detail_value = detail.find_element_by_class_name("value").text
            this.details_list.append(f"{detail_title} - {detail_value}")

    def load_amneties(this):
        amneties_container = this.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/main/div/div[3]/div[5]/div/div[2]/div[2]/div[1]/section[1]/div[3]/div")
        amneties = amneties_container.find_elements_by_css_selector("[class^='info']")

        
        # y2i_check2
        # y2i_close
        for amnety in amneties:
            amnety_icon = amnety.find_element_by_tag_name("i")
            if amnety_icon.get_attribute("class") == "y2i_check2":
                amnety_text = amnety.find_element_by_tag_name("span").text
                this.amneties.append(amnety_text)

    def load_seller_contact_info(this):
        contactSellerButton = this.driver.find_element_by_xpath("//*[@id=\"lightbox_contact_seller_0\"]")
        wait_sec = randrange(2,6)
        print("Waiting for {wait_sec} seconds".format(wait_sec=wait_sec))
        time.sleep(wait_sec)
        contactSellerButton.click()
        try :
            this.contact_number = WebDriverWait(this.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"lightbox_phone_number_0\"]"))).text
            print ("Phone number successfully got")
        except:
            print ("Phone number unavailable.")

    def format_post_string(this, template):       
        amneties_string = ', '.join(this.amneties)
        details = '\r\n'.join(this.details_list)
        formattedMessage = template.format(title=this.title, city=this.city,neighborhood=this.neighborhood,rooms=this.rooms,floor=this.floor,area=this.area,price=this.price,description=this.description,contactName=this.contact_name,contact_number=this.contact_number,url=this.url,amneties_list=amneties_string,details_list=details)
        return formattedMessage


    def __str__(this):    
        template = "{title}, {neighborhood} {city}\r\n{rooms}חדרים , {floor} קומה , {area} מ\"ר\r\n{details_list}\r\n{price}\r\n{description}\r\n{amneties_list}\r\n{contactName} - {contact_number}\r\n{url}"
        amneties_string = ', '.join(this.amneties)
        details = '\r\n'.join(this.details_list)
        formattedMessage = template.format(title=this.title, city=this.city,neighborhood=this.neighborhood,rooms=this.rooms,floor=this.floor,area=this.area,price=this.price,description=this.description,contactName=this.contact_name,contact_number=this.contact_number,url=this.url,amneties_list=amneties_string,details_list=details)
        return formattedMessage


    