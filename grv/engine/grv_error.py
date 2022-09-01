class Error:
    def __init__(self, error_type, error_detials, error_value):
        self.error_type = error_type
        self.error_details = error_detials
        self.error_value = error_value
    
    def __repr__(self):
        return f'{self.error_type} at line Number {self.error_details} {self.error_value}'