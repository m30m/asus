from tree import Node
from boolexpr import BooleanExpression


# From somewhere import device_list then comment the line below

class Rule(object):
  def __init__(self, rule_dict, weight=1):
    # print("andishe recieved the folowing rules", rule_dict)
    self.actions = rule_dict["actions"]
    self.weight = weight
    self.rule_dict = rule_dict
    # List of device ids that appear as an input to this rule
    self.dependent_devices = []
    self.root = self.build_tree(None, rule_dict)
    print(self.root, "finsihed tree")
    self.update_rule_given_id()

  def update_rule_given_id(self):
    from state import rules_given_id
    for device_id in self.dependent_devices:
      if device_id not in rules_given_id:
        rules_given_id[device_id] = []
      rules_given_id[device_id].append(self)

  def build_tree(self, parent_node, child_dict):
    if "children" not in child_dict["query"]:
      rule = child_dict["query"]["rule"]
      self.dependent_devices.append(rule)
      value = child_dict["query"]["value"]
      operator = child_dict["query"].get("operator", '=')
      expr = BooleanExpression(rule, value, operator)
      return Node("boolean_expression", parent=parent_node, value=expr)
    elif "children" in child_dict["query"]:
      node = Node(child_dict["query"]["logicalOperator"], parent=parent_node)
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

