from selenium.webdriver.common.by import By

class Es:

    selectors = []
    current_roots = None
    root = None

    def __init__(self,root, selectors=[]):
        self.selectors = selectors
        self.root = root

    def from_root(self, root):
        return Es(root)

        
    def select(self, selection_type, selection_string):
        appended_selectors = [*self.selectors,(selection_type, selection_string)]
        return Es(self.root, appended_selectors)
        

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
    
    def get_selection(self):
            current_roots = [self.root]
            for selector in self.selectors:
                current_selection_results = []
                for root in current_roots:
                    selection_type = selector[0]
                    selection_string = selector[1]
                    selection_function = self._get_selection_function(root,selection_type)
                    elements = selection_function(selection_string)
                    if type(elements) is not list:
                        elements = [elements]
                    current_selection_results += elements
                current_roots = current_selection_results
            return current_roots