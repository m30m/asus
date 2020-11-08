class BooleanExpression():
    def __init__(self, rule, value, operator):
        self.rule = rule
        self.op = operator
        if not isinstance(value, bool):
            value = float(value)
        self.rhs = value

    def __str__(self):
        return str(self.rule) + str(self.op) + str(self.rhs)

    def evaluate(self):
        from state import device_ids
        self.lhs = device_ids[self.rule].get_state()
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
        from state import device_ids
        self.lhs = device_ids[self.rule].get_state()

