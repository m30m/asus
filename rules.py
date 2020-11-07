# From somewhere import device_list
device_list = {}

class Rule():
    def __init__(self, statements, actions, weight = 1):
        self.actions = actions
        self.weight = weight
        self.all_expressions = []
        for expr in statements["all"]:
            self.all_expressions.append(BooleanExpression(*expr))
        self.any_expressions = []
        for expr in statements["any"]:
            self.any_expressions.append(BooleanExpression(*expr))

    def evaluate(self):
        flag1= True
        for expr in self.all_expressions:
            if expr.evaluate() == False:
                flag1= False
        flag2 = False
        for expr in self.any_expressions:
            if expr.evaluate() == True:
                flag2 = True
        return flag1 or flag2

    def execute(self):
        if self.evaluate():
            for action in self.actions.values():
                device = device_list[action["id"]]
                device.set_state(action["set_value"])

class BooleanExpression():
    def __init__(self, lhs, rhs, op):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        if lhs["type"] == "device":
            device = device_list[lhs["id"]]
            left_state_type = device.state_type
        elif  lhs["type"] == 'constant_continuous':
            left_state_type = "continuous"
        elif lhs["type"] == 'discrete':
            left_state_type = "discrete"

        if rhs["type"] == "device":
            device = device_list[rhs["id"]]
            right_state_type = device.state_type
        elif rhs["type"] == 'constant_continuous':
            right_state_type = "continuous"
        elif rhs["type"] == 'discrete':
            right_state_type = "discrete"
        assert(left_state_type==right_state_type)

    def evaluate(self):
        if self.lhs["type"] == "device":
            device = device_list[self.lhs["id"]]
            left_value = device.get_state()
        else:
            left_value = self.lhs["value"]
        if self.rhs["type"] == "device":
            device = device_list[self.lhs["id"]]
            right_value = device.get_state()
        else:
            right_value = self.rhs["value"]


        if self.op == "=":
            return left_value == right_value
        elif self.op == "<":
            return left_value < right_value
        elif self.op == ">":
            return left_value > right_value
        elif self.op == "<=":
            return left_value <= right_value
        elif self.op == ">=":
            return left_value <= right_value