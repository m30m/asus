from app import device_ids


class BooleanExpression():
    def __init__(self, rule, operand, operator):
        self.lhs = rule
        self.rhs = operand
        self.op = operator
        self.left_value = device_ids[rule].get_state()
        self.right_value = self.rhs["value"]

    def evaluate(self):
        if self.op == "=":
            return self.left_value == self.right_value
        elif self.op == "<":
            return self.left_value < self.right_value
        elif self.op == ">":
            return self.left_value > self.right_value
        elif self.op == "<=":
            return self.left_value <= self.right_value
        elif self.op == ">=":
            return self.left_value <= self.right_value

    def update(self):
        self.left_value = device_ids[self.lhs].get_state()