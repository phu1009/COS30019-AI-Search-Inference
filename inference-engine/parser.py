# parser.py

# Abstract base class for all expressions
# This will be inherited by all other logical constructs (Symbol, And, Or, etc.)
class Expr:
    pass

# Symbol represents an atomic proposition, e.g., 'a', 'p1'
class Symbol(Expr):
    def __init__(self, name):
        self.name = name  # Name of the symbol (e.g., 'a', 'rain')

    def __repr__(self):
        return f"Symbol({self.name})"

# Not represents logical negation: ~A
class Not(Expr):
    def __init__(self, operand):
        self.operand = operand  # The expression that is being negated

    def __repr__(self):
        return f"Not({self.operand})"

# And represents logical conjunction: A & B
class And(Expr):
    def __init__(self, left, right):
        self.left = left      # Left sub-expression of conjunction
        self.right = right    # Right sub-expression of conjunction

    def __repr__(self):
        return f"And({self.left}, {self.right})"

# Or represents logical disjunction: A || B
class Or(Expr):
    def __init__(self, left, right):
        self.left = left      # Left side of OR
        self.right = right    # Right side of OR

    def __repr__(self):
        return f"Or({self.left}, {self.right})"

# Imply represents logical implication: A => B
class Imply(Expr):
    def __init__(self, left, right):
        self.left = left      # Antecedent (if part)
        self.right = right    # Consequent (then part)

    def __repr__(self):
        return f"Imply({self.left}, {self.right})"

# Biconditional represents logical equivalence: A <=> B
class Biconditional(Expr):
    def __init__(self, left, right):
        self.left = left      # One side of the equivalence
        self.right = right    # Other side of the equivalence

    def __repr__(self):
        return f"Biconditional({self.left}, {self.right})"

# Recursive descent parser for propositional logic formulas
# This parser will take a string like 'a => (b & c)' and build a structured object tree
class FormulaParser:
    def __init__(self, text):
        self.text = text      # The full text input to parse
        self.pos = 0          # Current character index in the input string

    def parse(self):
        # Start parsing from the lowest precedence operator (biconditional)
        result = self.parse_equiv()
        self.skip_whitespace()
        if self.pos < len(self.text):
            raise ValueError(f"Unexpected token at position {self.pos}: '{self.text[self.pos:]}'")
        return result

    def skip_whitespace(self):
        # Skip over spaces and tabs
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def parse_equiv(self):
        # Parse biconditional expressions using <=>
        self.skip_whitespace()
        left = self.parse_imply()
        self.skip_whitespace()
        while self.text.startswith("<=>", self.pos):
            self.pos += 3
            right = self.parse_imply()
            left = Biconditional(left, right)  # Build a Biconditional expression
            self.skip_whitespace()
        return left

    def parse_imply(self):
        # Parse implication expressions using =>
        self.skip_whitespace()
        left = self.parse_or()
        self.skip_whitespace()
        if self.text.startswith("=>", self.pos):
            self.pos += 2
            right = self.parse_imply()
            return Imply(left, right)
        return left

    def parse_or(self):
        # Parse disjunctions using ||
        self.skip_whitespace()
        left = self.parse_and()
        self.skip_whitespace()
        while self.text.startswith("||", self.pos):
            self.pos += 2
            right = self.parse_and()
            left = Or(left, right)
            self.skip_whitespace()
        return left

    def parse_and(self):
        # Parse conjunctions using &
        self.skip_whitespace()
        left = self.parse_not()
        self.skip_whitespace()
        while self.pos < len(self.text) and self.text[self.pos] == '&':
            self.pos += 1
            right = self.parse_not()
            left = And(left, right)
            self.skip_whitespace()
        return left

    def parse_not(self):
        # Parse negation using ~ or move to atomic expressions
        self.skip_whitespace()
        if self.pos < len(self.text) and self.text[self.pos] == '~':
            self.pos += 1
            operand = self.parse_not()  # Apply negation to next unit
            return Not(operand)
        else:
            return self.parse_atom()

    def parse_atom(self):
        # Parse atomic propositions or parenthesized expressions
        self.skip_whitespace()
        if self.pos >= len(self.text):
            raise ValueError("Unexpected end of input in parse_atom")

        char = self.text[self.pos]

        if char == '(':  # Handle nested subexpressions in parentheses
            self.pos += 1
            expr = self.parse_equiv()
            self.skip_whitespace()
            if self.pos >= len(self.text) or self.text[self.pos] != ')':
                raise ValueError("Missing closing parenthesis")
            self.pos += 1
            return expr

        if char.isalpha():  # Handle atomic symbol like 'a', 'p1'
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isalnum():
                self.pos += 1
            name = self.text[start:self.pos]
            return Symbol(name)

        raise ValueError(f"Invalid character '{char}' at position {self.pos}")

# Convert a string formula into an AST expression using the FormulaParser class
def parse_formula(formula_str):
    parser = FormulaParser(formula_str)
    return parser.parse()

# Parse a knowledge base file with TELL and ASK
# Returns list of clause strings and query string
def parse_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != ""]  # Remove blank lines and strip whitespace

    tell_index = -1  # Index of TELL section
    ask_index = -1   # Index of ASK section

    # Identify the lines with "TELL" and "ASK"
    for i, line in enumerate(lines):
        if line.upper() == "TELL":
            tell_index = i
        elif line.upper() == "ASK":
            ask_index = i

    if tell_index == -1 or ask_index == -1:
        raise ValueError("File must contain TELL and ASK sections")

    # Collect the knowledge base lines between TELL and ASK
    kb_lines = []
    for i in range(tell_index+1, ask_index):
        kb_lines.append(lines[i])

    # Join all lines into a single string and split by semicolons to get individual clauses
    kb_text = " ".join(kb_lines)
    parts = [part.strip() for part in kb_text.split(';') if part.strip() != ""]

    # Find the query line (first non-empty line after ASK)
    query = None
    for i in range(ask_index+1, len(lines)):
        if lines[i] != "":
            query = lines[i].strip()
            break

    if query is None:
        raise ValueError("No query found after ASK")

    return parts, query
