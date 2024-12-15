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
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
    
    def visit_Number(self, node):
        return node.value
    
    def visit_Variable(self, node):
        return self.variables.get(node.name, 0)
    
    def visit_Assign(self, node):
        self.variables[node.name] = self.visit(node.value)
        return self.variables[node.name]
