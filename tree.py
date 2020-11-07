
class Node(object):
    def __init__(self, type, children, parent, value=None):
        # type can be one of three values "all", "any", or "boolean_expression"
        self.type = type
        self.children = children
        self.parent = parent
        # in case of boolean expressions the value is the boolean expression
        self.value = value
    def evaluate(self):
        if self.type == "boolean_expression":
            return self.value.evaluate()
        elif type == "all":
            for child in self.children:
                if child.evaluate()==False:
                    return False
            return True
        elif type == "any"
            for child in self.children:
                if child.evaluate()==True:
                    return False
            return False
