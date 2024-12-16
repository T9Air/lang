class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def interpret(self):
        return self.visit(self.ast)
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.visit_unknown)
        return visitor(node)
    
    def visit_unknown(self, node):
        raise Exception(f'Runtime Error: Unsupported operation {type(node).__name__}')
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        try:
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise Exception('Runtime Error: Division by zero')
                return left / right
        except TypeError:
            raise Exception(f'Runtime Error: Invalid operation {left} {node.op} {right}')
    
    def visit_Number(self, node):
        return node.value
    
    def visit_Variable(self, node):
        if node.name not in self.variables:
            raise Exception(f'Runtime Error: Variable "{node.name}" is not defined')
        return self.variables[node.name]
    
    def visit_Assign(self, node):
        self.variables[node.name] = self.visit(node.value)
        return self.variables[node.name]
    
    def visit_Print(self, node):
        value = self.visit(node.value)
        print(value)
        
    def visit_str(self, node):
        return node

    def visit_Statement(self, node):
        result = None
        for statement in node.statements:
            result = self.visit(statement)
        return result
