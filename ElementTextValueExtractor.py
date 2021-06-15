from Extractor import Extractor
from selenium import webdriver


class XpathElementTextValueExtractor(Extractor):
    
    def __init__(self, driver, xpath_selector: str):
        self.driver = driver
        self.xpath_selector = xpath_selector
        
    
    def extract(self) -> str:
        return self.driver.get_element_by_xpath(self.xpath_selector).text
