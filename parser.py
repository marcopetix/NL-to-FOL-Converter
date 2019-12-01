import spacy_interaction
import dependency_switcher
import named_entity_recognition
import mongo
import library

def text_from_user(text = None):
    if text is None:
        text = input("Inserisci la frase da convertire: \n")
        parse_text(text)

def text_from_file():
    filename = input("Inserisci il nome del file: \nfile\\")
    with open("files\\'" + filename, 'r') as f:

        for line in f:

            text = line

            parse_text(text)

            if 'str' in line:
                break

def parse_text(text):
    doc = spacy_interaction.spacy_parsing(text)

    for token in doc:
        dependency_switcher.dep_switcher(token, variables, predicates, cond_tokens, passive_tokens, num_of_terms, isa_tokens)

    library.output(text, doc, predicates, variables, num_of_terms, cond_tokens, isa_tokens)

    named_entity_recognition.ent_recognition(doc)

    if isa_tokens == []:
        mongo.load_FLAT(doc, variables, predicates, cond_tokens, num_of_terms)
    else:
        mongo.load_ISA(doc, variables, predicates, cond_tokens, num_of_terms, isa_tokens)

    library.clear_lists(predicates, variables, cond_tokens, passive_tokens, num_of_terms, isa_tokens)

predicates, variables, cond_tokens, passive_tokens = [], [], [], []
num_of_terms = [0, 0]
isa_tokens = []

text_from_user()
