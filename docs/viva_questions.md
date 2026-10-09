# Compiler Design Viva Questions & Demonstration Guide

This guide contains **50+ comprehensive viva questions and answers** covering all aspects of Compiler Design and this project, followed by structured **1-minute**, **3-minute**, and **5-minute project demonstration scripts**.

---

## ⏱️ Quick Demonstration Scripts

### 🎤 1-Minute Elevator Pitch
> *"Good morning, Professors. My project is 'LexiSym', an interactive Symbol Table Management System and Lexical Analyzer built for Compiler Design. In a compiler, the symbol table stores identifier semantics like data type, scope, and memory offset. Our system tokenizes C source code, detects function parameters and multi-variable declarations, and manages nested block scopes using a LIFO scope stack. For fast $O(1)$ search and insertion, we implemented a 10-bucket hash table with separate chaining collision resolution. The system also supports variable shadowing, rejects duplicate declarations in the same scope, detects undeclared identifiers, and visualizes collision chains and scope trees live in a modern web dashboard with CSV and JSON data export."*

---

### 🎤 3-Minute Technical Overview
> *"Good morning, Professors. The goal of this project is to implement and demonstrate the two foundational front-end phases of a compiler: Lexical Analysis and Semantic Symbol Table Management.*
>
> *First, in the Lexical Analysis phase, our scanner tokenizes C source code into keywords, identifiers, constants, strings, operators, and separators using regular expressions, while stripping single- and multi-line comments. It also detects lexical errors like invalid identifiers starting with numbers.*
>
> *Second, for Scope Management, we implemented a LIFO scope stack. When functions or nested blocks like `if` or `for` loops are entered, child scopes like `calculate.if.1` and `calculate.if.1.for.1` are pushed; when closing braces are met, scopes are popped cleanly without losing outer variables. We also support multi-variable declarations like `int a = 1, b = 2;` and function parameters.*
>
> *Third, for the Symbol Table, we use an array of 10 buckets backed by a deterministic ASCII summation modulo hash function: $h(key) = \sum \text{ord}(c) \pmod{10}$. When two identifiers hash to the same bucket index, separate chaining via singly linked list nodes resolves the collision without overwriting. Crucially, we enforce lexical shadowing: declaring `int result = 20;` inside an IF block shadows `int result = 0;` from the outer function without being flagged as a duplicate. Scope-aware search traverses upwards from the current scope to parent scopes and finally to global.*
>
> *Finally, the entire engine is wrapped in a Flask REST API with an interactive dark-mode dashboard where students can inspect real-time collision chains, test custom hash strings, view scope hierarchy trees, and download symbol tables as CSV or JSON."*

---

### 🎤 5-Minute Comprehensive College Viva Presentation
> 1. **Introduction & Motivation (1 min):**
>    *"A compiler consists of six phases. The symbol table is the only shared data structure accessed across every single phase. Traditional teaching examples use simple arrays that take $O(n)$ time or fail to handle nested blocks. Our project solves this by creating a production-grade educational platform featuring a 10-bucket separate chaining hash table and a scope-aware lexical parser."*
>
> 2. **Lexical Analysis & Tokenization (1 min):**
>    *(Show Code Analyzer page)*  
>    *"In our Code Analyzer, when we input C code, the tokenizer strips comments and splits the text into classified tokens: Keywords, Identifiers, Floats, Integers, Characters, Strings, Operators, and Separators. You can see the token stream table with line numbers on the screen. It also flags errors like `123abc` as invalid identifiers."*
>
> 3. **Scope Management & Shadowing (1 min):**
>    *(Load Preset 4 / Task 18 benchmark)*  
>    *"Here we have a function `calculate(int x, float y)` containing an IF block and an inner FOR loop. Notice how `result` is declared with value `0` in `calculate`, and declared again with value `20` inside `calculate.if.1`. Our semantic checker understands lexical shadowing: because they belong to different scopes, both are preserved! However, if we were to declare `int result` twice in the same scope, the compiler raises a duplicate error."*
>
> 4. **Hash Table & Separate Chaining (1 min):**
>    *(Navigate to Hash Visualizer)*  
>    *"Now look at our Hash Visualizer. We use the deterministic hash function $\text{sum}(\text{ASCII}) \pmod{10}$. Notice Bucket #3: it contains both `count` and `ch` linked together via separate chaining pointers: `Node -> Node -> NULL`. Neither overwrites the other. On the left, we can type any identifier name and watch the formula calculate character codes and bucket index in real time."*
>
> 5. **Scope Tree & Data Export (1 min):**
>    *(Navigate to Scope Page & click Export CSV)*  
>    *"The Scope Page visually renders the hierarchy tree: `GLOBAL` branching into `calculate` and nested blocks. Finally, the Symbol Registry allows filtering by datatype or scope, editing in place, and exporting the entire table to CSV or JSON with one click. In our automated test suite, all 18 unit and integration tests passed in 0.2 seconds. Thank you, and I am ready for questions."*

