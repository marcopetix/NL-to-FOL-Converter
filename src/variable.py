class Variable:
    def __init__(self, token, var):
        self.token_list = [token]
        self.var = var

    def to_print(self):
        variable = self.var + ": ["
        for token in self.token_list:
            variable += str(token.i) + "-" + token.lemma_ + "  "
        variable += "]"
        return variable
