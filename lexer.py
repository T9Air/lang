class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
        self.line = 1
        self.column = 1
        self.indent_level = 0

    def error(self):
        raise Exception(f'Invalid character "{self.current_char}" at line {self.line}, column {self.column}')

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
                self.advance()
                return Token('NEWLINE', '\n')
            self.advance()
        return None

    def get_number(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()
                
        return float(result)

    def get_identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_' or self.current_char == '\"'):
            result += self.current_char
            self.advance()
        return result

    def tokenize(self):
        tokens = []
        operator_count = 0

        while self.current_char:
            
            if self.current_char.isspace() and self.current_char != '\n':
                spaces = 0
                while self.current_char and self.current_char.isspace():
                    spaces += 1
                    self.advance()
                if self.column == spaces + 1:
                    self.indent_level = spaces // 4
                    if self.indent_level.is_integer() and self.indent_level > 0:
                        tokens.append(Token('INDENT', self.indent_level))

            if self.current_char.isspace():
                newline_token = self.skip_whitespace()
                if newline_token:
                    tokens.append(newline_token)
                    operator_count = 0  # Reset operator count on new line
                continue

            if self.current_char.isdigit():
                tokens.append(Token('NUMBER', self.get_number()))
                continue

            if self.current_char.isalpha():
                identifier = self.get_identifier()
                if identifier in ['plus', 'minus', 'times', 'divide']:
                    operator_count += 1
                    if operator_count > 1:
                        raise Exception(f'Syntax Error: Only one operator allowed per line (line {self.line}, column {self.column})')
                    
                    if identifier == 'plus':
                        tokens.append(Token('OPERATOR', "+"))
                    elif identifier == 'minus':
                        tokens.append(Token('OPERATOR', "-"))
                    elif identifier == 'times':
                        tokens.append(Token('OPERATOR', "*"))
                    elif identifier == 'divide':
                        tokens.append(Token('OPERATOR', "/"))
                elif identifier == 'output':
                    tokens.append(Token('KEYWORD', 'print'))
                    self.skip_whitespace()
                    start_pos = self.pos
                    if self.current_char == '\"':
                        output = ''
                        self.advance() 
                        while self.current_char != '\"':
                            if self.current_char == ' ':
                                output += ' '
                                self.advance()
                            else:
                                output += self.current_char
                                self.advance()
                        self.advance()
                        tokens.append(Token('STRING', output))
                    elif self.current_char.isdigit():
                        output = self.get_number()
                        tokens.append(Token('NUMBER', output))
                elif identifier == 'input':
                    tokens.append(Token('KEYWORD', 'input'))
                elif identifier == 'is':
                    self.skip_whitespace()
                    start_pos = self.pos
                    next_identifier = self.get_identifier()
                    if next_identifier == 'now':
                        tokens.append(Token('ASSIGN', '='))
                    else:
                        self.pos = start_pos
                        self.current_char = self.text[self.pos]
                        raise Exception(f'Syntax Error: Expected "now" after "is" at line {self.line}, column {self.column}')
                elif identifier == 'if':
                    tokens.append(Token('KEYWORD', 'if'))
                    self.skip_whitespace()
                    start_pos = self.pos
                    if self.current_char.isdigit():
                        number = self.get_number()
                        tokens.append(Token('NUMBER', number))
                    elif self.current_char.isalpha():
                        identifier = self.get_identifier()
                        tokens.append(Token('IDENTIFIER', identifier))
                    else:
                        self.pos = start_pos
                        self.current_char = self.text[self.pos]
                        raise Exception(f'Syntax Error: Expected number or identifier after "if" at line {self.line}, column {self.column}')
                    self.skip_whitespace()
                    identifier = self.get_identifier()
                    if identifier == 'equals':
                        tokens.append(Token('COMPARISON', '=='))
                    elif identifier == 'is':
                        self.advance()
                        identifier = self.get_identifier()
                        if identifier == 'not':
                            tokens.append(Token('COMPARISON', '!='))
                        elif identifier == 'greater':
                            self.advance()
                            identifier = self.get_identifier()
                            if identifier == 'than':
                                tokens.append(Token('COMPARISON', '>'))
                            else:
                                self.pos = start_pos
                                self.current_char = self.text[self.pos]
                                raise Exception(f'Syntax Error: Expected "than" after "greater" at line {self.line}, column {self.column}')
                        elif identifier == 'less':
                            self.advance()
                            identifier = self.get_identifier()
                            if identifier == 'than':
                                tokens.append(Token('COMPARISON', '<'))
                            else:
                                self.pos = start_pos
                                self.current_char = self.text[self.pos]
                                raise Exception(f'Syntax Error: Expected "than" after "less" at line {self.line}, column {self.column}')
                    else:
                        self.pos = start_pos
                        self.current_char = self.text[self.pos]
                        raise Exception(f'Syntax Error: Expected comparator after number or identifier at line {self.line}, column {self.column}')
                    self.skip_whitespace()
                    if self.current_char.isdigit():
                        number = self.get_number()
                        tokens.append(Token('NUMBER', number))
                    elif self.current_char.isalpha():
                        identifier = self.get_identifier()
                        tokens.append(Token('IDENTIFIER', identifier))
                    else:
                        self.pos = start_pos
                        self.current_char = self.text[self.pos]
                        raise Exception(f'Syntax Error: Expected number or identifier after operator at line {self.line}, column {self.column}')
                elif identifier == 'otherwise':
                    tokens.append(Token('KEYWORD', 'else'))
                else:
                    tokens.append(Token('IDENTIFIER', identifier))
                continue

            self.error()

        return tokens

test_inputs = [
    # 'x is now input',
]

for input_text in test_inputs:
    print(f"\nInput: {input_text}")
    lexer = Lexer(input_text)
    try:
        tokens = lexer.tokenize()
        print("Tokens:", tokens)
    except Exception as e:
        print("Error:", str(e))