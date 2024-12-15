# Basic structure you might start with
class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        
    def tokenize(self):
        # Convert source code into tokens
        pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        
    def parse(self):
        # Convert tokens into AST
        pass

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        
    def interpret(self):
        # Execute the AST
        pass
