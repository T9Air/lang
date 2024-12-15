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

    def error(self):
        raise Exception(f'Invalid character: {self.current_char}')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

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
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def tokenize(self):
        tokens = []
        operator_count = 0

        while self.current_char:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                tokens.append(Token('NUMBER', self.get_number()))
                continue

            if self.current_char.isalpha():
                identifier = self.get_identifier()
                if identifier in ['plus', 'minus', 'times', 'divide']:
                    operator_count += 1
                    if operator_count > 1:
                        raise Exception('Only one operator allowed per line')
                    
                    if identifier == 'plus':
                        tokens.append(Token('OPERATOR', "+"))
                    elif identifier == 'minus':
                        tokens.append(Token('OPERATOR', "-"))
                    elif identifier == 'times':
                        tokens.append(Token('OPERATOR', "*"))
                    elif identifier == 'divide':
                        tokens.append(Token('OPERATOR', "/"))
                continue

            self.error()

        return tokens

test_inputs = [
    "9 plus 2.798"
]

# for input_text in test_inputs:
#     print(f"\nInput: {input_text}")
#     lexer = Lexer(input_text)
#     try:
#         tokens = lexer.tokenize()
#         print("Tokens:", tokens)
#     except Exception as e:
#         print("Error:", str(e))