---

## 📚 50+ Viva Questions & Answers

### Group 1: General Compiler Concepts & Phases
#### Q1: What is a compiler?
**Ans:** A compiler is a language translator that converts high-level source code (like C) into equivalent low-level target machine code or assembly language in a single integrated process.

#### Q2: What are the phases of a compiler?
**Ans:** 
1. Lexical Analysis (Scanner)
2. Syntax Analysis (Parser)
3. Semantic Analysis
4. Intermediate Code Generation
5. Code Optimization
6. Target Code Generation

#### Q3: Which phases belong to the Front-End, and which belong to the Back-End?
**Ans:** 
- **Front-End (Machine-Independent):** Lexical, Syntax, Semantic Analysis, and Intermediate Code Generation.
- **Back-End (Machine-Dependent):** Code Optimization and Target Code Generation.

#### Q4: What is the role of the Symbol Table across these phases?
**Ans:** The symbol table records identifier names, types, scope levels, memory offsets, and attributes. It is populated by the scanner and parser, validated by semantic analysis, and referenced by intermediate and target code generators.

---

### Group 2: Lexical Analysis & Tokenization
#### Q5: What is a token, a lexeme, and a pattern?
**Ans:** 
- **Token:** An abstract category of syntactic element (e.g. `KEYWORD`, `IDENTIFIER`, `INTEGER`).
- **Lexeme:** The actual concrete character sequence in source code matching a token (e.g. `int`, `counter`, `42`).
- **Pattern:** The formal rule (usually a regular expression) describing the lexemes belonging to a token.

#### Q6: How does your lexical analyzer identify tokens?
**Ans:** It uses regular expressions mapped to distinct named groups: keywords (`int`, `float`, etc.), identifiers (`[a-zA-Z_]\w*`), numeric literals, operators, and separators.

#### Q7: How are single-line and multi-line comments handled?
**Ans:** Comments are matched using regex patterns (`//.*$` and `/\*.*?\*/`) and stripped before token stream generation so they do not produce spurious tokens.

#### Q8: What is an invalid identifier in C?
**Ans:** An identifier that violates naming rules, such as beginning with a numerical digit (e.g. `123abc`) or containing illegal characters.

---

### Group 3: Symbol Table & Data Structures
#### Q9: What data is stored in each entry of your symbol table?
**Ans:** Identifier name, data type (`int`, `float`, etc.), token category (`identifier`, `parameter`, `function`), initial assigned value, scope name, parent scope, source line number, and computed hash index.

#### Q10: What are the common data structures used to implement symbol tables?
**Ans:** Linear lists, arrays, Binary Search Trees (BST), AVL / Red-Black trees, and Hash Tables.

#### Q11: Why is a Hash Table preferred over an array or BST?
**Ans:** 
- Linear arrays require $O(n)$ search time.
- Balanced BSTs require $O(\log n)$ search time.
- Hash tables provide **$O(1)$ expected average-case** search, insert, and delete time.

---

