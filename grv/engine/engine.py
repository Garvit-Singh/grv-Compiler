import sys
from grv_error import Error
from grv_lexer import GameLexer
from grv_parser import GameParser
from grv_constant import Constant

def traverse(ast, level):
    
    s = ''
    t = ''
    for _ in range(level):
        t += '\t'

    root = ast
    while(root != None):
        if(root.type == 'EMPTY' or root.type == 'NEWLINE'):
            s += '\n' + t 
        else: 
            s += root.value + ' '
        if(root.below != None):
            s += traverse(root.below, level+1)
        root = root.next
    return s

if __name__ == '__main__':

    lexer = GameLexer()
    parser = GameParser()
    constants = Constant()

    n = len(sys.argv)

    if(n != 3):
        f = open(sys.argv[1], 'r')
        source_code = f.read()
        f.close()

        tokens = lexer.tokenize(source_code)

        token_stream = []
        for tok in tokens:
            if(isinstance(tok, Error)):
                print(tok.__repr__())
                quit()
            token_stream.append(tok)
            # print(tok.__repr__())
        
        # make abstract syntax tree
        ast = parser.parse(token_stream)

        if(isinstance(ast, Error)):
            print(ast.__repr__())
            quit()

        # traverse and write the code
        dest_code = traverse(ast, 0)

        # import the inbuilt library
        dest_code = constants.get_files() + dest_code

        # write to the python file
        f = open(constants.get_directory() + constants.get_filename(), 'w')
        f.write(dest_code)
        f.close()

        pass
    else:
        print('Invalid Amount of Arguments!')
        pass
