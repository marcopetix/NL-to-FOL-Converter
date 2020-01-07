import library

pos_verbs = library.pos_verbs
dep_modifiers = library.dep_modifiers

class Predicate:
    def __init__(self, main_token, contatore, dep_token, subj_token = None, obj_token = None, prefix_token = None):
        self.main_token = main_token
        self.dep_token = dep_token
        self.contatore = contatore

        if subj_token is None:
            self.subj_token_list = []
        elif isinstance(subj_token, list):
            self.subj_token_list = subj_token
        else:
            self.subj_token_list = [subj_token]

        if obj_token is None:
            self.obj_token_list = []
        elif isinstance(obj_token, list):
            self.obj_token_list = obj_token
        else:
            self.obj_token_list = [obj_token]

        if prefix_token is None:
            self.prefix_token_list = []
        elif isinstance(prefix_token, list):
            self.prefix_token_list = prefix_token
        else:
            self.prefix_token_list = [prefix_token]

    def to_formula(self, variables, predicates, num_of_terms, cond_tokens):
        predicate = ""
        if self.prefix_token_list != []:
            for pre_token in self.prefix_token_list:
                predicate += library.get_lemma(pre_token, cond_tokens) + ":" + pre_token.tag_ + "_"

        predicate += library.get_lemma(self.main_token, cond_tokens)

        if self.contatore != "":
            predicate += str(self.contatore).zfill(2)

        predicate += ":" + self.main_token.tag_

        predicate += "(" + library.get_var(self.dep_token, variables, predicates, num_of_terms)

        if self.main_token.tag_ in pos_verbs and self.main_token.dep_ is not "pobj":
            if self.subj_token_list != []:
                predicate += ", " + library.get_var(self.subj_token_list[0], variables, predicates, num_of_terms)
            else:
                predicate += ", " + "___"
            if self.obj_token_list != []:
                predicate += ", " + library.get_var(self.obj_token_list[0], variables, predicates, num_of_terms)
            else:
                predicate += ", " + "___"
        elif self.subj_token_list != []:
            predicate += ", " + library.get_var(self.subj_token_list[0], variables, predicates, num_of_terms)

        predicate += ")"
        return predicate

    def to_arguments(self, variables, predicates, num_of_terms):
        arguments = "["

        arguments += library.get_var(self.dep_token, variables, predicates, num_of_terms)

        if self.subj_token_list != []:
            arguments += ", " + library.get_var(self.subj_token_list[0], variables, predicates, num_of_terms)
        else:
            arguments += ", _"

        if self.obj_token_list != []:
            arguments += ", " + library.get_var(self.obj_token_list[0], variables, predicates, num_of_terms)
        else:
            arguments += ", _"

        arguments += "]"

        return arguments

    def to_label(self, cond_tokens):
        label = ""
        if self.prefix_token_list != []:
            for pre_token in self.prefix_token_list:
                label += library.get_lemma(pre_token, cond_tokens) + ":" + pre_token.tag_ + "_"

        label += library.get_lemma(self.main_token, cond_tokens)

        if self.contatore != "":
            predicate += str(self.contatore).zfill(2)

        label += ":" + self.main_token.tag_

        return label