### Group 4: Hashing & Separate Chaining
#### Q12: What hash function is used in this project?
**Ans:** The sum of ASCII character codes modulo table size:
$$h(K) = \left(\sum_{i=0}^{L-1} \text{ord}(K[i])\right) \pmod{10}$$

#### Q13: What is a hash collision?
**Ans:** A hash collision occurs when two different keys $K_1 \neq K_2$ evaluate to the same bucket index: $h(K_1) = h(K_2)$.

#### Q14: Give an example of two keys that collide in your project.
**Ans:** 
- Key `'a'`: $\text{ASCII} = 97 \implies 97 \pmod{10} = 7$.
- Key `'k'`: $\text{ASCII} = 107 \implies 107 \pmod{10} = 7$.  
Both hash to Bucket #7.

#### Q15: How does Separate Chaining resolve collisions?
**Ans:** Each slot in the bucket array points to the head of a singly linked list. When a collision occurs, the new record is added as a new node in that bucket's linked list chain.

#### Q16: What is Open Addressing and how does it differ from Separate Chaining?
**Ans:** In open addressing (linear probing, quadratic probing, double hashing), all elements are stored inside the hash table array itself. When a collision occurs, alternative slots are probed. In separate chaining, elements are stored in external linked lists, allowing infinite elements without table saturation.

#### Q17: What is the load factor ($\alpha$) of a hash table?
**Ans:** The load factor is the ratio of total stored elements ($n$) to the number of buckets ($m$): $\alpha = \frac{n}{m}$. In our project with $m=10$, storing 15 symbols gives $\alpha = 1.5$.

#### Q18: What is the worst-case time complexity of a hash table with separate chaining?
**Ans:** $O(n)$ in the worst case, which occurs if all $n$ keys produce the exact same hash index and form one long linked list.

---

### Group 5: Scopes, Nesting & Shadowing
#### Q19: What is lexical scoping (static scoping)?
**Ans:** Lexical scoping means that the visibility and lifetime of variable names are determined at compile time based strictly on their textual position and nesting within the source code.

#### Q20: How does your project track nested scopes?
**Ans:** Using a LIFO **Scope Stack** initialized with `['global']`. When entering a function or block (`if`, `for`, `while`, `{ ... }`), a child scope is pushed (e.g. `calculate.if.1`). When exiting via `}`, the scope is popped.

#### Q21: What is variable shadowing?
**Ans:** Shadowing occurs when an identifier declared within an inner scope has the exact same name as an identifier in an outer scope. The inner declaration temporarily hides (shadows) the outer variable.

#### Q22: Is shadowing allowed or an error?
**Ans:** Shadowing across **different scopes is completely legal**. It is **not** an error. However, declaring the same variable twice in the **exact same scope** is a duplicate declaration error.

#### Q23: How does your duplicate checking rule work?
**Ans:** A duplicate error is raised **if and only if** both the identifier name AND the scope match an existing record:
$$\text{Duplicate} \iff \text{name}_1 = \text{name}_2 \land \text{scope}_1 = \text{scope}_2$$

#### Q24: What is scope-aware lookup?
**Ans:** When resolving a variable, the compiler searches:
$\text{Current Scope} \to \text{Parent Scope} \to \text{Grandparent Scope} \to \text{Global Scope}$. The first matching definition is returned. If not found in any ancestor, an undeclared error is reported.

---

### Group 6: Advanced Compiler Features in this Project
#### Q25: How does your analyzer handle multi-variable declarations?
**Ans:** When a data type keyword is read, the analyzer parses a comma-separated list of declarators until a semicolon `;` is reached, correctly extracting all variables (e.g. `int a = 1, b = 2;`).

#### Q26: How are function parameters detected?
**Ans:** When a function signature is matched (e.g. `void calculate(int x, float y)`), the function itself is registered in the parent scope with role `function`, while each parameter is registered under the function's scope with role `parameter`.

#### Q27: How are pointer and array parameters handled?
**Ans:** The parser tracks asterisks (`*`) and brackets (`[]`), registering types like `char*[]` without crashing.

