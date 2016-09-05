from nltk.tree import Tree


def parse_pred_logic_to_sp(sp_string, with_features=False):
    parts = sp_string.split("(")
    node_label = parts[0]
    if with_features:
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
    children = [parse_pred_logic_to_sp(arg, with_features) for arg in args]
    if with_features:
        return SentPlan(node_label, features=prop_dict, children=children)
    else:
        return SentPlan(node_label, children=children)


class SentPlan(Tree):
    def __init__(self, node_label, *, features=None, children=None):
        """
        Sent(ence)Plan object for input to a surface realization system.

        :param node_label: label for this node in the tree
        :param features: mapping of properties to their values
        :param children: list of SentPlan objects which are children of this node
        :type node_label: basestring
        :type features: dict
        :type children: list
        """
        self.set_label(node_label)
        if features:
            self.features = features
        else:
            self.features = {}
        if children:
            self.extend(children)


if __name__ == "__main__":
    # Define test inputs
    test_measure_silica_gel_absorption = "measure(necessary(time, absorb(silica_gel, moisture)))"
    test_measure_silica_gel_absorption_w_props = "measure:mood=imp(necessary(time:det=def, absorb:mood=inf(silica_gel:det=def, moisture:det=def)))"

    # Test importing and printing without features
    without_features = parse_pred_logic_to_sp(test_measure_silica_gel_absorption)
    print(without_features)

    # Test importing and printing with features
    with_features = parse_pred_logic_to_sp(test_measure_silica_gel_absorption_w_props, with_features=True)
    print(with_features)