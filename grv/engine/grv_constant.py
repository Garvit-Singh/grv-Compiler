class Constant:
    def __init__(self):
        self.output_directory = './grv/bin/'
        self.import_files = 'from tetris import *\n'
        self.filename = 'out.py'
        self.shell_file = './grv/shell_out.grv'
        pass

    def get_files(self):
        return f'{self.import_files}'

    def get_directory(self):
        return f'{self.output_directory}'

    def get_filename(self):
        return f'{self.filename}'

    def get_shell_file(self):
        return f'{self.shell_file}'