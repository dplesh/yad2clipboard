from .Statement import Statement

class ConstructStatement(Statement):
    
    queries = None

    def __init__(self, *args):
        self.queries = args    

    def execute(self, element):
        results = []
        for query in self.queries:
            query.root = element
            current_query_results = list(map(lambda e: e.text, query.execute()))
            results.append(current_query_results)
        return list(zip(*results))