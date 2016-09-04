from nltk.tree import Tree


class SentPlan(Tree):
    def __init__(self, node_label, *, properties=None, children=None):
        """
        Sent(ence)Plan object for input to a surface realization system.

        :param node_label: label for this node in the tree
        :param properties: mapping of properties to their values
        :param children: list of SentPlan objects which are children of this node
        :type node_label: basestring
        :type properties: dict
        :type children: list
        """
        self.set_label(node_label)
        if properties:
            self.properties = properties
        else:
            self.properties = {}
        if children:
            self.extend(children)

test = SentPlan('test', children=[SentPlan('a'), SentPlan('b')])
print(test)

test_measure_silica_gel_absorption = "measure(necessary(time, absorb(silica_gel, moisture)))"
test_measure_silica_gel_absorption_w_props = "measure:mood=imp(necessary(time:det=def, absorb:mood=inf(silica_gel:det=def, moisture:det=def)))"


def parse_pred_logic_to_sp(sp_string, with_properties=False):
    parts = sp_string.split("(")
    node_label = parts[0]
    if with_properties:
        nl_parts = node_label.split(":")
        node_label = nl_parts[0]
        properties = nl_parts[1:]
        prop_dict = {}
        if properties:
            for prop in properties:
                key, val = prop.split("=")
                prop_dict[key] = val
    rest = "(".join(parts[1:])
    level = 0
    arg = []
    args = []
    for char in rest[:-1]:
        arg.append(char)
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        elif char == "," and level == 0:
            args.append("".join(arg[:-1]))
            arg = []

    if arg:
        args.append("".join(arg))
    children = [parse_pred_logic_to_sp(arg, with_properties) for arg in args]
    if with_properties:
        return SentPlan(node_label, properties=prop_dict, children=children)
    else:
        return SentPlan(node_label, children=children)

tmp = parse_pred_logic_to_sp(test_measure_silica_gel_absorption)
print(tmp)

t2 = parse_pred_logic_to_sp(test_measure_silica_gel_absorption_w_props, with_properties=True)
print(t2)