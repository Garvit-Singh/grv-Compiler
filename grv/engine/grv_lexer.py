from sly import Lexer
from grv_error import Error
from grv_token import Token

class GameLexer(Lexer):
    def __init__(self):
        self.line_number = 1
        self.nesting_level = 0
        self.statement_number = 1
        self.reserved = [
            'if', 'elif', 'else', 'while', 'func', 'True', 'False',
            'break', 'return', 'continue', 'console'
        ]

    tokens = {
        'INT', 'FLOAT', 'STRING',
        'ASSIGN',
        'MUL', 'DIV', 'PLUS', 'MINUS',
        'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
        'OR', 'NOT', 'AND'
    }
    
    literals = [
        '{', '}', '[', ']', '(', ')', '.', ',', ';'
    ]

    # literals
    @_('\(')
    def lopen(self, t):
        return Token(self.line_number, t.index, '(', t.value)
    @_('\)')
    def lclose(self, t):
        return Token(self.line_number, t.index, ')', t.value)
    @_('\[')
    def aopen(self, t):
        return Token(self.line_number, t.index, '[', t.value)
    @_('\]')
    def aclose(self, t):
        return Token(self.line_number, t.index, ']', t.value)
    @_('\.')
    def DOT(self, t):
        return Token(self.line_number, t.index, '.', t.value)
    @_(',')
    def COMMA(self, t):
        return Token(self.line_number, t.index, ',', t.value)

    # Integers or Floats
    @_(r'\d+')
    def INT(self, t):
        return Token(self.line_number, t.index, 'INT', t.value)
    @_(r'[0-9]*\.[0-9]+')
    def FLOAT(self, t):
        return Token(self.line_number, t.index, 'FLOAT', t.value)

    # String 
    @_(r'\'.*\'')
    def STRING(self, t):
        return Token(self.line_number, t.index, 'STRING', t.value)

    # __inbuilt__ functions
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*__')
    def INBUILT(self, t):
        return Token(self.line_number, t.index, 'INBUILT', t.value)

    # Language Keywords, Variables Identifiers
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        if(t.value in self.reserved):
            return Token(self.line_number, t.index, t.value.upper(), t.value)
        else:
            return Token(self.line_number, t.index, 'ID', t.value)

    # Update Line Number
    @_('\n')
    def newline(self, t):
        self.line_number += 1
        return

    # Update New Statement
    @_(';')
    def newstatement(self, t):
        self.statement_number += 1
        return Token(self.line_number, t.index, ';', t.value)

    # Update Nesting Level
    @_('{')
    def lbrace(self, t):
        tok = Token(self.line_number, t.index, '{', t.value)
        self.nesting_level += 1
        return tok
    @_('}')
    def rbrace(self, t):
        tok = Token(self.line_number, t.index, '}', t.value)
        self.nesting_level -= 1
        return tok

    # Ignore Comments nd Spaces
    ignore_space = r'[ ]+'
    ignore_tab = r'[\t]+'
    ignore_comment = r'\#.*'

    # Arthematic Operators
    PLUS    = r'\+'
    @_(PLUS)
    def PLUS(self, t):
        return Token(self.line_number, t.index, 'PLUS', t.value)
    MINUS   = r'-'
    @_(MINUS)
    def MINUS(self, t):
        return Token(self.line_number, t.index, 'MINUS', t.value)
    MUL     = r'\*'
    @_(MUL)
    def MUL(self, t):
        return Token(self.line_number, t.index, 'MUL', t.value)
    DIV     = r'/'
    @_(DIV)
    def DIV(self, t):
        return Token(self.line_number, t.index, 'DIV', t.value)

    # Comparision Operators
    EQ      = r'=='
    @_(EQ)
    def EQ(self, t):
        return Token(self.line_number, t.index, 'EQ', t.value)
    LE      = r'<='
    @_(LE)
    def LE(self, t):
        return Token(self.line_number, t.index, 'LE', t.value)
    LT      = r'<'
    @_(LT)
    def LT(self, t):
        return Token(self.line_number, t.index, 'LT', t.value)
    GE      = r'>='
    @_(GE)
    def GE(self, t):
        return Token(self.line_number, t.index, 'GE', t.value)
    GT      = r'>'
    @_(GT)
    def GT(self, t):
        return Token(self.line_number, t.index, 'GT', t.value)
    NE      = r'!='
    @_(NE)
    def NE(self, t):
        return Token(self.line_number, t.index, 'NE', t.value)
    
    # Assignment Operators
    ASSIGN  = r'='
    @_(ASSIGN)
    def ASSIGN(self, t):
        return Token(self.line_number, t.index, 'ASSIGN', t.value)
    
    # Logical Operators
    NOT     = r'!'
    @_(NOT)
    def NOT(self, t):
        return Token(self.line_number, t.index, 'NOT', 'not')
    OR      = r'\|\|'
    @_(OR)
    def OR(self, t):
        return Token(self.line_number, t.index, 'OR', 'or')
    AND     = r'\&\&'
    @_(AND)
    def AND(self, t):
        return Token(self.line_number, t.index, 'AND', 'and')

    # Token Errors
    def error(self, t):
        error = Error('Illegal Character', self.line_number, t.value)
        return error