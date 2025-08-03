# inference_research.py
# Research version of the propositional logic inference engine
# Supports: Truth Table (TT) and DPLL inference methods
# This version is designed for research comparison, modular structure, and CNF transformation

import sys, argparse, time, re
from functools import reduce

# --- AST classes for propositional logic expressions ---
# Each expression is a tree node: Symbol, Not, And, Or, Imply
class Expr: pass

class Symbol(Expr):
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name

class Not(Expr):
    def __init__(self, child): self.child = child
    def __repr__(self): return f"~{self.child}"

class And(Expr):
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"({self.left} & {self.right})"

class Or(Expr):
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"({self.left} | {self.right})"

class Imply(Expr):
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"({self.left} -> {self.right})"

# --- Parser ---
# Converts a formula string into an expression tree (AST)
def tokenize(s):
    # Replace alternate logical symbols and remove whitespace
    s = s.replace('=>','->').replace('→','->')
    s = s.replace('¬','~').replace('∧','&').replace('∨','|')
    s = s.replace('||','|'); s = re.sub(r'\s+','',s)
    tokens, i = [], 0
    while i < len(s):
        if s[i].isalnum() or s[i]=='_':
            j = i
            while j < len(s) and (s[j].isalnum() or s[j]=='_'):
                j += 1
            tokens.append(s[i:j]); i = j
        elif s[i:i+2] == '->': tokens.append('->'); i += 2
        elif s[i] in '~&|()': tokens.append(s[i]); i += 1
        else: raise ValueError(f"Bad char: {s[i]}")
    return tokens

def parse_expr(tokens):
    # Recursive descent parser following operator precedence: ~ > & > | > ->
    def parse_imp():
        node = parse_or()
        if tokens and tokens[0] == '->': tokens.pop(0); node = Imply(node, parse_imp())
        return node
    def parse_or():
        node = parse_and()
        while tokens and tokens[0] == '|': tokens.pop(0); node = Or(node, parse_and())
        return node
    def parse_and():
        node = parse_not()
        while tokens and tokens[0] == '&': tokens.pop(0); node = And(node, parse_not())
        return node
    def parse_not():
        if tokens[0] == '~': tokens.pop(0); return Not(parse_not())
        return parse_atom()
    def parse_atom():
        if tokens[0] == '(':
            tokens.pop(0)
            node = parse_imp()
            if not tokens or tokens[0] != ')':
                raise ValueError("Missing )")
            tokens.pop(0)
            return node
        else:
            sym = tokens.pop(0)
            return Symbol(sym)
    return parse_imp()

def parse_formula(s): return parse_expr(tokenize(s))

# --- Truth Table Evaluation ---
def tt_entails(kb, query):
    # Check if KB entails query using truth-table (brute force)
    symbols = set()
    def collect(e):
        if isinstance(e, Symbol): symbols.add(e.name)
        elif isinstance(e, Not): collect(e.child)
        elif isinstance(e, (And, Or, Imply)): collect(e.left); collect(e.right)
    for e in kb + [query]: collect(e)
    symbols = sorted(symbols); model_count = 0
    for bits in range(1 << len(symbols)):
        model = {symbols[i]: bool((bits >> i) & 1) for i in range(len(symbols))}
        def eval_expr(e):
            if isinstance(e, Symbol): return model[e.name]
            if isinstance(e, Not): return not eval_expr(e.child)
            if isinstance(e, And): return eval_expr(e.left) and eval_expr(e.right)
            if isinstance(e, Or): return eval_expr(e.left) or eval_expr(e.right)
            if isinstance(e, Imply): return (not eval_expr(e.left)) or eval_expr(e.right)
        if all(eval_expr(e) for e in kb):
            model_count += 1
            if not eval_expr(query): return False, model_count
    return True, model_count

# --- DPLL ---
# Convert formulas to CNF using rewriting

def to_cnf(expr):
    if isinstance(expr, Imply): return to_cnf(Or(Not(expr.left), expr.right))
    if isinstance(expr, Not):
        child = expr.child
        if isinstance(child, Not): return to_cnf(child.child)
        if isinstance(child, And): return to_cnf(Or(Not(child.left), Not(child.right)))
        if isinstance(child, Or): return to_cnf(And(Not(child.left), Not(child.right)))
        return Not(to_cnf(child))
    if isinstance(expr, And): return And(to_cnf(expr.left), to_cnf(expr.right))
    if isinstance(expr, Or):
        a, b = to_cnf(expr.left), to_cnf(expr.right)
        if isinstance(a, And): return And(to_cnf(Or(a.left, b)), to_cnf(Or(a.right, b)))
        if isinstance(b, And): return And(to_cnf(Or(a, b.left)), to_cnf(Or(a, b.right)))
        return Or(a, b)
    return expr

# Flatten CNF into clause list: [[A, ~B], [~C]]
def flatten_cnf(expr):
    clauses = []
    def gather(e):
        if isinstance(e, And): gather(e.left); gather(e.right)
        elif isinstance(e, Or):
            def flat(o): return flat(o.left) + flat(o.right) if isinstance(o, Or) else [o]
            clauses.append(flat(e))
        else: clauses.append([e])
    gather(expr); return clauses

# DPLL SAT solver
def dpll(clauses, assignment={}):
    def val(lit):
        if isinstance(lit, Symbol): return assignment.get(lit.name)
        if isinstance(lit, Not): return not assignment.get(lit.child.name)
    def clause_val(c):
        v = [val(l) for l in c]
        if any(x is True for x in v): return True
        if all(x is False for x in v): return False
        return None
    # Unit propagation
    while True:
        unit = None
        for c in clauses:
            v = [val(l) for l in c]
            if v.count(None) == 1 and all(x is False for x in v if x is not None):
                unit = c[v.index(None)]; break
        if unit is None: break
        name = unit.name if isinstance(unit, Symbol) else unit.child.name
        val0 = True if isinstance(unit, Symbol) else False
        assignment[name] = val0
    # Terminal case: all true
    if all(clause_val(c) == True for c in clauses): return True
    if any(clause_val(c) == False for c in clauses): return False
    # Recursive choice
    for c in clauses:
        for lit in c:
            name = lit.name if isinstance(lit, Symbol) else lit.child.name
            if name not in assignment:
                for val0 in [True, False]:
                    assignment[name] = val0
                    if dpll(clauses, dict(assignment)): return True
                return False
    return True

# --- File Parsing and CLI ---
def parse_kb_file(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    tell_idx = lines.index('TELL'); ask_idx = lines.index('ASK')
    kb_lines = lines[tell_idx+1:ask_idx]; ask_line = lines[ask_idx+1]
    kb = [parse_formula(x) for line in kb_lines for x in line.split(';') if x.strip()]
    return kb, parse_formula(ask_line)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file'); parser.add_argument('method')
    args = parser.parse_args()
    kb, query = parse_kb_file(args.file)
    t0 = time.time()
    if args.method == 'TT':
        result, count = tt_entails(kb, query)
        print(f"YES: {count}" if result else "NO")
    elif args.method == 'DPLL':
        combined = reduce(lambda a, b: And(a, b), kb)
        conj = And(combined, Not(query))
        clauses = flatten_cnf(to_cnf(conj))
        result = not dpll(clauses)
        print("YES" if result else "NO")
    else:
        print("Method not implemented in research version.")
    print(f"Time: {time.time()-t0:.4f}s")

if __name__ == '__main__':
    main()
