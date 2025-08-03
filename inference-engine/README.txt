# Inference Engine for Propositional Logic

This project implements a Propositional Logic Inference Engine using three different reasoning algorithms:

* **Truth Table (TT) Method**: Works with both Horn and general propositional logic.
* **Forward Chaining (FC)**: Efficient inference for Horn-form knowledge bases.
* **Backward Chaining (BC)**: Goal-directed reasoning using Horn-form rules.

---

## 📁 Project Structure

```
.
├── iengine.py               # Entry point for running inference
├── parser.py                # Formula parser for TELL/ASK input
├── truth_table.py           # Implementation of truth table checking
├── forward_chaining.py      # Implementation of forward chaining
├── backward_chaining.py     # Implementation of backward chaining
├── test_genericKB.txt       # Sample test file (general KB)
├── test_genericKB_1.txt     # Sample test file (general KB with biconditional)
├── test_HornKB.txt          # Sample test file (Horn KB)
```

---

## ✅ How to Run

Open a terminal and use the following command:

```bash
python iengine.py <filename> <method>
```

* `<filename>`: path to a `.txt` file containing TELL/ASK.
* `<method>`: `TT` for Truth Table, `FC` for Forward Chaining, `BC` for Backward Chaining.

### Examples:

```bash
python iengine.py test_HornKB.txt FC
python iengine.py test_genericKB.txt TT
python iengine.py test_HornKB.txt BC
```

---

## 📌 Input Format

Input files must contain:

* `TELL` followed by Horn clauses or formulas separated by semicolons.
* `ASK` followed by a single query proposition.

### Example `test_HornKB.txt`

```
TELL
p2=> p3; p3 => p1; c => e; b&e => f; f&g => h; p2&p1&p3 =>d; p1&p3 => c; a; b; p2;
ASK
d
```

---

## 🧠 Supported Logic Syntax

* `~` for NOT
* `&` for AND
* `||` for OR
* `=>` for IMPLICATION
* `<=>` for BICONDITIONAL

### Example:

```
TELL
(a <=> (c => ~d)) & b & (b => a); c; ~f || g;
ASK
~d & (~g => ~f)
```

---

## 🔍 Output Format

* For TT:

  * `YES: <number>` if query is entailed with that many models
  * `NO` if not entailed

* For FC and BC:

  * `YES: <list of entailed symbols>` if the query is entailed
  * `NO` otherwise

### Sample Outputs:

```
YES: 3
YES: a, b, p2, p3, p1, c, e, f, d
YES: p2, p3, p1, d
NO
```

---

## ✍️ Author Notes

* This project is designed for academic use in COS30019 – Introduction to AI.
* Python 3.8+ recommended.
* All algorithms tested on real Horn and general propositional knowledge bases.

---

## 🧪 Testing

Use the provided test files to validate all three reasoning engines. You can create your own test files by following the format shown above.

---

## 📚 References

* Russell & Norvig. Artificial Intelligence: A Modern Approach (3rd Edition)
* COS30019 Assignment 2 Specification

---

Happy reasoning! 🧠
