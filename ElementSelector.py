# from typing import List
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC, wait
# from selenium.webdriver.common.by import By
# #from PluralElementSelector import PluralElementSelector

# class ElementSelector:
    
#     selectors = []

#     def __init__(self, source):
#         if type(source) is list:
#             for element in source:
#                 self.selectors.append(ElementSelector(element))
#         else:
#             self.selectors.append(source)

#     def select(self, selection_type, selection_string):
#         elements = []
#         for selector in self.selectors:
#                 selection_function = selector._get_selection_function(selection_type)
#                 selection_result = selection_function(selection_string)
#                 elements.append(selection_result)
        
#         return ElementSelector(elements)
    
#     def _get_selection_function(self, selection_type):
#         selection_function = None

#         if selection_type == By.XPATH:
#             selection_function = self.html_element.find_element_by_xpath
#         elif selection_type == By.CLASS_NAME:
#             selection_function = self.html_element.find_elements_by_class_name
#         elif selection_type == By.CSS_SELECTOR:
#             selection_function = self.html_element.find_elements_by_css_selector
#         elif selection_type == By.ID:
#             selection_function = self.html_element.find_element_by_id
#         elif selection_type == By.TAG_NAME:
#             selection_function = self.html_element.find_elements_by_tag_name
        
#         return selection_function

#     def get_selection(self):
#         return self.html_element

#     class PluralElementSelector():
    
        

            

#         def select(self, selection_type, selection_string):
#             elements = []
           
            
#             return PluralElementSelector(elements)

#         def get_selection(self):
#             return map(lambda s: s.get_selection, self.selectors)


