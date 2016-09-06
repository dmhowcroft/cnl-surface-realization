import pickle
from deptree import DependencyTree
from nltk.stem import *
from nltk.stem.porter import *

stemmer = PorterStemmer()


def realize(deptree, with_stemming=True):
    """

    :param deptree:
    :type deptree: DependencyTree
    :return:
    """
    if deptree.features.get("dependency_label") in ("nsubj", "dobj", "conj", "compound"):
        return realize_noun_phrase(deptree, with_stemming)
    else:
        if with_stemming:
            out_string = stemmer.stem(deptree.label())
        else:
            out_string = deptree.label()
        left_edge_buffer = []
        left_mid_buffer = []
        left_buffer = []
        for child in deptree:
            attachment_decision = where_to_attach(child)
            if attachment_decision == -3:
                left_edge_buffer.append(realize(child, with_stemming))
            elif attachment_decision == -2:
                left_mid_buffer.append(realize(child, with_stemming))
            elif attachment_decision == -1:
                left_buffer.append(realize(child, with_stemming))
            elif attachment_decision == 1:
                out_string = out_string + " " + realize(child, with_stemming)
        for buffer in left_buffer, left_mid_buffer, left_edge_buffer:
            if buffer:
                out_string = " ".join(buffer) + " " + out_string
        return out_string


def where_to_attach(deptree):
    """

    :param deptree:
    :type deptree: DependencyTree
    :return:
    """
    dep = deptree.features.get("dependency_label")
    if dep in ("det", "mark") or deptree.label() in ("when", ):
        return -3
    elif dep in ("nsubj", "nsubjpass", "amod", "nummod"):
        return -2
    elif dep in ("aux", "auxpass", "neg", "compound"):
        return -1
    else:
        return 1


def realize_noun_phrase(deptree, with_stemming=True):
    if with_stemming:
        noun = stemmer.stem(deptree.label())
    else:
        noun = deptree.label()
    out_string = noun
    det = []
    amod = []
    compound = []
    prep = []
    cc = []
    conj = []
    for child in deptree:
        dep = child.features.get("dependency_label")
        if dep == "det":
            det.append(realize(child, with_stemming))
        elif dep in ("amod", "nummod"):
            amod.append(realize(child, with_stemming))
        elif dep in ("compound", ):
            compound.append(realize(child, with_stemming))
        elif dep in ("prep", ):
            prep.append(realize(child, with_stemming))
        elif dep == "cc":
            cc.append(realize(child, with_stemming))
        elif dep == "conj":
            conj.append(realize(child, with_stemming))
        else:
            amod.append(realize(child, with_stemming))
    for buffer in det, amod, compound:
        if buffer:
            out_string = " ".join(buffer) + " " + out_string
    for buffer in prep, cc, conj:
        if buffer:
            out_string = out_string + " " + " ".join(buffer)
    return out_string
        

if __name__ == "__main__":
    try:
        with open("ste100.pickle", 'rb') as ste_pickle:
            examples = pickle.load(ste_pickle)
    except FileNotFoundError:
        from load_from_spacy import load_examples
        examples = load_examples("ste100.sents")
    print(examples[0][0])
    print(examples[0][1])
    print(realize(examples[0][1]))
    print(realize(examples[0][1], with_stemming=False))
    for example in examples:
        print(example[0])
        print(example[1])
        print(realize(example[1], with_stemming=False))
        print()
