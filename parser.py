from lexer import Token, Lexer

class AST:
    def __str__(self, indent=0):
        return '  ' * indent + self.__class__.__name__

class Statement(AST):
    def __init__(self, statements):
        self.statements = statements
    
    def __str__(self, indent=0):
        result = '  ' * indent + 'Statements:\n'
        for stmt in self.statements:
            result += stmt.__str__(indent + 1) + '\n'
        return result.rstrip()
    
    def __repr__(self):
        return self.__str__()

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self, indent=0):
        result = '  ' * indent + 'BinOp:\n'
        result += self.left.__str__(indent + 1) + '\n'
        result += '  ' * (indent + 1) + f"Operator: '{self.op}'\n"
        result += self.right.__str__(indent + 1)
        return result
    
    def __repr__(self):
        return self.__str__()
    
class Keyword(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self, indent=0):
        return '  ' * indent + f"KeywordOP:\n  value: {self.value}"
    
    def __repr__(self):
        return self.__str__()

class Assign(AST):
    def __init__(self, name, value):
        self.name = name
        if name.isdecimal():
            raise Exception(f"Syntax Error: Invalid variable name '{name}'. Variable names must start with a letter.")
        self.value = value
    
    def __str__(self, indent=0):
        result = '  ' * indent + 'Assign:\n'
        result += '  ' * (indent + 1) + f"Name: {self.name}\n"
        result += self.value.__str__(indent + 1)
        return result
    
    def __repr__(self):
        return self.__str__()

class Number(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self, indent=0):
        return '  ' * indent + f'Number({self.value})'
    
    def __repr__(self):
        return self.__str__()
    
class String(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self, indent=0):
        return '  ' * indent + f'String("{self.value}")'
    
    def __repr__(self):
        return self.__str__()

class Variable(AST):
    def __init__(self, name):
        self.name = name
    
    def __str__(self, indent=0):
        return '  ' * indent + f'Variable({self.name})'
    
    def __repr__(self):
        return self.__str__()

class Print(AST):
    def __init__(self, value):
        self.value = value
    
    def __str__(self, indent=0):
        result = '  ' * indent + 'Print:\n'
        result += self.value.__str__(indent + 1)
        return result
    
    def __repr__(self):
        return self.__str__()
    
class If(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self, indent=0):
        result = '  ' * indent + 'If:\n'
        result += self.left.__str__(indent + 1) + '\n'
        result += '  ' * (indent + 1) + f"Comparison: '{self.op}'\n"
        result += self.right.__str__(indent + 1)
        return result
    
    def __repr__(self):
        return self.__str__()

class IfBlock(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __str__(self, indent=0):
        result = '  ' * indent + 'IfBlock:\n'
        result += self.condition.__str__(indent + 1) + '\n'
        result += self.body.__str__(indent + 1)
        return result
    
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
            
    def parse_if(self):
        # Get left side of condition
        left = self.term()
        
        # Get comparison operator
        if self.current_token and self.current_token.type == 'COMPARISON':
            op = self.current_token.value
            self.advance()
            right = self.term()
            condition = If(left, op, right)
        else:
            self.error()
        
        if self.current_token and self.current_token.type == 'NEWLINE':
            self.advance()
        else:
            self.error()
            
        if self.current_token and self.current_token.type == 'INDENT':
            self.advance()
        else:
            self.error()
        
        body = []
        while self.current_token:
            if self.current_token.type == 'NEWLINE':
                self.advance()
                if self.current_token.type != 'INDENT':
                    break
                continue
            line = self.expr()
            if line:
                body.append(line)

        return IfBlock(condition, Statement(body))
    
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
        
        if isinstance(left, Keyword):
            if left.value == 'print':
                if self.current_token: 
                    if self.current_token.type == 'STRING':
                        right = self.term()
                        left = Print(right)
                    elif self.current_token.type == 'NUMBER' or self.current_token.type == 'IDENTIFIER':
                        right = self.term()
                        # Add check for None before accessing type
                        if self.current_token and self.current_token.type == 'OPERATOR':
                            op = self.current_token.value
                            self.advance()
                            next_num = self.term()
                            right = BinOp(right, op, next_num)
                        left = Print(right)
                else:
                    self.error()
            elif left.value == 'if':
                left = self.parse_if()
                
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
                if self.current_token and self.current_token.type == 'OPERATOR':
                    op = self.current_token.value
                    self.advance()
                    next_num = self.term()
                    right = BinOp(right, op, next_num)
                
                left = Assign(left.name, right)
            
                # Allow newline or None after assignment
                if self.current_token and self.current_token.type != 'NEWLINE':
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
        "if x equals 5\n    x is now 5\noutput x",
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