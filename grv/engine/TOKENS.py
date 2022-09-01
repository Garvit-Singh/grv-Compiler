TT_ID = 'ID'

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'

TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'

TT_GT = 'GT'
TT_LT = 'LT'
TT_GE = 'GE'
TT_LE = 'LE'
TT_EQ = 'EQ'
TT_NE = 'NE'
TT_ASSIGN = 'ASSIGN'

TT_OR = 'OR'
TT_NOT = 'NOT'
TT_AND = 'AND'

class TokenTypes():
    def __init__(self):
        self.token_dict = {
            TT_ID,
            TT_INT, TT_FLOAT, TT_STRING,
            TT_MUL, TT_DIV, TT_PLUS, TT_MINUS,
            TT_GT, TT_LT, TT_GE, TT_LE, TT_EQ, TT_ASSIGN,
            TT_OR, TT_NOT, TT_AND
        }

        self.token_op = {
            TT_MUL, TT_DIV, TT_PLUS, TT_MINUS,
            TT_GT, TT_LT, TT_GE, TT_LE, TT_EQ,
            TT_OR, TT_NOT, TT_AND
        }
    
    def getTokens(self):
        return self.token_dict

    def getOperators(self):
        return self.token_op