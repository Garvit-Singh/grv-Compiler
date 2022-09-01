class Token:
    def __init__(self, lineno, index, type, value):
        self.lineno = lineno
        self.index = index
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f'[type: \'{self.type}\', value: \'{self.value}\', line {self.lineno}, index {self.index}]'