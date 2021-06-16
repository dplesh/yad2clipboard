class Yad2Post:
    driver = None
    url = None
    
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
    
    def load(self):
        pass