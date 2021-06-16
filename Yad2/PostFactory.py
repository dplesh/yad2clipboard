from typing import Callable

from selenium.webdriver.common.by import By
from HtmlQuery.HtmlQuery import HtmlQuery # pylint: disable=import-error

class PostFactory:
    
    post_unique_element_to_constructor = []

    def register(self, unique_xpath_element: str, constructor: Callable):
        self.post_unique_element_to_constructor.append((unique_xpath_element, constructor))
        return self
    
    def get_post(self, driver, url):
        for xpath,ctor in self.post_unique_element_to_constructor:
            if len(HtmlQuery(driver).select(By.XPATH, xpath).execute()) >0:
                return ctor(driver,url)

    
