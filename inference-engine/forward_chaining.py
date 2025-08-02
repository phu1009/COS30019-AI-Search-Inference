# forward_chaining.py
from parser import Symbol, Imply, And

# Forward Chaining Inference Algorithm
# This method is designed for Horn-form knowledge bases only

def forward_chain(KB_AST, query):
    """
    Implements forward chaining for Horn clauses.
    Args:
        KB_AST: list of AST expressions representing the knowledge base.
        query: symbol name to check (string).
    Returns:
        (entailed_list, entails_boolean): A list of inferred symbols and whether query is entailed.
    """
    # Initialize known facts (atomic symbols) and rules (Horn implications)
    facts_list = []     # Ordered list of known facts (to maintain insertion order)
    facts_set = set()   # Set version for faster lookup
    rules = []          # List of Horn rules as (premises, conclusion)

    # Step 1: Separate facts and rules from KB
    for clause in KB_AST:
        if isinstance(clause, Symbol):
            # Simple fact like "a"
            if clause.name not in facts_set:
                facts_list.append(clause.name)
                facts_set.add(clause.name)

        elif isinstance(clause, Imply):
            # Horn rule of the form A => B or A & B => C
            if isinstance(clause.right, Symbol):
                conclusion = clause.right.name  # Right-hand side (conclusion)
            else:
                continue  # Ignore malformed rules

            # Extract premises from left-hand side
            left = clause.left
            premises = []

            def get_conjuncts(expr):
                # Helper to flatten A & B & C into [A, B, C]
                if isinstance(expr, And):
                    return get_conjuncts(expr.left) + get_conjuncts(expr.right)
                elif isinstance(expr, Symbol):
                    return [expr.name]
                else:
                    return []  # Unsupported syntax for FC

            if isinstance(left, Symbol):
                premises = [left.name]  # Single premise
            else:
                premises = get_conjuncts(left)

            # Add rule to rule base
            rules.append((premises, conclusion))

    # Step 2: Forward chaining loop
    entailed = list(facts_list)       # List of inferred symbols (initially facts)
    entailed_set = set(facts_list)    # For fast duplicate checking
    added = True                      # Loop control flag

    while added:
        added = False  # Reset flag each iteration
        for premises, conclusion in rules:
            if conclusion in entailed_set:
                continue  # Skip rule if conclusion is already known

            if all(p in entailed_set for p in premises):
                # All premises are known, so infer conclusion
                entailed.append(conclusion)
                entailed_set.add(conclusion)
                added = True  # Mark that a new symbol was inferred

    # Step 3: Check if query symbol was entailed
    return entailed, (query in entailed_set)
