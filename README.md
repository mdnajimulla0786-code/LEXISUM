# ⚡ LexiSym: Compiler Design Symbol Table & Lexical Analyzer

A comprehensive, interactive web-based Compiler Design project implementing **Lexical Analysis (Tokenization)**, **Separate Chaining Hash Table (O(1) average lookup)**, and **Hierarchical Scope Management with Shadowing Support**.

Built for academic submission and practical demonstrations in undergraduate Computer Science & Engineering (B.Tech / BE) Compiler Design laboratory courses.

---

## 🌟 Key Features

1. **Lexical Analyzer (Tokenizer)**
   - Categorizes C source tokens into `KEYWORD`, `IDENTIFIER`, `INTEGER`, `FLOAT`, `CHARACTER`, `STRING`, `OPERATOR`, and `SEPARATOR`.
   - Strips single-line (`//`) and multi-line (`/* */`) comments.
   - Detects lexical errors such as invalid identifiers (e.g. `123abc`).

2. **Hierarchical Scope Stack & Nested Blocks**
   - Implements a LIFO scope stack: `global` &rarr; `function` &rarr; `function.if.1` &rarr; `function.if.1.for.1`.
   - Accurately tracks brace `{ ... }` depth across loops, conditionals, and functions without prematurely resetting to global scope.
   - Supports multi-variable declarations on a single line (`int a = 1, b = 2;`, `float x, y, z;`).
   - Automatically detects function declarations, return types, and parameter lists (`int argc, char *argv[]`).

3. **Lexical Shadowing & Semantic Rules**
   - **Allowed Shadowing:** The same identifier can be declared in different scopes (e.g. `int x = 10;` in `global` and `int x = 20;` inside `calculate()`).
   - **Duplicate Detection:** Rejects redeclaration of the same identifier in the **same scope** (`ERROR: Duplicate identifier 'x' in scope 'test'`).
   - **Undeclared Identifier Warnings:** Flags identifiers used before being declared in any visible ancestor scope.

4. **Separate Chaining Hash Table**
   - Fixed 10-bucket array with linked-list nodes.
   - Deterministic ASCII-sum hash function:
     $$h(\text{key}) = \left(\sum_{i=1}^{n} \text{ord}(c_i)\right) \pmod{10}$$
   - Resolves collisions via separate chaining without overwriting.
   - Live collision counters, occupancy percentage, and load factor calculation.

5. **Scope-Aware Symbol Lookup**
   - Resolves identifiers following the lexical scoping chain:
     $$\text{Current Scope} \longrightarrow \text{Parent Scope} \longrightarrow \dots \longrightarrow \text{Global Scope}$$
   - Returns the nearest shadowed definition or flags undeclared variables.

6. **Interactive Developer-Tool UI**
   - **Dashboard:** Live load factor gauge, 10-bucket occupancy bar, recent symbols table.
   - **Symbol Registry:** Instant live search, filter by datatype/scope/role, in-place edit modal, delete actions.
   - **Insert Symbol:** Real-time ASCII character-by-character hash calculation preview.
   - **Hash Visualizer:** Interactive diagram of buckets 0–9 with linked-list node pointers (`Node ──▶ Node ──▶ NULL`) and test calculator.
   - **Scope Analysis:** Visual scope hierarchy tree (`GLOBAL └── calculate └── calculate.if.1`) and variable visibility tables.
   - **Code Analyzer:** C code editor with 4 presets (including the Task 18 integration benchmark), error report banner, and live token stream table.
   - **Data Export:** Instant download of symbol tables in standard **CSV** and **JSON** formats.

---

## 🏗️ System Architecture

```text
               +-----------------------------------+
               |         C Source Code             |
               +-----------------------------------+
                                 |
                                 v
               +-----------------------------------+
               |        Lexical Analyzer           |
               |       (code_analyzer.py)          |
               +-----------------------------------+
                     /           |           \
                    v            v            v
            [Token Stream]   [Scope Stack]   [Compiler Errors]
              - KEYWORD        - global        - Duplicates
              - IDENTIFIER     - func          - Undeclared
              - OPERATOR       - func.if.1     - Invalid IDs
              - CONSTANT       - func.for.1
                                 |
                                 v
               +-----------------------------------+
               |          Symbol Table             |
               |        (symbol_table.py)          |
               +-----------------------------------+
                                 |
                     Deterministic Hash:
                   sum(ord(c)) % 10 = index
                                 |
                                 v
               +-----------------------------------+
               |      10-Bucket Hash Table         |
               |        (hash_table.py)            |
               |        Separate Chaining          |
               | [Bucket 0] -> Node -> Node -> NULL|
               | [Bucket 1] -> NULL                |
               | ...                               |
               | [Bucket 9] -> Node -> NULL        |
               +-----------------------------------+
                                 |
                                 v
               +-----------------------------------+
               |     Flask REST API & Web UI       |
               |       (app.py + templates/)       |
               +-----------------------------------+
```

