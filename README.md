<div align="center">

# 🤖 Artificial Intelligence Laboratory

### BMS College of Engineering, Bengaluru
##### (Autonomous College under VTU Belagavi) | Department of Computer Science and Engineering

<p>
<img src="https://img.shields.io/badge/Language-Python%203-blue?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Course%20Code-23CS5PCAIN-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/Semester-5th-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/Programs-13-purple?style=for-the-badge" />
<img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

Python implementations of the **Artificial Intelligence laboratory programs**, covering intelligent agents, search, local search, propositional and first order logic, and adversarial search, following the **23CS5PCAIN** syllabus.

</div>

---

## 👨‍🎓 Student & Course Information

| Student | Details | Course | Details |
|---|---|---|---|
| **Name** | Priyanshu Sharan | **Course Title** | Artificial Intelligence |
| **USN** | 1WA24CS223 | **Course Code** | 23CS5PCAIN |
| **Semester** | 5th Semester | **Credits (L-T-P)** | 4 (3-0-1) |
| **Department** | Computer Science and Engineering | **Language** | Python 3 |
| **Institution** | BMS College of Engineering | **Environment** | Linux / Windows / macOS |

---

## 📚 Programs

| # | Program | Topic | Folder |
|:-:|---|---|---|
| 1 | Tic-Tac-Toe game | Intelligent Agents | [`tic-tac-toe`](01-intelligent-agents/tic-tac-toe) |
| 1 | Vacuum cleaner agent (simple reflex + goal-based) | Intelligent Agents | [`vacuum-cleaner-agent`](01-intelligent-agents/vacuum-cleaner-agent) |
| 2 | 8-Puzzle using Depth First Search | Uninformed Search | [`8-puzzle-dfs`](02-uninformed-search/8-puzzle-dfs) |
| 2 | 8-Puzzle using Iterative Deepening Search | Uninformed Search | [`8-puzzle-iterative-deepening`](02-uninformed-search/8-puzzle-iterative-deepening) |
| 3 | A* search: misplaced tiles heuristic | Informed Search | [`misplaced-tiles`](03-informed-search/a-star-8-puzzle/misplaced-tiles) |
| 3 | A* search: Manhattan distance heuristic | Informed Search | [`manhattan-distance`](03-informed-search/a-star-8-puzzle/manhattan-distance) |
| 4 | Hill Climbing for N-Queens (4-Queens) | Local Search | [`hill-climbing-4-queens`](04-local-search/hill-climbing-4-queens) |
| 5 | Simulated Annealing for 8-Queens | Local Search | [`simulated-annealing-8-queens`](04-local-search/simulated-annealing-8-queens) |
| 6 | Truth-table entailment in propositional logic | Propositional Logic | [`truth-table-entailment`](05-propositional-logic/truth-table-entailment) |
| 7 | Unification in first order logic | First Order Logic | [`unification`](06-first-order-logic/unification) |
| 8 | Forward chaining in first order logic | First Order Logic | [`forward-chaining`](06-first-order-logic/forward-chaining) |
| 9 | Resolution in first order logic | First Order Logic | [`resolution`](06-first-order-logic/resolution) |
| 10 | Alpha-Beta Pruning | Adversarial Search | [`alpha-beta-pruning`](07-adversarial-search/alpha-beta-pruning) |

> `#` is the program number used in the lab record index. Each folder has its own README with the aim, algorithm and sample output.

---

## 🗂️ Repository Structure

```
artificial-intelligence/
├── README.md
├── LICENSE
├── 01-intelligent-agents/
│   ├── tic-tac-toe/
│   │   ├── tic_tac_toe.py
│   │   ├── output-1.png
│   │   └── output-2.png
│   └── vacuum-cleaner-agent/
│       ├── vacuum_cleaner_agent.py
│       └── output.png
├── 02-uninformed-search/
│   ├── 8-puzzle-dfs/
│   │   ├── dfs_8_puzzle.py
│   │   └── output.png
│   └── 8-puzzle-iterative-deepening/
│       ├── ids_8_puzzle.py
│       └── output.png
├── 03-informed-search/
│   └── a-star-8-puzzle/
│       ├── misplaced-tiles/
│       │   ├── a_star_misplaced_tiles.py
│       │   └── output.png
│       └── manhattan-distance/
│           ├── a_star_manhattan_distance.py
│           └── output.png
├── 04-local-search/
│   ├── hill-climbing-4-queens/
│   │   ├── hill_climbing_4_queens.py
│   │   └── output.png
│   └── simulated-annealing-8-queens/
│       ├── simulated_annealing_8_queens.py
│       └── output.png
├── 05-propositional-logic/
│   └── truth-table-entailment/
│       ├── truth_table_entailment.py
│       └── output.png
├── 06-first-order-logic/
│   ├── unification/
│   │   ├── unification.py
│   │   ├── output-1.png
│   │   └── output-2.png
│   ├── forward-chaining/
│   │   ├── forward_chaining.py
│   │   └── output.png
│   └── resolution/
│       ├── resolution.py
│       └── output.png
└── 07-adversarial-search/
    └── alpha-beta-pruning/
        ├── alpha_beta_pruning.py
        └── output.png
```

Every program folder also contains a `README.md`.

---

## 🚀 Getting Started

**Requirements:** Python 3.8 or newer. Only the standard library is used, so there is nothing to install.

```bash
git clone https://github.com/priyanshusharan-cmd/artificial-intelligence.git
cd artificial-intelligence

# run any program from its folder, for example:
cd 07-adversarial-search/alpha-beta-pruning
python3 alpha_beta_pruning.py
```

Programs that read input (tic-tac-toe, vacuum cleaner, 8-puzzle, unification, alpha-beta) prompt for it in the terminal. For the 8-puzzle, enter each row as space-separated numbers with `0` for the blank.

---

## 🧠 Topics Covered

| Unit | Topic | Programs |
|:-:|---|---|
| 1 | Intelligent agents, problem solving | Tic-Tac-Toe, Vacuum Cleaner Agent |
| 2 | Uninformed search | DFS, Iterative Deepening Search |
| 2 | Informed search | A* (Misplaced Tiles, Manhattan Distance) |
| 2 | Local search | Hill Climbing, Simulated Annealing |
| 3 | Propositional logic | Truth-Table Enumeration (TT-ENTAILS) |
| 4 | Inference in first order logic | Unification, Forward Chaining, Resolution |
| 4 | Adversarial search | Alpha-Beta Pruning |

---

## 📖 Reference

Stuart J. Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 3rd Edition, Pearson.

---

<div align="center">

**Priyanshu Sharan** · USN 1WA24CS223
Department of Computer Science and Engineering, BMS College of Engineering, Bengaluru

⭐ If you found this repository useful, consider giving it a star!

</div>
