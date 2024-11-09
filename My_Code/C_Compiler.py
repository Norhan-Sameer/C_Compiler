#Lexical Analyzer
import re
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):       
         return f"Token({self.type}, {self.value})"
def lex(source_code):
    token_specification = [      
        ('INT', r'\bint\b'),     
        ('RETURN', r'\breturn\b'),     
        ('NUMBER', r'\b\d+\b'), 
        ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),       
        ('LBRACE', r'\{'),     
        ('RBRACE', r'\}'),        
        ('LPAREN', r'\('),        
        ('RPAREN', r'\)'),      
        ('SEMICOLON', r';'),       
        ('WHITESPACE', r'\s+'),
    ]

    # Compile the regex pattern with named groups  
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification) 
    get_token = re.compile(tok_regex).match

    tokens = []
    pos = 0 
    while pos < len(source_code):       
        match = get_token(source_code, pos)      
        if not match:          
            raise SyntaxError (f"Unexpected character: {source_code[pos]}")
        pos = match.end()      
        token_type = match.lastgroup        
        if token_type != 'WHITESPACE':            
            tokens.append(Token(token_type, match.group(0)))  
    return tokens


#Parsing (Syntax Analysis)
class ASTNode:
    pass
class FunctionDeclaration(ASTNode):   
    def __init__(self, name, body):     
        self.name = name     
        self.body = body
class ReturnStatement(ASTNode):  
    def __init__(self, value):        
        self.value = value
def parse(tokens):  
    def consume(expected_type):  
        token = tokens.pop(0)   
        if token.type != expected_type:        
            raise SyntaxError(f"Expected {expected_type}, got {token.type}")
        return token  
    consume('INT')  
    func_name = consume('IDENTIFIER').value
    consume('LPAREN')
    consume('RPAREN')    
    consume('LBRACE')    
    return_stmt = parse_return_statement(tokens, consume)   
    consume('RBRACE')  
    return FunctionDeclaration(func_name, return_stmt)
def parse_return_statement(tokens, consume):  
    consume('RETURN')
    value = int(consume('NUMBER').value)  
    consume('SEMICOLON')
    return ReturnStatement(value)


# semantic Analyzer
def semantic_check(ast):   
    if isinstance(ast, FunctionDeclaration) and ast.name == "main":      
        if isinstance(ast.body, ReturnStatement) and isinstance(ast.body.value, int):           
            return True 
    raise TypeError("Semantic error: main must return an integer")


# ir_generator
class IR:    
    def __init__(self, instructions):       
        self.instructions = instructions
def generate_ir(ast):    
    if isinstance(ast, FunctionDeclaration) and ast.name == "main":
        instructions = [f"LOAD_CONST {ast.body.value}", "RETURN" ]
        return IR(instructions)


# Code Generator
def generate_code(ir):  
    assembly = []    
    for instr in ir.instructions:   
        if instr.startswith("LOAD_CONST"):          
            _, value = instr.split()       
            assembly.append(f"mov rax, {value}")   
        elif instr == "RETURN":        
            assembly.append("ret")   
    return "\n".join(assembly)


# Main Function
def main(): 
    source_code = """  
    int main() {      
        return 42;   
    } 
    """
    
    # Step 1: Lexical Analysis  
    tokens = lex(source_code)   
    print("Tokens:", tokens)   
    print('\n')
    
    # Step 2: Parsing  
    ast = parse(tokens)   
    print("AST:", ast)    
    print('\n')
       
    # Step 3: Semantic Analysis   
    if semantic_check(ast):       
        print("Semantic check passed.")       
        print('\n')  
        
    # Step 4: IR Generation  
    ir = generate_ir(ast)   
    print("IR:", ir.instructions)  
    print('\n')  
      
    # Step 5: Code Generation 
    assembly_code = generate_code(ir)
    print("Assembly code:\n", assembly_code)  
    print('\n')
    
if __name__ == "__main__":
    main()