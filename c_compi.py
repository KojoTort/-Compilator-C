import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        print("Tokenizing...")
        patterns = [
            (r'\b(int|char|void|if|else|while|for|switch|case|default|break|continue|return)\b', 'KEYWORD'),
            (r'[a-zA-Z_][a-zA-Z_0-9]*', 'IDENTIFIER'),
            (r'\d+', 'LITERAL'),
            (r'[(){}\[\];,\.]', 'SYMBOL'),
            (r'[+\-*/%=<>!&|^~]', 'OPERATOR'),
            (r'\s+', 'WHITESPACE'),  # added whitespace pattern
        ]

        for pattern, token_type in patterns:
            print(f"Matching pattern: {pattern}")
            for match in re.finditer(pattern, self.source_code, re.MULTILINE):
                token = match.group()
                print(f"Found token: {token} ({token_type})")
                if token_type!= 'WHITESPACE':
                    if token_type == 'LITERAL':
                        self.tokens.append({'type': token_type, 'value': int(token)})
                    else:
                        self.tokens.append({'type': token_type, 'value': token})

        print("Tokenization complete!")
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ast = {}

    def parse(self):
        self.ast = self.program()

    def program(self):
        declarations = []
        while self.tokens:
            declaration = self.declaration()
            if declaration:
                declarations.append(declaration)
            else:
                break
        return {'type': 'PROGRAM', 'declarations': declarations}

    def declaration(self):
        if self.tokens[0]['type'] == 'KEYWORD' and self.tokens[0]['value'] in ['int', 'char']:
            type_specifier = self.tokens.pop(0)
            identifier = self.tokens.pop(0)
            if self.tokens[0]['type'] == 'SYMBOL' and self.tokens[0]['value'] == ';':
                self.tokens.pop(0)
                return {'type': 'DECLARATION', 'type_specifier': type_specifier, 'identifier': identifier}
        return None

    def statement(self):
        if self.tokens[0]['type'] == 'KEYWORD' and self.tokens[0]['value'] == 'if':
            if_token = self.tokens.pop(0)
            expression = self.expression()
            if self.tokens[0]['type'] == 'SYMBOL' and self.tokens[0]['value'] == '{':
                self.tokens.pop(0)
                statements = self.statements()
                if self.tokens[0]['type'] == 'SYMBOL' and self.tokens[0]['value'] == '}':
                    self.tokens.pop(0)
                    return {'type': 'IF_STATEMENT', 'if_token': if_token, 'expression': expression, 'statements': statements}
        return None

    def expression(self):
        
        if self.tokens[0]['type'] == 'LITERAL':
            literal = self.tokens.pop(0)
            return {'type': 'LITERAL_EXPRESSION', 'value': literal}
        elif self.tokens[0]['type'] == 'IDENTIFIER':
            identifier = self.tokens.pop(0)
            return {'type': 'IDENTIFIER_EXPRESSION', 'value': identifier}
        return None

    def statements(self):
        statements = []
        while self.tokens:
            statement = self.statement()
            if statement:
                statements.append(statement)
            else:
                break
        return statements

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = ''

    def generate_code(self):
        self.code = ''
        self.generate_program(self.ast)
        return self.code

    def generate_program(self, program):
        for declaration in program['declarations']:
            self.generate_declaration(declaration)

    def generate_declaration(self, declaration):
        self.code += f"{declaration['type_specifier']['value']} {declaration['identifier']['value']};\n"

    def generate_if_statement(self, if_statement):
        self.code += f"if ({if_statement['expression']['value']}) {{\n"
        for statement in if_statement['statements']:
            self.generate_statement(statement)
        self.code += "}\n"

    def generate_statement(self, statement):
        if statement['type'] == 'IF_STATEMENT':
            self.generate_if_statement(statement)
        else:
            raise Exception(f"Unknown statement type: {statement['type']}")

def compile_c_code(source_code):
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    return tokens

source_code = """
int main() {
    int x = 10;
    return 0;
}
"""
code = compile_c_code(source_code)
print("Tokens:")
for token in code:
    print(f"Type: {token['type']}, Value: {token['value']}")