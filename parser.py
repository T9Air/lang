from lexer import Token, Lexer

class AST:
    pass

class Statement(AST):
    def __init__(self, statements):
        self.statements = statements
    
    def __str__(self):
        return "\n".join(str(stmt) for stmt in self.statements)
    
    def __repr__(self):
        return self.__str__()

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self):
        return f"BinOp:\n  left: {self.left}\n  op: {self.op}\n  right: {self.right}"
    
    def __repr__(self):
        return self.__str__()
    
class Keyword(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"KeywordOP:\n  value: {self.value}"
    
    def __repr__(self):
        return self.__str__()

class Assign(AST):
    def __init__(self, name, value):
        self.name = name
        if name.isdecimal():
            raise Exception(f"Syntax Error: Invalid variable name '{name}'. Variable names must start with a letter.")
        self.value = value
    
    def __str__(self):
        return f"AssignOP:\n  name: {self.name}\n  value: {self.value}"
    
    def __repr__(self):
        return self.__str__()

class Number(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"Number({self.value})"
    
    def __repr__(self):
        return self.__str__()
    
class String(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"String({self.value})"
    
    def __repr__(self):
        return self.__str__()

class Variable(AST):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"Variable({self.name})"
    
    def __repr__(self):
        return self.__str__()

class Print(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"PrintOP:\n  value: {self.value}"
    
    def __repr__(self):
        return self.__str__()

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self):
        token = self.current_token
        token_str = f"'{token.value}'" if token else "end of input"
        raise Exception(f'Syntax Error: Unexpected {token_str} at position {self.pos}')
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.tokens) - 1:
            self.current_token = None
        else:
            self.current_token = self.tokens[self.pos]
    
    def parse(self):
        statements = []
        while self.current_token:
            if self.current_token.type == 'NEWLINE':
                self.advance()
                continue
            stmt = self.expr()
            if stmt:
                statements.append(stmt)
            # Skip any trailing newlines after statement
            while self.current_token and self.current_token.type == 'NEWLINE':
                self.advance()
        return Statement(statements)
    
    def expr(self):
        left = self.term()
        
        if isinstance(left, Keyword) and left.value == 'print':
            if self.current_token and self.current_token.type == 'STRING':
                right = self.term()
                left = Print(right)
            else:
                self.error()
        
        elif self.current_token:
            if self.current_token.type == 'OPERATOR':
                op = self.current_token.value
                self.advance()
                right = self.term()
                left = BinOp(left, op, right)
            
                # Allow newline or None after expression
                if self.current_token and self.current_token.type != 'NEWLINE':
                    self.error()
            elif self.current_token.type == 'ASSIGN':
                if not isinstance(left, Variable):
                    raise Exception("Can only assign to variables")
                self.advance()
                right = self.term()
                left = Assign(left.name, right)
            
                # Allow newline or None after assignment
                if self.current_token and self.current_token.type != 'NEWLINE':
                    self.error()
            elif self.current_token.type == 'KEYWORD':
                op = self.current_token.value
                if op == 'print':
                    self.advance()
                    right = self.term()
                    left = Print(right)
            
                # Allow newline or None after output
                if self.current_token and self.current_token.type != 'NEWLINE':
                    self.error()
            elif self.current_token.type == 'STRING':
                self.error()
        
        return left
    
    def term(self):
        if not self.current_token:
            self.error()
            
        if self.current_token.type == 'NUMBER':
            token = self.current_token
            self.advance()
            return Number(token.value)
        elif self.current_token.type == 'IDENTIFIER':
            token = self.current_token
            self.advance()
            return Variable(token.value)
        elif self.current_token.type == 'KEYWORD':
            token = self.current_token
            self.advance()
            return Keyword(token.value)
        elif self.current_token.type == 'STRING':
            token = self.current_token
            self.advance()
            return String(token.value)
        else:
            self.error()

if __name__ == '__main__':
    test_inputs = [
        "output \"Hello, World!\""
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