# COS30019 – Introduction to AI: Search Algorithms & Inference Engine

Two Python projects for **COS30019 Introduction to Artificial Intelligence** at Swinburne University of Technology (Hanoi), June – August 2025.

## 1. Robot Navigation – tree-based search ([`robot-navigation`](robot-navigation))
Individual assignment (June 2025). A robot must find a path from a start cell to one of several goal cells on an N×M grid with walls.

- **Uninformed:** Depth-First Search, Breadth-First Search, *Custom 1* = Iterative-Deepening DFS
- **Informed:** Greedy Best-First Search, A\*, *Custom 2* = Weighted A\*
- Pluggable heuristics: Manhattan, Euclidean, Chebyshev
- Clean architecture with interfaces (`Components/Interfaces`), a parser for the problem file, and a **Tkinter visualiser** that animates the search
- Report: [`robot-navigation/report/RobotNav_Report.pdf`](robot-navigation/report)

```bash
cd robot-navigation
python search.py Test/RobotNav-test.txt AS     # DFS | BFS | GBFS | AS | CUS1 | CUS2
python search.py ui                            # interactive visualiser
```

## 2. Propositional-Logic Inference Engine ([`inference-engine`](inference-engine))
Pair assignment with Nguyen Huu Duc Anh (July – August 2025). Given a knowledge base (`TELL`) and a query (`ASK`), decides entailment with:

- **Truth Table (TT)** checking — Horn and generic KBs
- **Forward Chaining (FC)** and **Backward Chaining (BC)** — Horn KBs
- Recursive-descent formula parser supporting `~`, `&`, `||`, `=>`, `<=>`; 16 test cases plus research tests (CNF, DPLL-style and negation edge cases)
- Report: [`inference-engine/report/InferenceEngine_Report.pdf`](inference-engine/report)

```bash
cd inference-engine
python iengine.py test_case/test_HornKB.txt FC
```

## Notes
- Commit dates reflect the original file modification dates of the coursework; the repository itself was published on GitHub in November 2026.
