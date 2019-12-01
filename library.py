pos_verbs = ["BES", "HVS", "MD", "VB", "VBD", "VBN", "VBP", "VBZ", "VBG"]
dep_modifiers = ['amod', "advmod", "npadvmod", "nmod", "nummod", "npmod", "quantmod", "oprd"]

import predicate as Predicate
import variable as Variable



def same_lemma_tag(token_a, token_b):
    return token_a.lemma_ == token_b.lemma_ and token_a.tag_ == token_b.tag_

def get_lemma(token, cond_tokens):
    lemma = ""
    if token in cond_tokens:
        lemma = "COND"
    elif token.tag_ == "PRP" or token.tag_ == "PRP$" or (token.tag_ == "VBG" and token.dep_ in dep_modifiers):
        lemma = token.text
    else:
        lemma = token.lemma_
    #if (token.dep_ == "poss" and token.tag_ != "PRP$") or (token.dep_ == "compound" and token.head.dep_ == "poss"):
    #    lemma += "('s)"
    return lemma

def get_predicate(target_token, predicates):
    for predicate in predicates:
        if target_token == predicate.main_token:
            return predicate
    else:
        return None

def make_mono_predicate(token, predicates):
    if get_predicate(token, predicates) is None and (token.tag_ not in pos_verbs or (token.tag_ == "VBG" and token.dep_ in dep_modifiers)):
        predicates.append(Predicate.Predicate(token, token))

def make_predicate(predicates, main_token, dep_token, subj_token = None, obj_token = None, prefix_token = None):
    predicates.append(Predicate.Predicate(main_token, dep_token, subj_token, obj_token, prefix_token))

def name_var(token, num_of_terms):
    if token.tag_ in pos_verbs and token.dep_ is not "pobj":
        num_of_terms[1] += 1
        return "e" + str(num_of_terms[1])
    else:
        num_of_terms[0] += 1
        return "x" + str(num_of_terms[0])

def get_var(token, variables, predicates, num_of_terms):
    if token.dep_ is "xcomp":
        return get_var(token.head, variables, predicates, n_noun, n_verb)
    for variable in variables:
        if token in variable.token_list:
            return variable.var
    else:
        var = name_var(token, num_of_terms)
        variables.append(Variable.Variable(token, var))
        if token.tag_ not in pos_verbs or (token.tag_ == "VBG" and token.dep_ in dep_modifiers):
            make_mono_predicate(token, predicates)
        return var

def make_var(token, variables, predicates, num_of_terms):
    var = name_var(token, num_of_terms)
    variables.append(Variable.Variable(token, var))
    if token.tag_ not in pos_verbs or (token.tag_ == "VBG" and token.dep_ in dep_modifiers):
        make_mono_predicate(token, predicates)

def add_to_same_var_list(token_added, token_to_add, variables, predicates, num_of_terms):
    if variables:
        for variable in variables:
            if token_to_add not in variable.token_list:
                for token in variable.token_list:
                    if token_added == token:
                        variable.token_list.append(token_to_add)
                        make_mono_predicate(token_to_add, predicates)
                        #if not same_lemma_tag(token_added, token_to_add):
                        #    predicates.append(Predicate(token_to_add, token_to_add))
                        return
            else:
                return
    make_var(token_added, variables, predicates, num_of_terms)
    add_to_same_var_list(token_added, token_to_add, variables, predicates, num_of_terms)

def add_to_subj_list(token_to_add, target_token, variables, predicates,num_of_terms):
    for predicate in predicates:
        if target_token == predicate.main_token:
            if predicate.subj_token_list  != []:
                add_to_same_var_list(predicate.subj_token_list[0], token_to_add, variables, predicates, num_of_terms)
            predicate.subj_token_list.append(token_to_add)
            return True
    return False

def add_to_obj_list(token_to_add, target_token, variables, predicates, num_of_terms):
    for predicate in predicates:
        if target_token == predicate.main_token:
            if predicate.obj_token_list != []:
                add_to_same_var_list(predicate.obj_token_list[0], token_to_add, variables, predicates, num_of_terms)
            predicate.obj_token_list.append(token_to_add)
            return True
    return False

def add_to_prefix(token_to_add, target_token, predicates):
    for predicate in predicates:
        if target_token == predicate.main_token:
            predicate.prefix_token_list.append(token_to_add)
            return True
    return False

def until_not(dep, token):
    result_token = token
    while result_token.dep_ is dep:
        result_token = result_token.head
    return result_token

def print_table(doc):
    print("\n")
    print("{:<10}{:<15}{:<15}{:<15}{:<10}{:<15}{:<10}".format("ID", "TEXT", "DEPENDENCY", "HEAD", "ID_HEAD", "LEMMA", "POS"))
    for token in doc:
        print("{:<10}{:<15}{:<15}{:<15}{:<10}{:<15}{:<10}".format(token.i, token.text, token.dep_, token.head.lemma_, token.head.i, token.lemma_, token.tag_))

def print_predicates(variables, predicates, num_of_terms, cond_tokens):
    print("\n")
    print("PREDICATES:\n")
    for x in predicates:
        print(x.to_formula(variables, predicates, num_of_terms, cond_tokens))

def print_variables(variables):
    print("\n")
    print("VARIABLES:\n")
    for x in variables:
        print(x.to_print())

def print_isa(isa_tokens):
    print("\n")
    print("ISA TOKENS:\n")
    for x in isa_tokens:
        print(x.lemma_ + str(x.i))


def output(text, doc, predicates, variables, num_of_terms, cond_tokens, isa_tokens):
    print("\n{:<20}{:<150}".format("Text: ", text))
    print_table(doc)
    print_predicates(variables, predicates, num_of_terms, cond_tokens)
    print_variables(variables)
    print_isa(isa_tokens)
    print("\n")

def clear_lists(predicates, variables, cond_tokens, passive_tokens, num_of_terms, isa_tokens):
    if predicates:
        for predicate in predicates:
            predicate.subj_token_list.clear()
            predicate.obj_token_list.clear()
            predicate.prefix_token_list.clear()

        predicates.clear()

    if variables:
        for variable in variables:
            variable.token_list.clear()

        variables.clear()

    if cond_tokens:
        cond_tokens.clear()

    if passive_tokens:
        passive_tokens.clear()

    if isa_tokens:
        isa_tokens.clear()

    num_of_terms = [0, 0]
