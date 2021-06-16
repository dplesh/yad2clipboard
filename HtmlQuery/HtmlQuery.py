from HtmlQuery.ConstructStatement import ConstructStatement
from selenium.webdriver.common.by import By
from .SelectStatement import SelectStatement # pylint: disable=import-error
from .WhereStatement import WhereStatement # pylint: disable=import-error

class HtmlQuery:

    statements = []
    current_roots = None
    root = None

    def __init__(self,root=None, query_steps=[]):
        self.statements = query_steps
        self.root = root

    def from_root(self, root):
        return HtmlQuery(root)

    def select(self, selection_type, selection_string):
        appended_stages = [*self.statements,SelectStatement(selection_type, selection_string)]
        return HtmlQuery(self.root, appended_stages)        

    def where(self, predicate):
        appended_stages = [*self.statements, WhereStatement(predicate)]
        return HtmlQuery(self.root, appended_stages)    

    def construct(self, *args):            
        appended_stages = appended_stages = [*self.statements, ConstructStatement(*args)]
        return HtmlQuery(self.root, appended_stages)

    def execute(self):
            current_roots = [self.root]
            for statement in self.statements:
                current_results = []
                for root in current_roots:
                    result = statement.execute(root)
                    if result == None:
                        continue
                    if type(result) is not list:
                        result = [result]
                    current_results += result
                current_roots = current_results
            return current_roots