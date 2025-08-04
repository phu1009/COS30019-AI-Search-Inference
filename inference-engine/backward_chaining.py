# backward_chaining.py
from parser import Symbol, Imply, And

# Backward Chaining Inference Algorithm
# This method works for Horn-form knowledge bases only

def backward_chain(KB_AST, query):
    """
    Implements backward chaining for Horn clauses.
    Args:
        KB_AST: list of AST expressions representing the knowledge base.
        query: symbol name to prove (string).
    Returns:
        (entailed_list, entails_boolean): List of symbols inferred during the proof and whether the query is entailed.
    """
    facts = set()    # Atomic known facts (like "a", "b")
    rules = []       # List of rules in form (premises, conclusion)

    # Step 1: Parse KB and separate facts from Horn rules
    for clause in KB_AST:
        if isinstance(clause, Symbol):
            # Atomic fact, add to known set
            facts.add(clause.name)

        elif isinstance(clause, Imply):
            # Rule: premise => conclusion (Horn clause)
            if isinstance(clause.right, Symbol):
                conclusion = clause.right.name
            else:
                continue  # Skip invalid rules

            left = clause.left
            premises = []

            def get_conjuncts(expr):
                # Recursively extract all conjuncts in A & B & C
                if isinstance(expr, And):
                    return get_conjuncts(expr.left) + get_conjuncts(expr.right)
                elif isinstance(expr, Symbol):
                    return [expr.name]
                else:
                    return []

            if isinstance(left, Symbol):
                premises = [left.name]  # Single condition
            else:
                premises = get_conjuncts(left)

            rules.append((premises, conclusion))

    visited = set()     # Prevent infinite recursion due to cycles
    entailed = []       # Track all symbols proven during reasoning

    # Recursive backward chaining procedure
    def bc_prove(symbol):
        if symbol in entailed:
            return True  # Already proven

        if symbol in facts:
            # Known fact, add to entailed list
            if symbol not in entailed:
                entailed.append(symbol)
            return True

        if symbol in visited:
            return False  # Already visited, avoid infinite loop

        visited.add(symbol)  # Mark this symbol as being processed

        # Try all rules that conclude this symbol
        for premises, conclusion in rules:
            if conclusion != symbol:
                continue

            # Try to prove all premises
            if all(bc_prove(p) for p in premises):
                if symbol not in entailed:
                    entailed.append(symbol)
                return True

        return False  # No rule could prove this symbol

    entails = bc_prove(query)  # Start proof from the query symbol

    return entailed, entails
