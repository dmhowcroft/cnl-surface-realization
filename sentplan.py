from nltk.tree import Tree
from nltk.compat import string_types


def parse_pred_logic_to_sp(sp_string, with_features=False):
    parts = sp_string.split("(")
    node_label = parts[0]
    if with_features:
        nl_parts = node_label.split(":")
        node_label = nl_parts[0]
        features = nl_parts[1:]
        feature_dict = {}
        if features:
            for feature in features:
                feature, value = feature.split("=")
                feature_dict[feature] = value
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
        return SentPlan(node_label, features=feature_dict, children=children)
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

    # Required Abstract Method overrides
    def _get_node(self):
        pass

    def _set_node(self, value):
        pass

    # Other overrides
    def pformat(self, margin=70, indent=0, nodesep='', parens='()', quotes=False, with_features=True):
        """
        :param margin: The right margin at which to do line-wrapping.
        :type margin: int
        :param indent: The indentation level at which printing
            begins.  This number is used to decide how far to indent
            subsequent lines.
        :type indent: int
        :param nodesep: A string that is used to separate the node
            from the children.  E.g., the default value ``':'`` gives
            trees like ``(S: (NP: I) (VP: (V: saw) (NP: it)))``.
        :param parens: The two characters to use as left and right parentheses.
        :type parens: basestring
        :param quotes: Indicates whether strings should be quoted.
        :type quotes: bool

        :return: A pretty-printed string representation of this tree.
        :rtype: str
        """

        # Try writing it on one line.
        s = self._pformat_flat(nodesep, parens, quotes, with_features)
        if len(s) + indent < margin:
            return s

        # If it doesn't fit on one line, then write it on multi-lines.
        if isinstance(self._label, string_types):
            output_label = self._label
            if with_features:
                for feature in self.features:
                    output_label += ":{}={}".format(feature, self.features[feature])
            s = '%s%s%s' % (parens[0], output_label, nodesep)
        else:
            s = '%s%s%s' % (parens[0], str(self._label), nodesep)
        for child in self:
            if isinstance(child, Tree):
                s += '\n' + ' ' * (indent + 2) + child.pformat(margin, indent + 2, nodesep, parens, quotes, with_features)
            elif isinstance(child, tuple):
                s += '\n' + ' ' * (indent + 2) + "/".join(child)
            elif isinstance(child, string_types) and not quotes:
                s += '\n' + ' ' * (indent + 2) + '%s' % child
            else:
                s += '\n' + ' ' * (indent + 2) + str(child)
        return s + parens[1]

    def _pformat_flat(self, nodesep, parens, quotes, with_features=True):
        child_strings = []
        for child in self:
            if isinstance(child, Tree):
                child_strings.append(child._pformat_flat(nodesep, parens, quotes, with_features))
            elif isinstance(child, tuple):
                child_strings.append("/".join(child))
            elif isinstance(child, string_types) and not quotes:
                child_strings.append('%s' % child)
            else:
                child_strings.append(str(child))
        if isinstance(self._label, string_types):
            if with_features:
                output_label = self._label
                for feature in self.features:
                    output_label += ":{}={}".format(feature, self.features[feature])
            else:
                output_label = self._label
            return '%s%s%s %s%s' % (parens[0], output_label, nodesep,
                                    " ".join(child_strings), parens[1])
        else:
            return '%s%s%s %s%s' % (parens[0], str(self._label), nodesep,
                                    " ".join(child_strings), parens[1])


if __name__ == "__main__":
    # Define test inputs
    test_measure_silica_gel_absorption = "measure(necessary(time, absorb(silica_gel, moisture)))"
    test_measure_silica_gel_absorption_w_props = "measure:mood=imp(necessary(time:det=def, absorb:mood=inf(silica_gel:det=def, moisture:det=def)))"

    # Test importing and printing without features
    test_without_features = parse_pred_logic_to_sp(test_measure_silica_gel_absorption)
    print(test_without_features)

    # Test importing and printing with features
    test_with_features = parse_pred_logic_to_sp(test_measure_silica_gel_absorption_w_props, with_features=True)
    print(test_with_features)
    print(test_with_features.features)