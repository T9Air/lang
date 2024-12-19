import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_program(source_code):
    # Create lexer instance
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    # return tokens
    
    # Create parser instance
    parser = Parser(tokens)
    ast = parser.parse()
    # return ast
    
    # Create interpreter instance
    interpreter = Interpreter(ast)
    result = interpreter.interpret()
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename.enl>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.enl'):
        print("Error: File must have .enl extension")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Processing {filename}...")
            result = run_program(content)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()