import pickle
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
        child_tree = from_spacy_sentence(child, find_root=False)
        dt.append(child_tree)
    return dt


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


def load_examples(example_filename):
    examples = []
    with open(example_filename, 'r') as example_file:
        line_count = 0
        for line in example_file:
            line_count += 1
            print("Processing example {}".format(line_count))
            print(line)
            dt = from_spacy_sentence(en_nlp(line))
            print(dt)
            print(realize(dt))
            print("----------------")
            print()
            examples.append((line, dt))
    with open(".".join(example_filename.split(".")[:-1]) + ".pickle", 'wb') as ste_pickle:
        pickle.dump(examples, ste_pickle)
    return examples
