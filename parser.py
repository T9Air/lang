from lexer import Token, Lexer

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self):
        return f"BinOp:\n  left: {self.left}\n  op: {self.op}\n  right: {self.right}"
    
    def __repr__(self):
        return self.__str__()

class Number(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"Number({self.value})"
    
    def __repr__(self):
        return self.__str__()

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self):
        raise Exception('Invalid syntax')
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.tokens) - 1:
            self.current_token = None
        else:
            self.current_token = self.tokens[self.pos]
    
    def parse(self):
        return self.expr()
    
    def expr(self):
        left = self.term()
        
        if self.current_token and self.current_token.type == 'OPERATOR':
            op = self.current_token.value
            self.advance()
            right = self.term()
            left = BinOp(left, op, right)
            
            if self.current_token is not None:
                self.error()
            
        return left
    
    def term(self):
        if not self.current_token or self.current_token.type != 'NUMBER':
            self.error()
        token = self.current_token
        self.advance()
        return Number(token.value)

if __name__ == '__main__':
    test_inputs = [
        "9 plus 2.798",
        "5 minus 3",
        "10 times 4",
        "15 divide 3"
    ]
    
    for text in test_inputs:
        print(f"\nProcessing: {text}")
        try:
            # Lexical analysis
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            print("Tokens:", tokens)
            
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            print("AST:", ast)
        except Exception as e:
            print("Error:", str(e))