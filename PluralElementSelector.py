# from ElementSelector import ElementSelector

# class PluralElementSelector(ElementSelector):
    
#     selectors = []
    
#     def __init__(self, elements):
#         for element in elements:
#             self.selectors.append(ElementSelector(element))

#     def select(self, selection_type, selection_string):
#         elements = []
#         for selector in self.selectors:
#             element = selector.select(selection_type,selection_string)
#             elements.append(element)
        
#         return PluralElementSelector(elements)

#     def get_selection(self):
#         return map(lambda s: s.get_selection, self.selectors)
