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
    
    def visit_If(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '>':
            return left > right
        elif node.op == '<':
            return left < right
    
    def visit_Else(self, node):
        self.visit(node.body)
    
    def visit_IfBlock(self, node):
        condition = self.visit(node.condition)
        if condition:
            self.visit(node.body)
        else:
            if node.else_body:
                self.visit(node.else_body)
          
    def visit_ForBlock(self, node):
        count = self.visit(node.count)
        for _ in range(int(count)):
            self.visit(node.body)

    def visit_WhileBlock(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        while True:
            if op == '==':
                if left == right:
                    break
            elif op == '!=':
                if left != right:
                    break
            elif op == '>':
                if left > right:
                    break
            elif op == '<':
                if left < right:
                    break
            elif op == '>=':
                if left >= right:
                    break
            elif op == '<=':
                if left <= right:
                    break
            self.visit(node.body)
            left = self.visit(node.left)
            right = self.visit(node.right)
            
    def visit_Number(self, node):
        return node.value
    
    def visit_Variable(self, node):
        if node.name not in self.variables:
            raise Exception(f'Runtime Error: Variable "{node.name}" is not defined')
        return self.variables[node.name]
    
    def visit_Assign(self, node):
        self.variables[node.name] = self.visit(node.value)
    
    def visit_Input(self, node):
        input_value = input(f"Input value for {node.var_name}: ")
        if input_value.isdigit():
            return float(input_value)
        else:
            return input_value
    
    def visit_Print(self, node):
        value = self.visit(node.value)
        print(value)
        
    def visit_str(self, node):
        return node
    
    def visit_String(self, node):
        return node.value

    def visit_Statement(self, node):
        for statement in node.statements:
            self.visit(statement)
