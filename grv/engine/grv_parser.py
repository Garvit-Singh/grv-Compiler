from grv_node import Node
from grv_error import Error
from TOKENS import TokenTypes

class ast:
    def __init__(self, token_idx, top_level = False, inside_while = False, inside_function = False):
        self.inside_function = inside_function
        self.inside_while = inside_while
        self.top_level = top_level
        self.token_idx = token_idx
        self.current_token = None
        self.head = None 
        self.tail = None

    # advance the token pointer in stream
    def advance(self):
        self.token_idx += 1
        if(self.token_idx < len(tokens)):
            self.current_token = tokens[self.token_idx]
        return
    
    # __repr__ token identifier function
    def __repr__(self):
        print(f'[{self.current_token.type} {self.current_token.value} {self.current_token.lineno} {self.current_token.index}]')
        return

    # insert node at the end of currently runnning level
    def insert_end(self, node):
        self.tail.next = node
        self.tail = self.tail.next
    
    # insert list at the level below the current level
    def insert_below(self, node):
        self.tail.below = node

    # insert new line node at the end of currently running level
    def line_break(self):
        # new line after each part in same level
        new_node = Node('NEWLINE', '\n')
        self.insert_end(new_node)

    # insert pass statement node at the end of currently running level
    def add_pass(self):
        new_node = Node('PASS', 'pass\n')
        self.insert_end(new_node)

    def check(self, tok):
        # check for balanced parenthesis
        last_tok = None
        open_paren = 0
        close_paren = 0
        for cur_tok in tok:
            if(cur_tok.value in ['}', '{', ';', '=']):
                return False
            if(cur_tok.value == '('):
                open_paren += 1
            if(cur_tok.value == ')'):
                close_paren += 1
            if(last_tok != None and last_tok.type in tokentypes.getOperators() and cur_tok.type not in {'INT', 'FLOAT', 'ID', 'STRING', '('}):
                return False
            if(last_tok != None and last_tok.type == ')' and (cur_tok.type not in tokentypes.getOperators() and cur_tok.type != ')')):
                return False
            if(open_paren < close_paren):
                return False
            last_tok = cur_tok
        
        if(open_paren != close_paren):
            return False

        return (last_tok == None or last_tok.type not in tokentypes.getOperators())

    def expr(self):
        # error check expression
        # make new node of expression w/ value = string
        # append to tail
        # return on semilcolon
        s = ''
        equal = False
        tok = []
        while(self.token_idx < len(tokens) and self.current_token.value != ';'):
            s += self.current_token.value + ' '
            equal = equal or (self.current_token.type == 'ASSIGN')
            tok.append(self.current_token)
            self.advance()
        
        if(equal):
            if(not (len(tok)>2 and tok[0].type == 'ID' and tok[1].type == 'ASSIGN')):
                return self.token_idx, Error('Unexpected Assignment', self.current_token.lineno, 0)
            if(not self.check(tok[2:])):
                return self.token_idx, Error('Unexpected expression', self.current_token.lineno, 0)

        else:
            if(not self.check(tok)):
                return self.token_idx, Error('Unexpected expression', self.current_token.lineno, 0)
        
        # removed len(s) >= 0
        if(self.token_idx < len(tokens)):
            # expression node
            new_node = Node('Expression', s)
            self.insert_end(new_node)
            return 
        return self.token_idx, Error('Expected ; or empty string', self.current_token.lineno, self.current_token.index)
    
    # if, else, while conditions
    def condition(self):
        # condition open parenthesis
        if(self.current_token.value != '('):
            return self.token_idx, Error('Expected (', self.current_token.lineno, self.current_token.index)
        new_node = Node('LOPEN', self.current_token.value)
        self.insert_end(new_node)
        self.advance()

        # condition expression
        s = ''
        tok = []
        open_paren = 0
        close_paren = 0
        while(self.token_idx < len(tokens)):
            if(self.current_token.value == '('):
                open_paren += 1
            if(self.current_token.value == ')'):
                close_paren += 1

            if(open_paren>=close_paren):
                s += str(self.current_token.value)
                s += ' '
                tok.append(self.current_token)
                self.advance()
            else:
                break
        
        if(not self.check(tok)):
            return self.token_idx, Error('Unexpected expression', self.current_token.lineno, self.current_token.index)

        if(self.token_idx >= len(tokens)):
            return self.token_idx, Error('Incomplete Expression', self.current_token.lineno, ')')

        # expression node
        new_node = Node('Expression', s)
        self.insert_end(new_node)
        
        # condition close parenthesis
        if(self.current_token.value != ')'):
            return self.token_idx, Error('Expected )', self.current_token.lineno, self.current_token.index)
        new_node = Node('LCLOSE', self.current_token.value)
        self.insert_end(new_node)
        return

    # func, call function, inbuilt
    def parameters(self):
        # condition open parenthesis
        if(self.current_token.value != '('):
            return self.token_idx, Error('Expected (', self.current_token.lineno, self.current_token.index)
        new_node = Node('LOPEN', self.current_token.value)
        self.insert_end(new_node)
        self.advance()

        while(self.token_idx < len(tokens) and self.current_token.type != ')'):
            s = ''
            tok = []
            open_paren = 0
            close_paren = 0
            while(self.token_idx < len(tokens) and self.current_token.type != ','):
                if(self.current_token.value == '('):
                    open_paren += 1
                if(self.current_token.value == ')'):
                    close_paren += 1
                
                if(open_paren>=close_paren):
                    s += str(self.current_token.value)
                    s += ' '
                    tok.append(self.current_token)
                    self.advance()
                else:
                    break

            if(not self.check(tok)):
                return self.token_idx, Error('Invalid Parameter', self.current_token.lineno, self.current_token.index)
            
            # expression node
            new_node = Node('Expression', s)
            self.insert_end(new_node)

            # insert LCLOSE OR COMMA
            if(self.current_token.type == ','):
                new_node = Node('COMMA', self.current_token.value)
                self.insert_end(new_node)
                self.advance()

        # condition close parenthesis
        if(self.current_token.value != ')'):
            return self.token_idx, Error('Expected )', self.current_token.lineno, self.current_token.index)
        new_node = Node('LCLOSE', self.current_token.value)
        self.insert_end(new_node)
        return

    # make new ast for a new level in code
    def block(self, inside_function = False, inside_while = False):
        # change open paranthesis to ':'
        if(self.current_token.value != '{'):
            return self.token_idx, Error('Expected {', self.current_token.lineno, self.current_token.index)
        new_node = Node('THEN', ':')
        self.insert_end(new_node)
        
        # recursively create new level
        self.token_idx, new_list = ast(self.token_idx, inside_while=inside_while, inside_function=inside_function).code()
        if(isinstance(new_list, Error)):
            return self.token_idx, new_list
        self.current_token = tokens[self.token_idx]
        self.insert_below(new_list)

        # check it again
        self.add_pass()

        # check block ending
        if(self.current_token.value != '}'):
            return self.token_idx, Error('Expected }', self.current_token.lineno, self.current_token.index)

    def code(self):
        self.head = Node('EMPTY', '\n')
        self.tail = self.head

        self.advance()
        while(self.token_idx < len(tokens) and self.current_token.value != '}'):
            # print(self.current_token.__repr__())
            if(self.current_token.type == 'IF' or self.current_token.type == 'ELIF'):
                # if case
                new_node = Node(self.current_token.type, self.current_token.value)
                self.insert_end(new_node)
                self.advance()

                err = self.condition()
                if(err != None):
                    return err
                self.advance()

                # case body
                err = self.block(inside_function=self.inside_function, inside_while=self.inside_while)
                if(err != None):
                    return err

            elif(self.current_token.type == 'ELSE'):                
                # else case
                new_node = Node(self.current_token.type, self.current_token.value)
                self.insert_end(new_node)
                self.advance()

                # case body
                err = self.block(inside_function=self.inside_function, inside_while=self.inside_while)
                if(err != None):
                    return err

            elif(self.current_token.type == 'WHILE'):
                # loop begin
                new_node = Node(self.current_token.type, self.current_token.value)
                self.insert_end(new_node)
                self.advance()

                # looping condition
                err = self.condition()
                if(err != None):
                    return err
                self.advance()

                # loop body
                err = self.block(inside_function=self.inside_function, inside_while=True)
                if(err != None):
                    return err

            elif(self.current_token.type == 'FUNC'):
                # function declaration                
                new_node = Node(self.current_token.type, 'def')
                self.insert_end(new_node)
                self.advance()

                # function name
                if(self.current_token.type != 'ID'):
                    return self.token_idx, Error('Function Name not declared!', self.current_token.lineno, self.current_token.index)
                new_node = Node(self.current_token.type, self.current_token.value)
                self.insert_end(new_node)
                self.advance()

                # function parameters
                err = self.parameters()
                if(err != None):
                    return err
                self.advance()

                # function body
                err = self.block(inside_function=True)
                if(err != None):
                    return err
                
            else:
                if(self.current_token.type in { 'CONTINUE', 'BREAK'}):
                    # continue statement
                    if(not self.inside_while):
                        return self.token_idx, Error(f'{self.current_token.value} used without a loop', self.current_token.lineno, self.current_token.value)
                    new_node = Node(self.current_token.type, self.current_token.value)
                    self.insert_end(new_node)
                    self.advance()

                    # expect a semicolon
                    if(self.current_token.type != ';'):
                        return self.token_idx, Error(f'{self.current_token.value} followed by something', self.current_token.lineno, self.current_token.value)

                elif(self.current_token.type == 'RETURN'):
                    # continue statement
                    if(not self.inside_function):
                        return self.token_idx, Error(f'{self.current_token.value} used without a function', self.current_token.lineno, self.current_token.value)
                    new_node = Node(self.current_token.type, self.current_token.value)
                    self.insert_end(new_node)
                    self.advance()
                    
                    # # expect a semicolon
                    # if(self.current_token.type != ';'):
                    #     return self.token_idx, Error(f'Return followed by something', self.current_token.lineno, self.current_token.value)

                    # expression statement
                    err = self.expr()
                    if(err != None):
                        return err 
                    
                elif(self.current_token.type == 'CONSOLE'):
                    new_node = Node(self.current_token.type, 'print')
                    self.insert_end(new_node)
                    self.advance()
                    
                    # check for open parenthesis
                    if(self.current_token.type != '('):
                        return self.token_idx, Error('Expected opening parenthesis after console', self.current_token.lineno, self.current_token.index)
                    new_node = Node(self.current_token.type, self.current_token.value)
                    self.insert_end(new_node)
                    self.advance()

                    # check for string
                    while(self.current_token.type in {'STRING', 'ID', 'INT', 'FLOAT'}):
                        new_node = Node(self.current_token.type, self.current_token.value)
                        self.insert_end(new_node)
                        self.advance()

                        if(self.current_token.type == ')'):
                            break

                        # check for comma
                        if(self.current_token.type != ','):
                            return self.token_idx, Error('expected a string signature even if empty', self.current_token.lineno, self.current_token.index)
                            
                        new_node = Node(self.current_token.type, self.current_token.value)
                        self.insert_end(new_node)
                        self.advance()

                    # check for closing parenthesis
                    if(self.current_token.type != ')'):
                        return self.token_idx, Error('Expected closing parenthesis after console', self.current_token.lineno, self.current_token.index)
                    new_node = Node(self.current_token.type, self.current_token.value)
                    self.insert_end(new_node)
                    self.advance()

                    # expect semicolon
                    if(self.current_token.type != ';'):
                        return self.token_idx, Error('Semicolon expected after console which returns nothing', self.current_token.lineno, self.current_token.index)
                
                elif(self.current_token.type == 'INBUILT'):
                    new_node = Node(self.current_token.type, self.current_token.value)
                    self.insert_end(new_node)
                    self.advance()

                    # check for parameters
                    err = self.parameters()
                    if(err != None):
                        return err
                    self.advance()

                    # expect semicolon
                    if(self.current_token.type != ';'):
                        return self.token_idx, Error('Inbuilt functions should be called individually or put semicolon', self.current_token.lineno, self.current_token.index)
                
                else:
                    # expression statement
                    err = self.expr()
                    if(err != None):
                        return err 
                    
            self.line_break()
            self.advance()
        
        if(not self.top_level):
            return self.token_idx, self.head
        if(self.top_level and self.token_idx >= len(tokens)):
            return self.token_idx, self.head
        return self.token_idx, Error(f'Unxpected character',  self.current_token.lineno, '}')

class GameParser:
    def __init__(self):
        pass
    
    def parse(self, token_stream):
        global tokens
        tokens = token_stream
        
        global tokentypes
        tokentypes = TokenTypes()

        syntax_tree = ast(-1, True)
        _, tree = syntax_tree.code()
        return tree