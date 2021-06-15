from selenium.webdriver.common.by import By
from .Statement import Statement # pylint: disable=import-error

class SelectStatement(Statement):
    
    selection_string = None
    selection_type = None

    def __init__(self, selection_type, selection_string):
        self.selection_type = selection_type
        self.selection_string = selection_string

    def execute(self, element):
        selection_function = self._get_selection_function(element, self.selection_type)
        return selection_function(self.selection_string)

    def _get_selection_function(self,root, selection_type):
        selection_function = None

        if selection_type == By.XPATH:
            selection_function = root.find_element_by_xpath
        elif selection_type == By.CLASS_NAME:
            selection_function = root.find_elements_by_class_name
        elif selection_type == By.CSS_SELECTOR:
            selection_function = root.find_elements_by_css_selector
        elif selection_type == By.ID:
            selection_function = root.find_element_by_id
        elif selection_type == By.TAG_NAME:
            selection_function = root.find_elements_by_tag_name
        
        return selection_function
    