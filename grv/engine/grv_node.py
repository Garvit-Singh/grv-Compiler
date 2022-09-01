from multiprocessing.sharedctypes import Value


class Node:
    def __init__(self, type, value, below=None, next=None):
        self.type = type
        self.value = value 
        self.below = below
        self.next = next
