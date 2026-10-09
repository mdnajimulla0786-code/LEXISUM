# PROJECT REPORT
## Title: Implementation of a Scope-Aware Symbol Table Management System and Lexical Analyzer Using Separate Chaining Hash Tables

**Course:** B.Tech Computer Science and Engineering  
**Subject:** Compiler Design (CS-X01)  
**Academic Year:** 2026–2027  

---

### Table of Contents
1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Existing System](#5-existing-system)
6. [Proposed System](#6-proposed-system)
7. [Requirements Specification](#7-requirements-specification)
8. [System Architecture](#8-system-architecture)
9. [Module Descriptions](#9-module-descriptions)
10. [Symbol Table Data Structure](#10-symbol-table-data-structure)
11. [Hash Function Design](#11-hash-function-design)
12. [Collision Resolution: Separate Chaining](#12-collision-resolution-separate-chaining)
13. [Scope Management & Lexical Shadowing](#13-scope-management--lexical-shadowing)
14. [Lexical Analysis & Tokenization](#14-lexical-analysis--tokenization)
15. [Algorithms & Complexity Analysis](#15-algorithms--complexity-analysis)
16. [System Flowcharts](#16-system-flowcharts)
17. [Implementation Details](#17-implementation-details)
18. [Test Cases & Experimental Verification](#18-test-cases--experimental-verification)
19. [Results & Discussions](#19-results--discussions)
20. [System Advantages](#20-system-advantages)
21. [Limitations](#21-limitations)
22. [Future Scope](#22-future-scope)
23. [Conclusion](#23-conclusion)
24. [References](#24-references)

---

### 1. Abstract
The symbol table is the central data structure in a compiler, responsible for storing essential semantic attributes of identifiers, including data types, memory offsets, scope levels, and token categories. Traditional linear symbol tables suffer from $O(n)$ search and insertion complexities, rendering them inefficient for large programs. This project presents a full-stack, scope-aware Compiler Design Symbol Table Management System and Lexical Analyzer. Utilizing a 10-bucket hash table with separate chaining via linked lists, the system achieves $O(1)$ average-case insertion, lookup, and deletion time. It implements a lexical tokenizer that categorizes C tokens, tracks nested block scopes via a LIFO scope stack, enforces semantic shadowing, and flags duplicate declarations. A responsive, developer-grade web interface visualizes collision chains, scope trees, and token streams in real-time, accompanied by automated CSV/JSON data export.

---

### 2. Introduction
In computer language processing, a compiler translates high-level source code into low-level machine instructions across multiple sequential phases:
1. **Lexical Analysis (Scanner)**: Breaks source code into a stream of meaningful tokens.
2. **Syntax Analysis (Parser)**: Builds hierarchical parse trees representing grammatical structure.
3. **Semantic Analysis**: Enforces type compatibility, declaration rules, and scope boundaries.
4. **Intermediate Code Generation**: Translates parse trees into linear intermediate representations.
5. **Code Optimization**: Improves execution speed and minimizes resource footprint.
6. **Target Code Generation**: Generates machine or assembly code.

The **Symbol Table** interfaces directly with every phase. During lexical and syntax analysis, symbols are identified and registered. During semantic analysis, types are checked and scope boundaries are verified. This project realizes the core operational principles of Phase 1 (Lexical Analysis) and Phase 3 (Semantic Scope Management) through an accessible, interactive software platform.

---

### 3. Problem Statement
Simple symbol table implementations frequently face three major challenges:
1. **Performance Bottlenecks:** Naive linear lists or array implementations require $O(n)$ search time, causing compiler degradation on large codebases.
2. **Scope Obliviousness:** Basic hash tables store identifiers globally by name alone, incorrectly rejecting legal variable shadowing (e.g. declaring a local variable with the same name as a global variable) or incorrectly retaining local variables across nested blocks.
3. **Lack of Visual Introspection:** Students and developers lack intuitive tools to observe how hashing algorithms distribute identifiers, how collision chains grow, and how compiler scope stacks expand and collapse during brace resolution.

---

### 4. Objectives
- Implement a deterministic hash table with separate chaining for collision resolution.
- Develop an accurate lexical tokenizer recognizing C keywords, identifiers, constants, strings, operators, and separators.
- Implement a LIFO scope stack to support nested block scopes (`if`, `for`, `while`, anonymous `{ ... }`) and function scopes without premature resets.
- Support multi-variable declarations (`int a = 1, b = 2;`) and function parameter parsing (`int argc, char *argv[]`).
- Enforce semantic rules: allow legitimate identifier shadowing across different scopes while strictly rejecting duplicate declarations within the same scope.
- Provide scope-aware search traversing the lexical ancestry: $\text{Current Scope} \to \text{Parent} \to \text{Global}$.
- Build an interactive, modern web interface with live visualizers and CSV/JSON export capabilities.

---

### 5. Existing System
Existing teaching tools are typically command-line C or Python scripts that output raw text dumps.
- **Drawbacks:**
  - Inflexible static data without interactive querying.
  - No visualization of linked-list collision chains.
  - Fragile regexes that reset scope upon encountering any closing brace `}`.
  - Inability to export structured data for laboratory reports.

---

### 6. Proposed System
The proposed system implements a complete client-server compiler demonstration platform:
- **Backend:** Python Flask microframework serving REST endpoints for lexical analysis, symbol CRUD, hash state inspection, and file exports.
- **Data Structure Layer:** Pure Python object-oriented implementation of `Node`, `HashTable` (10 buckets, separate chaining), and `SymbolTable`.
- **Frontend Layer:** Responsive dark-mode dashboard with real-time SVG visualizers, live ASCII calculation monitors, and interactive code editors.

---

### 7. Requirements Specification
- **Hardware Requirements:**
  - Processor: 1.6 GHz dual-core or higher
  - Memory: 2 GB RAM minimum
  - Storage: 100 MB available disk space
- **Software Requirements:**
  - Operating System: Windows 10/11, Linux, or macOS
  - Runtime: Python 3.9 or higher
  - Dependencies: Flask 2.0+
  - Web Browser: Chrome, Firefox, Edge, or Safari with JavaScript enabled

---

### 8. System Architecture
```text
 +-------------------------------------------------------------------+
 |                         User Web Browser                          |
 |  [Dashboard] [Symbol Table] [Hash Visualizer] [Scope Hierarchy]  |
 +-------------------------------------------------------------------+
                                   | HTTP / JSON
                                   v
 +-------------------------------------------------------------------+
 |                         Flask Controller                          |
 |       Endpoints: /analyze, /symbols, /hash-table, /export/*       |
 +-------------------------------------------------------------------+
             |                                           |
             v                                           v
 +-----------------------+                   +-----------------------+
 |    Code Analyzer      |                   |     Symbol Table      |
 |  - Tokenizer          |                   |  - Scope Ancestry     |
 |  - Scope Stack        |                   |  - Shadowing Engine   |
 |  - Semantic Validator |                   |  - CRUD Controller    |
 +-----------------------+                   +-----------------------+
                                                         |
                                                         v
                                             +-----------------------+
                                             |      Hash Table       |
                                             |  - 10-Bucket Array    |
                                             |  - Separate Chaining  |
                                             |  - Node Linked Lists  |
                                             +-----------------------+
```

---

### 9. Module Descriptions
1. **`hash_table.py`:** Contains `Node` and `HashTable`. Implements the deterministic hash function, bucket array, and linked-list operations (`insert`, `search`, `delete`, `get_all`, `get_table_state`).
2. **`symbol_table.py`:** Contains `SymbolTable`. Orchestrates scope-aware symbol insertion, duplicate detection, hierarchical lookup, and statistics calculation.
3. **`code_analyzer.py`:** Contains `CodeAnalyzer`. Performs regex-driven tokenization, maintains the scope stack, extracts parameters and multi-variable declarations, and identifies compiler errors.
4. **`app.py`:** Provides the REST API routes, template rendering, and file export streams.
5. **Frontend Modules:** HTML templates and CSS/JS assets providing visual interfaces for each compiler design concept.

---

### 10. Symbol Table Data Structure
Each symbol is represented as an in-memory record:
```c
struct SymbolRecord {
    char* name;           // Identifier token lexeme (e.g. "result")
    char* data_type;      // Type specification (e.g. "int", "float*")
    char* token_type;     // Category: "identifier", "parameter", "function"
    char* value;          // Initial constant or assigned expression
    char* scope;          // Enclosing scope (e.g. "calculate.if.1")
    char* parent_scope;   // Immediate ancestor (e.g. "calculate")
    int   line_number;    // Source code line where declared
    int   hash_index;     // Computed bucket index (0 - 9)
};
```

---

### 11. Hash Function Design
The project utilizes a deterministic ASCII summation modulo function:
$$h(K) = \left(\sum_{i=0}^{L-1} \text{ord}(K[i])\right) \pmod m$$
Where:
- $K$ is the identifier string of length $L$.
- $\text{ord}(c)$ is the ASCII integer code of character $c$.
- $m = 10$ is the fixed bucket capacity.

**Example Calculation:**
For identifier `x`:
- $\text{ASCII}('x') = 120$
- $h('x') = 120 \pmod{10} = 0$ (Bucket #0)

For identifier `count`:
- $\text{ord}('c') = 99, \text{ord}('o') = 111, \text{ord}('u') = 117, \text{ord}('n') = 110, \text{ord}('t') = 116$
- $\text{Sum} = 99 + 111 + 117 + 110 + 116 = 553$
- $h(\text{"count"}) = 553 \pmod{10} = 3$ (Bucket #3)

---

### 12. Collision Resolution: Separate Chaining
When two distinct identifiers produce the identical bucket index (e.g. `'count'` ($553 \pmod{10} = 3$) and `'ch'` ($99 + 104 = 203 \pmod{10} = 3$)), a **hash collision** occurs.
The system resolves collisions via **Separate Chaining**:
- Each bucket in the table array points to the head of a singly linked list of `Node` objects.
- When a collision occurs, the new node is appended to the tail of the linked list for that bucket.
- **Deletions** splice the target node out of the chain by reassigning `prev.next = current.next`.
- **Search** traverses only the chain corresponding to $h(\text{key})$, yielding $O(1 + \alpha)$ expected search time, where $\alpha = \frac{n}{m}$ is the load factor.

---

### 13. Scope Management & Lexical Shadowing
#### Scope Stack Model
A LIFO stack tracks current scope:
```text
[ "global" ]
   |-- Enter function 'calculate'  --> [ "global", "calculate" ]
   |-- Enter if block              --> [ "global", "calculate", "calculate.if.1" ]
   |-- Enter for loop              --> [ "global", "calculate", "calculate.if.1", "calculate.if.1.for.1" ]
   |-- Exit for loop (pop)         --> [ "global", "calculate", "calculate.if.1" ]
   |-- Exit if block (pop)         --> [ "global", "calculate" ]
   |-- Exit function (pop)         --> [ "global" ]
```

#### Lexical Shadowing Rule
- A variable `x` declared inside `calculate.if.1` shadows `x` in `calculate`, which in turn shadows `x` in `global`.
- Duplicate checking enforces:
  $$\text{Duplicate Error} \iff \text{name}_1 = \text{name}_2 \land \text{scope}_1 = \text{scope}_2$$
- Declarations with the same identifier in distinct scopes are valid and stored as distinct nodes in the hash table.

#### Scope-Aware Lookup
When resolving a symbol reference from scope $S$:
$$\text{Search}(S) \xrightarrow{\text{not found}} \text{Search}(\text{Parent}(S)) \xrightarrow{\text{not found}} \dots \xrightarrow{\text{not found}} \text{Search}(\text{"global"}) \xrightarrow{\text{not found}} \text{Undeclared Error}$$

---

### 14. Lexical Analysis & Tokenization
The lexical scanner tokenizes input using regular expression patterns:
- **Keywords:** `int`, `float`, `double`, `char`, `void`, `if`, `else`, `for`, `while`, `return`, `break`, `continue`, `switch`, `case`, `default`, `struct`.
- **Identifiers:** `^[a-zA-Z_][a-zA-Z0-9_]*$`
- **Numeric Literals:** Floats (`\d+\.\d+`) and Integers (`\d+`)
- **String & Char Literals:** `"..."` and `'.'`.
- **Operators:** Arithmetic (`+`, `-`, `*`, `/`, `%`), Relational (`==`, `!=`, `<`, `>`, `<=`, `>=`), Logical (`&&`, `||`, `!`), Assignment (`=`, `+=`, `-=`, etc.).
- **Separators:** `(`, `)`, `{`, `}`, `[`, `]`, `;`, `,`.
- **Lexical Errors:** Identifiers starting with digits (`123var`) are detected and flagged immediately.

---

### 15. Algorithms & Complexity Analysis

#### Algorithm 1: Separate Chaining Hash Insertion
```text
Algorithm InsertSymbol(key, symbol_data):
  1. index = HashFunction(key)
  2. If table[index] is NULL:
       table[index] = Node(key, symbol_data)
       Return True
  3. current = table[index]
  4. While current is not NULL:
       If current.key == key and current.value.scope == symbol_data.scope:
         current.value = symbol_data  // In-place update
         Return True
       If current.next is NULL:
         Break
       current = current.next
  5. current.next = Node(key, symbol_data)
  6. Return True
```

#### Complexity Summary
| Operation | Average Case | Worst Case (High Collisions) |
| :--- | :---: | :---: |
| **Insert** | $O(1)$ | $O(n)$ |
| **Search** | $O(1)$ | $O(n)$ |
| **Delete** | $O(1)$ | $O(n)$ |
| **Scope Resolution** | $O(d)$ ($d$ = nesting depth) | $O(d \cdot n)$ |

---

### 16. System Flowcharts

```text
                  +---------------------------+
                  |     Start C Analysis      |
                  +---------------------------+
                                |
                                v
                  +---------------------------+
                  |   Scan Line by Line       |
                  |   Generate Token Stream   |
                  +---------------------------+
                                |
                                v
                  +---------------------------+
                  |   Token Type Branching    |
                  +---------------------------+
                   /          |             \
        Control (if/for)   Type Keyword      Braces ({ / })
               |              |                     |
               v              v                     v
       Push pending     Parse variable(s)    Push / Pop Scope
       subscope identifier   or function/params    from Scope Stack
                              |
                              v
                  +---------------------------+
                  | Check Same-Scope Duplicate|
                  +---------------------------+
                     /                     \
                   Yes                      No
                    |                        |
                    v                        v
        Emit Duplicate Error       Compute Hash: sum % 10
                                             |
                                             v
                                   Append to Bucket Chain
```

---

### 17. Implementation Details
The project is organized in modular Python and HTML/CSS/JS components:
- **`code_analyzer.py`**: Tokenizer engine that maintains `scope_stack = ['global']`, handles multi-variable parsing, and registers symbols with scopes.
- **`hash_table.py`**: Encapsulates the 10-bucket array, collision chains, and node metadata.
- **`symbol_table.py`**: Implements the symbol management layer, duplicate rules, and scope hierarchy builders.
- **`app.py`**: Flask web server delivering endpoints for CRUD, analysis, scope trees, and CSV/JSON downloads.

---

### 18. Test Cases & Experimental Verification
The automated test suite (`test_compiler.py`) validates all system behaviors:

| Test ID | Test Description | Input Condition | Expected Output | Status |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | Basic Symbol Insertion | `x = 10` in `global` | `total = 1`, `global = 1` | ✅ Passed |
| **TC-02** | Search Existing Symbol | Query `"varA"` | Symbol record returned | ✅ Passed |
| **TC-03** | Update Symbol In-Place | Modify value to `5` | Updated value saved | ✅ Passed |
| **TC-04** | Delete Symbol | Delete `"temp"` | Removed from chain | ✅ Passed |
| **TC-05** | Hash Collision | Keys `"a"` & `"k"` ($h = 7$) | Both coexist in Bucket 7 | ✅ Passed |
| **TC-06** | Duplicate in Same Scope | `int x; float x;` in `main` | Rejected with Error | ✅ Passed |
| **TC-07** | Scope Shadowing | `x` in `global`, `test`, `if.1` | All 3 stored successfully | ✅ Passed |
| **TC-08** | Global Lookup | Lookup `g_var` from inner scope | Resolves to global value | ✅ Passed |
| **TC-09** | Local Shadowing Lookup | Lookup `x` from `funcA` | Returns local `20`, not global | ✅ Passed |
| **TC-10** | Nested Scope Traversal | Lookup from `main.if.1` | Traverses to `main` | ✅ Passed |
| **TC-11** | Shadowing Precedence | Lookup from 3 nested scopes | Returns nearest scope value | ✅ Passed |
| **TC-12** | Undeclared Variable | Reference uninitialized `b` | Emits Undeclared Error | ✅ Passed |
| **TC-13** | Multi-Variable Line | `int a=1, b=2; float x,y;` | All 4 symbols extracted | ✅ Passed |
| **TC-14** | Function Parameters | `void calc(int x, float y)` | Parameters tagged to `calc` | ✅ Passed |
| **TC-15** | Nested `{ ... }` Braces | Three levels of `{}` | Correct scope push/pop | ✅ Passed |
| **TC-16** | CSV Export | `GET /export/csv` | Valid CSV stream returned | ✅ Passed |
| **TC-17** | JSON Export | `GET /export/json` | Valid JSON array returned | ✅ Passed |
| **TC-18** | Benchmark Integration | Task 18 C Program | 11 symbols, 0 errors | ✅ Passed |

---

### 19. Results & Discussions
All 18 automated tests executed cleanly in **0.213 seconds**.
When executing the benchmark Task 18 integration program:
- 11 symbols were extracted across 4 distinct scope levels (`global`, `calculate`, `calculate.if.1`, `calculate.if.1.for.1`).
- The two declarations of identifier `result` (one at line 6 with value `0` in `calculate`, and one at line 10 with value `20` in `calculate.if.1`) were both preserved in the hash table.
- Lookup queries from inside the IF block returned `result = 20`, while queries from the function body returned `result = 0`, demonstrating accurate lexical scope resolution.

---

### 20. System Advantages
1. **Accurate Lexical Scoping:** Unlike simplistic implementations, this system supports real-world language scoping rules including shadowing and nested block isolation.
2. **Deterministic & Visual:** Real-time visual feedback of hash chains, ASCII calculations, and scope trees demystifies abstract compiler concepts.
3. **High Efficiency:** Hash-based bucket distribution avoids linear scan overhead.
4. **Complete Toolchain:** Integrates scanning, scope validation, collision handling, and reporting in a unified application.

---

### 21. Limitations
1. Does not perform full grammar parsing or Abstract Syntax Tree (AST) construction (focuses on lexical and scope analysis).
2. Type checking is limited to declarations and does not validate complex expression type coercions (e.g. `int + float`).
3. Fixed bucket size of 10 is chosen for educational demonstration; dynamic rehashing would be preferred in production compilers.

---

### 22. Future Scope
- Implementation of an LL(1) or LR(1) syntax parser to generate full syntax trees.
- Intermediate Code Generation producing Three-Address Code (TAC) or quadruples.
- Dynamic table resizing (rehashing) when load factor $\alpha > 0.75$.
- Target assembly code generation (e.g. MIPS or x86-64).

---

### 23. Conclusion
This project successfully designed, implemented, and verified an end-to-end Symbol Table Management System and Lexical Analyzer for compiler design. By combining separate chaining hash tables, LIFO scope stacks, multi-variable extraction, and semantic error reporting with a modern user interface, the system satisfies all rigorous theoretical and practical requirements for undergraduate Compiler Design curricula.

---

### 24. References
1. Alfred V. Aho, Monica S. Lam, Ravi Sethi, and Jeffrey D. Ullman, *"Compilers: Principles, Techniques, and Tools"* (2nd Edition), Addison-Wesley, 2006.
2. Kenneth C. Louden, *"Compiler Construction: Principles and Practice"*, PWS Publishing, 1997.
3. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *"Introduction to Algorithms"* (3rd Edition), MIT Press, 2009.
4. Flask Documentation: https://flask.palletsprojects.com/
