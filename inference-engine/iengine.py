# iengine.py
import sys
from parser import parse_file, parse_formula
from truth_table import tt_entails
from forward_chaining import forward_chain
from backward_chaining import backward_chain

def main():
    """
    Main entry for the inference engine.
    Usage: python iengine.py <filename> <method>
    method: TT (Truth Table), FC (Forward Chaining), BC (Backward Chaining)
    """
    if len(sys.argv) != 3:
        print("Usage: python iengine.py <filename> <method>")
        return

    filename = sys.argv[1]   # Input file with TELL and ASK
    method = sys.argv[2].upper()  # Inference method: TT, FC, or BC

    try:
        # Parse the TELL and ASK sections from the file
        kb_sentences, query_str = parse_file(filename)
    except Exception as e:
        print(f"Error parsing file: {e}")
        return

    # Parse all the knowledge base (KB) sentences into logical expressions (ASTs)
    KB_AST = []
    for sentence in kb_sentences:
        try:
            formula = parse_formula(sentence)
            KB_AST.append(formula)
        except Exception as e:
            print(f"Error parsing formula '{sentence}': {e}")
            return

    # Depending on the method chosen, invoke the appropriate inference engine
    if method == "TT":
        try:
            query_ast = parse_formula(query_str)  # Parse the query expression
        except Exception as e:
            print(f"Error parsing query '{query_str}': {e}")
            return

        # Perform truth table entailment checking
        entails, model_count = tt_entails(KB_AST, query_ast)
        if entails:
            print(f"YES: {model_count}")  # If entailed, print YES and number of models
        else:
            print("NO")  # Not entailed

    elif method == "FC":
        # Forward chaining works on symbol names (not logical expressions)
        query_symbol = query_str.strip()
        try:
            # Try to extract the symbol name from the query
            q_ast = parse_formula(query_symbol)
            if hasattr(q_ast, 'name'):
                query_symbol = q_ast.name
        except Exception:
            pass  # Fallback to original string if parse fails

        # Perform forward chaining
        entailed, entails = forward_chain(KB_AST, query_symbol)
        if entails:
            print("YES: " + ", ".join(entailed))  # Output the entailed symbols
        else:
            print("NO")

    elif method == "BC":
        # Backward chaining also works with symbol names
        query_symbol = query_str.strip()
        try:
            q_ast = parse_formula(query_symbol)
            if hasattr(q_ast, 'name'):
                query_symbol = q_ast.name
        except Exception:
            pass

        # Perform backward chaining
        entailed, entails = backward_chain(KB_AST, query_symbol)
        if entails:
            print("YES: " + ", ".join(entailed))  # Output entailed chain
        else:
            print("NO")

    else:
        # Invalid method argument
        print(f"Unknown method: {method}. Use TT, FC, or BC.")

if __name__ == "__main__":
    main()
