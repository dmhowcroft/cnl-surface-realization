import time

from deptree import DependencyTree

print("Loading spaCy for English...")
start_time = time.time()

import spacy
en_nlp = spacy.load('en')

print("Loaded in {} seconds.".format(time.time() - start_time))


def from_spacy_sentence(spacy_doc, find_root=True):
    """
    Produces a DependencyTree object from a spaCy doc.

    :param spacy_doc:
    :type spacy_doc: spacy.tokens.doc.Doc
    :param find_root:
    :type find_root: bool
    :return: a DependencyTree extracted from the doc
    :rtype: deptree.DependencyTree
    """
    if find_root:
        root = get_root(spacy_doc)
    else:
        root = spacy_doc
    dt = DependencyTree(str(root))
    dt.features['dependency_label'] = en_nlp.vocab[root.dep].orth_
    for child in root.children:
        child_tree = DependencyTree("")
        child_tree.from_spacy_sentence(child, find_root=False)
        dt.append(child_tree)
    return dt


def realize(deptree):
    out_string = deptree.label()
    left_edge_buffer = []
    left_mid_buffer = []
    left_buffer = []
    for child in deptree:
        attachment_decision = where_to_attach(child)
        if attachment_decision == -3:
            left_edge_buffer.append(realize(child))
        elif attachment_decision == -2:
            left_mid_buffer.append(realize(child))
        elif attachment_decision == -1:
            left_buffer.append(realize(child))
        elif attachment_decision == 1:
            out_string = out_string + " " + realize(child)
    for buffer in left_buffer, left_mid_buffer, left_edge_buffer:
        if buffer:
            out_string = " ".join(buffer) + " " + out_string
    return out_string


def where_to_attach(deptree):
    dep = deptree.features.get("dependency_label")
    if dep in ("det", "mark") or deptree.label() in ("when", ):
        return -3
    elif dep in ("nsubj", "nsubjpass", "amod", "nummod"):
        return -2
    elif dep in ("aux", "auxpass", "neg", "compound"):
        return -1
    else:
        return 1


def get_root(spacy_doc):
    """

    :param spacy_doc: spaCy document representing one sentence
    :type spacy_doc: spacy.tokens.doc.Doc
    :return:
    """
    token = spacy_doc[0]
    while token.head is not token:
        token = token.head
    return token


def print_dependencies(spacy_doc, from_root=True):
    if from_root:
        root = get_root(spacy_doc)
    else:
        root = spacy_doc
    print(root.dep, root)
    for child in root.children:
        print_dependencies(child, from_root=False)


if __name__ == "__main__":
    with open("ste100.sents", 'r') as example_file:
        line_count = 0
        for line in example_file:
            line_count += 1
            print("Processing example {}".format(line_count))
            print(line)
            dt = DependencyTree("")
            dt.from_spacy_sentence(en_nlp(line))
            print(dt)
            print(realize(dt))
            print("----------------")
            print()