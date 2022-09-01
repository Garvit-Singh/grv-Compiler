from engine.grv_constant import Constant

constants = Constant()

while True:
    text = input('grv> ')
    
    if(text == 'quit()'):
        break
    
    f = open(constants.get_shell_file(), 'w')
    f.write(text)
    f.close()
