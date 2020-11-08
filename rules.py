from tree import Node
from boolexpr import BooleanExpression
# From somewhere import device_list then comment the line below

class Rule(object):
    def __init__(self, rule_dict, weight = 1):
        # print("andishe recieved the folowing rules", rule_dict)
        self.actions = rule_dict["actions"]
        self.weight = weight
        self.rule_dict = rule_dict
        # List of device ids that appear as an input to this rule
        self.dependent_devices = []
        self.root = self.build_tree(None,rule_dict)
        print(self.root, "finsihed tree")
        from state import rules_given_id
        for device_id in self.dependent_devices:
            if device_id not in rules_given_id:
                rules_given_id[device_id] = []
            rules_given_id[device_id].append(self)
    def build_tree(self,parent_node, child_dict):
        if "children" not in child_dict["query"]:
            rule = child_dict["query"]["rule"]
            self.dependent_devices.append(rule)
            value = child_dict["query"]["value"]
            operator = child_dict["query"].get("selectedOperator", '=')
            expr = BooleanExpression(rule, value, operator)
            return Node("boolean_expression", parent=parent_node, value=expr)
        elif "children" in child_dict["query"]:
            node = Node(child_dict["query"]["logicalOperator"],parent=parent_node)
            for child in child_dict["query"]["children"]:
                node.children.append(self.build_tree(node, child))
            return node


    def evaluate(self):
        return self.root.evaluate()


    def execute(self):
        from state import device_ids
        if self.evaluate():
            for action in self.actions:
                device = device_ids[action["device_id"]]
                device.set_state(action["value"])
"""
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

"""
if __name__ == "__main__":
    amme = {
      "logicalOperator": "all",
      "children": [
        {
          "type": "query-builder-rule",
          "query": {
            "rule": 0,
            "operator": "=",
            "operand": "Vegetable",
            "value": 0
          }
        },
        {
          "type": "query-builder-rule",
          "query": {
            "rule": 0,
            "operand": "Fruit",
            "operator": "<",
            "value": 20
          }
        },
        {
          "type": "query-builder-group",
          "query": {
            "logicalOperator": "any",
            "children": [
              {
                "type": "query-builder-rule",
                "query": {
                  "rule": 0,
                  "operator": ">",
                  "operand": "Vegetable",
                  "value": 5
                }
              },
              {
                "type": "query-builder-rule",
                "query": {
                  "rule": 0,
                  "operator": "<",
                  "operand": "Vegetable",
                  "value": -20
                }
              }
            ]
          }
        }
      ]
    }
    rule = Rule(amme)
    print(rule.root)
    print(rule.evaluate())