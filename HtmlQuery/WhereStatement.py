from .Statement import Statement # pylint: disable=import-error

class WhereStatement(Statement):
    
    predicate = None

    def __init__(self, predicate) -> None:
        self.predicate = predicate

    def execute(self, element):
        if self.predicate(element):
            return element
        return None