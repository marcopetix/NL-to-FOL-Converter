import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["nlp"]
col_sentences = mydb["Sentences"]
col_terms = mydb["Terms"]

def load_data(doc, variables, predicates, cond_tokens, num_of_terms, isa_tokens = None):
    sentence_to_add = { "value": doc.text }
    x = col_sentences.insert_one(sentence_to_add)
    sentence_id = x.inserted_id

    for predicate in predicates:
        term_to_add = {}
        term_to_add["id_sentence"] = sentence_id
        term_to_add["label"] = predicate.to_label(cond_tokens)
        term_to_add["arguments"] = predicate.to_arguments(variables, predicates, num_of_terms)

        if isa_tokens != []:
            term_to_add["hand_side"] = get_hand_side(predicate, isa_tokens)
            term_to_add["type"] = "ISA"
        else:
            term_to_add["hand_side"] = "BLANK"
            term_to_add["type"] = "FLAT"

        col_terms.insert_one(term_to_add)

def get_hand_side(predicate, isa_tokens):
    if predicate.main_token in isa_tokens:
        return "M"
    elif predicate.main_token.i < isa_tokens[0].i:
        return "L"
    else:
        return "R"