---

## 📁 Project Structure

```
d:/study/COMPILER DEGINE PROJECT/
├── app.py                   # Flask server, REST APIs, and export endpoints
├── code_analyzer.py         # Tokenizer, nested scope tracking, semantic checks
├── hash_table.py            # 10-bucket separate chaining hash table
├── symbol_table.py          # Scope-aware symbol manager & lexical lookup
├── test_compiler.py         # Automated 18-case test suite
├── README.md                # Project documentation
├── docs/
│   ├── project_report.md    # 24-section academic project report
│   └── viva_questions.md    # 50+ viva questions, answers & time-based pitches
├── static/
│   ├── css/
│   │   └── style.css        # Modern dark-mode developer UI design system
│   └── js/
│       └── main.js          # Client-side API caller & toast notifications
└── templates/
    ├── base.html            # Shared layout with navigation & footer
    ├── index.html           # Dashboard & system metrics
    ├── symbols.html         # Symbol table registry with search & filters
    ├── add.html             # Manual insertion with live ASCII hash preview
    ├── hashing.html         # Separate chaining visualizer & calculator
    ├── scope.html           # Hierarchical scope tree & grouped tables
    └── analyzer.html        # C code editor, token stream & compiler errors
```

---

## ⚙️ REST API Endpoints

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | Dashboard web page |
| `/symbols-page` | `GET` | Full Symbol Table management view |
| `/add-page` | `GET` | Manual symbol insertion view |
| `/hashing-page` | `GET` | Separate chaining hash table visualizer |
| `/scope-page` | `GET` | Scope hierarchy view |
| `/analyzer-page` | `GET` | C code lexical and scope analyzer view |
| `/api/stats` | `GET` | System stats (total, global, local, buckets, load factor) |
| `/symbols` | `GET` | Returns list of all stored symbols with hash indices |
| `/add-symbol` | `POST` | Inserts an identifier token (`name, type, value, scope, line, token_type`) |
| `/search/<name>` | `GET` | Scope-aware search (optional query param `?scope=...`) |
| `/update/<name>` | `PUT` | Updates datatype, value, scope, or line number |
| `/delete/<name>` | `DELETE` | Removes symbol (optional query param `?scope=...`) |
| `/api/clear` | `POST` | Resets the symbol table |
| `/analyze` | `POST` | Tokenizes and extracts symbols from source code |
| `/hash-table` | `GET` | Returns collision chains across all 10 buckets |
| `/api/scopes` | `GET` | Returns scope hierarchy tree |
| `/export/csv` | `GET` | Downloads symbol table as `symbol_table.csv` |
| `/export/json` | `GET` | Downloads symbol table as `symbol_table.json` |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9+ installed
- Flask (`pip install flask`)

### 1. Start the Flask Server
```powershell
python app.py
```
*The server will start on `http://127.0.0.1:5000`.*

### 2. Run Automated Test Suite
```powershell
python test_compiler.py
```
*Expected output: `Ran 18 tests in 0.213s. OK`.*

---

## 🧪 Benchmark Program (Task 18 Integration Test)

Paste this benchmark program into the **Code Analyzer** page (`Preset 4`):

```c
int globalVar = 10;
float pi = 3.14;

void calculate(int x, float y) {

    int result = 0;

    if (x > 0) {

        int result = 20;

        for (int i = 0; i < 5; i++) {

            int temp = i;

        }

        int afterLoop = 50;
    }

    int finalValue = 100;
}
```

### Analysis Verification
- **Global Scope:** `globalVar` (10), `pi` (3.14), `calculate` (function)
- **Function Scope (`calculate`):** `x` (param), `y` (param), `result` (0), `finalValue` (100)
- **IF Block Scope (`calculate.if.1`):** `result` (20), `afterLoop` (50)
- **FOR Block Scope (`calculate.if.1.for.1`):** `i` (0), `temp` (`i`)
- **Shadowing Result:** The two declarations of `result` in different scopes are permitted without errors. Lookup from inside the IF block returns `20`, while lookup from the outer function returns `0`.
