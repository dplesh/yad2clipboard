from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
from ElementTextValueExtractor import XpathElementTextValueExtractor


class HtmlElement:
    
    source = None
    
    def __init__(self,source):
        self.source = source
    