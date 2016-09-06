import pickle

if __name__ == "__main__":
    try:
        with open("ste100.pickle", 'rb') as ste_pickle:
            examples = pickle.load(ste_pickle)
    except FileNotFoundError:
        from load_from_spacy import load_examples
        examples = load_examples("ste100.sents")
