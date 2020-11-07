

class BooleanExpression():
    def __init__(self, rule, value, operator):
        self.rule = rule

        self.op = operator

        from app import device_ids
        self.lhs = device_ids[rule].get_state()

        self.rhs = value

    def __str__(self):
        return str(self.lhs) + str(self.op) + str(self.rhs)

    def evaluate(self):
        if self.op == "=":
            return self.lhs == self.rhs
        elif self.op == "<":
            return self.lhs < self.rhs
        elif self.op == ">":
            return self.lhs > self.rhs
        elif self.op == "<=":
            return self.lhs <= self.rhs
        elif self.op == ">=":
            return self.lhs <= self.rhs

    def update(self):
        self.lhs = device_ids[self.lhs].get_state()