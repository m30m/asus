
class Node(object):
    def __init__(self, type, parent=None, value=None):
        # type can be one of three values "all", "any", or "boolean_expression"
        self.type = type
        self.children = []
        self.parent = parent
        # in case of boolean expressions the value is the boolean expression
        self.value = value
    def evaluate(self):
        if self.type == "boolean_expression":
            return self.value.evaluate()
        elif self.type == "all":
            for child in self.children:
                if child.evaluate()==False:
                    return False
            return True
        elif self.type == "any":
            for child in self.children:
                if child.evaluate()==True:
                    return False
            return False

    def __str__(self):
        if self.type == "boolean_expression":
            return self.value.__str__()
        else:
            str = self.type + "["
            for node in self.children:
                str = str + node.__str__() + " "
            str = str + "]"
            return str