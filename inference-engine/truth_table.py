# truth_table.py
from parser import Symbol, Not, And, Or, Imply, Biconditional

# Evaluate the truth value of a logical expression based on a model (symbol assignments)
def evaluate(expr, model):
    """
    Recursively evaluates the truth value of the expression 'expr'
    under the given model (dictionary of symbol: truth_value).
    """
    if isinstance(expr, Symbol):
        return model.get(expr.name, False)  # Look up truth value of the symbol in the model
    elif isinstance(expr, Not):
        return not evaluate(expr.operand, model)  # Evaluate negation
    elif isinstance(expr, And):
        return evaluate(expr.left, model) and evaluate(expr.right, model)  # Evaluate A & B
    elif isinstance(expr, Or):
        return evaluate(expr.left, model) or evaluate(expr.right, model)  # Evaluate A || B
    elif isinstance(expr, Imply):
        return (not evaluate(expr.left, model)) or evaluate(expr.right, model)  # A => B is (¬A ∨ B)
    elif isinstance(expr, Biconditional):
        return evaluate(expr.left, model) == evaluate(expr.right, model)  # A <=> B is true when A and B are equal
    else:
        raise ValueError(f"Unknown expression type: {expr}")

# Collect all symbols used in a formula recursively
def get_symbols(expr, symbols_set):
    """
    Recursively collect all unique symbol names used in the expression 'expr'.
    Adds them to the provided set 'symbols_set'.
    """
    if isinstance(expr, Symbol):
        symbols_set.add(expr.name)
    elif isinstance(expr, Not):
        get_symbols(expr.operand, symbols_set)
    elif isinstance(expr, (And, Or, Imply, Biconditional)):
        get_symbols(expr.left, symbols_set)
        get_symbols(expr.right, symbols_set)
    return symbols_set

# Main truth table entailment checker
def tt_entails(KB, query):
    """
    Determine whether the knowledge base (KB) entails the query using truth-table checking.
    KB: list of expressions (formulas)
    query: the query expression to check
    Returns: (entailed: bool, model_count: int)
    """
    # Collect all symbols from KB and the query into a list
    symbols = set()
    for clause in KB:
        get_symbols(clause, symbols)
    get_symbols(query, symbols)
    symbols = list(symbols)

    # If no symbols exist, evaluate once using empty model
    if not symbols:
        kb_true = all(evaluate(clause, {}) for clause in KB)
        query_true = evaluate(query, {})
        if kb_true and query_true:
            return True, 1
        else:
            return False, 0

    from itertools import product  # Used to enumerate all truth assignments

    model_count = 0     # Count how many models satisfy the KB
    entails = True      # Will become False if one model satisfies KB but falsifies query
    n = len(symbols)    # Total number of distinct propositional symbols

    # Iterate through every possible truth assignment (2^n models)
    for values in product([False, True], repeat=n):
        model = {symbols[i]: values[i] for i in range(n)}

        # If this model satisfies all formulas in KB
        if all(evaluate(clause, model) for clause in KB):
            model_count += 1
            # Check if query is also true in this model
            if not evaluate(query, model):
                entails = False  # Found a counterexample, so entailment fails

    # If no model satisfies the KB, entailment is vacuously true
    if model_count == 0:
        return True, 0

    return entails, model_count  # Return result and how many models satisfied KB
