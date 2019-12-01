import library

class Entity:
    def __init__(self, ent_type, token):
        self.ent_type = ent_type
        self.token_list = [token]

    def to_predicate(self, variables, predicates, num_of_terms):
        entity = self.ent_type + "("

        entity += library.get_var(self.token_list[0], variables, predicates, num_of_terms)

        entity += ")"

        return entity