#### Q28: How does your analyzer handle `for` loop headers?
**Ans:** In `for (int i = 0; i < 5; i++) {`, the `for` scope is entered at the header so that `int i` belongs to the `for` loop's scope, and the matching `{` does not create an unintended duplicate block.

---

### Group 7: Implementation & Software Architecture
#### Q29: What web framework is used for the backend?
**Ans:** Python Flask, providing lightweight REST API endpoints and template rendering.

#### Q30: What endpoints are implemented in the API?
**Ans:**
- `/analyze` (`POST`): Tokenizes and populates symbols.
- `/symbols` (`GET`): Returns all symbols with bucket indices.
- `/add-symbol` (`POST`): Manually inserts a symbol.
- `/search/<name>` (`GET`): Performs scope-aware search.
- `/update/<name>` (`PUT`): Modifies existing symbol attributes.
- `/delete/<name>` (`DELETE`): Removes a symbol.
- `/hash-table` (`GET`): Returns 10-bucket chain state.
- `/export/csv` & `/export/json` (`GET`): Stream downloadable files.

#### Q31: How is the user interface designed?
**Ans:** Built with Vanilla HTML5, CSS3, and JavaScript featuring glassmorphism, responsive CSS grid layouts, and typography using Google Fonts `Outfit` and `JetBrains Mono`.

#### Q32: What automated tests were implemented?
**Ans:** An 18-test unit and integration test suite (`test_compiler.py`) covering insertion, search, delete, update, collisions, scope lookup, shadowing, multi-var declarations, parameters, exports, and the Task 18 benchmark program.

---

### Group 8: Quick Rapid-Fire Concepts
- **Q33: Can a local variable have the same name as a function?**  
  *Ans: Yes, inside the function block, it shadows the function name.*
- **Q34: What is static vs dynamic scoping?**  
  *Ans: Static scoping resolves variables based on code structure at compile time; dynamic scoping resolves variables based on the call stack at runtime.*
- **Q35: What is a lexeme?**  
  *Ans: The concrete string of source characters forming a token.*
- **Q36: Why is table size 10 used?**  
  *Ans: For clean visual demonstration of hash collisions in laboratory evaluations.*
- **Q37: What is the time complexity to search an identifier in your system?**  
  *Ans: $O(1)$ average case.*
- **Q38: What happens when an undeclared variable is referenced?**  
  *Ans: The analyzer emits an `ERROR: Undeclared identifier` warning.*
- **Q39: What is the difference between keyword and identifier?**  
  *Ans: Keywords are reserved language words (e.g. `int`, `return`); identifiers are programmer-chosen names.*
- **Q40: Does your hash table allow deleting a symbol?**  
  *Ans: Yes, by splicing the node out of the bucket's linked list.*
- **Q41: How are strings exported?**  
  *Ans: In CSV format via Python's `csv` module and in JSON format via `json.dumps()`.*
- **Q42: What is an activation record?**  
  *Ans: The runtime stack frame corresponding to a function's local scope.*
- **Q43: How does the visualizer highlight search results?**  
  *Ans: By dynamically calculating $h(\text{key})$ and styling the target bucket row with cyan glow borders.*
- **Q44: What is the worst-case space complexity of your hash table?**  
  *Ans: $O(n + m)$, where $n$ is the number of symbols and $m=10$ is the bucket count.*
- **Q45: What is AST?**  
  *Ans: Abstract Syntax Tree, an intermediate tree representation of code syntax.*
- **Q46: Is Flask running asynchronously or synchronously here?**  
  *Ans: Synchronously in WSGI development mode.*
- **Q47: Why is ASCII sum modulo deterministic?**  
  *Ans: The same string will always produce the identical integer sum and index on any machine.*
- **Q48: What is semantic analysis?**  
  *Ans: The compiler phase that checks type compatibility, scope validity, and semantic correctness.*
- **Q49: How are anonymous blocks named?**  
  *Ans: `parent.block.1`, `parent.block.2`, etc.*
- **Q50: Can a symbol table hold functions?**  
  *Ans: Yes, with `token_type = "function"` and `type` representing the return type.*
