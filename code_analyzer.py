"""
Compiler Design Lexical & Semantic Analyzer.
Features:
- Complete tokenization (Keywords, Identifiers, Constants, Strings, Operators, Separators)
- Accurate scope stack and nested block management ({ ... })
- Multi-variable declarations (int a = 1, b = 2;)
- Function declarations and parameter detection
- Lexical scoping & shadowing support
- Compiler error reporting (duplicate in same scope, undeclared identifier, invalid identifier)
"""

import re


class CodeAnalyzer:
    KEYWORDS = {
        "int", "float", "double", "char", "void",
        "if", "else", "for", "while", "return",
        "break", "continue", "switch", "case", "default",
        "struct", "true", "false"
    }

    DATA_TYPES = {"int", "float", "double", "char", "void"}

    OPERATORS = {
        "==", "!=", "<=", ">=", "&&", "||", "++", "--",
        "+=", "-=", "*=", "/=", "=", "+", "-", "*", "/", "%",
        "<", ">", "!", "&", "|"
    }

    SEPARATORS = {"(", ")", "{", "}", "[", "]", ";", ","}

    def __init__(self):
        # Regular expressions for tokenizing
        self.comment_regex = re.compile(r'//.*?$|/\*.*?\*/', re.DOTALL | re.MULTILINE)

    def tokenize(self, code):
        """
        Lexical Analysis: Scans C code into categorized tokens with line numbers.
        Returns: (tokens, lexical_errors)
        """
        tokens = []
        errors = []

        # Token specification regex
        token_spec = [
            ("STRING", r'"([^"\\]|\\.)*"'),
            ("CHAR", r"'([^'\\]|\\.)'"),
            ("INVALID_ID", r'\b\d+[a-zA-Z_]\w*\b'),
            ("FLOAT", r'\b\d+\.\d+\b'),
            ("INTEGER", r'\b\d+\b'),
            ("IDENTIFIER", r'\b[a-zA-Z_]\w*\b'),
            ("OPERATOR", r'==|!=|<=|>=|&&|\|\||\+\+|--|\+=|-=|\*=|/=|[-+*/%=<>!&|]'),
            ("SEPARATOR", r'[(){}\[\];,]'),
            ("WHITESPACE", r'[ \t]+'),
            ("NEWLINE", r'\n'),
            ("MISMATCH", r'.')
        ]

        tok_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec))
        
        # Split into lines and track exact positions
        lines = code.split('\n')
        line_num = 1
        
        for i, line_content in enumerate(lines):
            line_num = i + 1
            # Strip inline comments for this line if present
            clean_line = re.sub(r'//.*$', '', line_content)
            
            for mo in tok_regex.finditer(clean_line):
                kind = mo.lastgroup
                val = mo.group()

                if kind in ("WHITESPACE", "NEWLINE"):
                    continue
                elif kind == "INVALID_ID":
                    errors.append({
                        "type": "invalid_identifier",
                        "message": f"ERROR: Invalid identifier '{val}' at line {line_num}",
                        "line": line_num,
                        "token": val
                    })
                    tokens.append({"token": val, "type": "INVALID_ID", "line": line_num})
                elif kind == "IDENTIFIER":
                    if val in self.KEYWORDS:
                        tokens.append({"token": val, "type": "KEYWORD", "line": line_num})
                    else:
                        tokens.append({"token": val, "type": "IDENTIFIER", "line": line_num})
                elif kind == "FLOAT":
                    tokens.append({"token": val, "type": "FLOAT", "line": line_num})
                elif kind == "INTEGER":
                    tokens.append({"token": val, "type": "INTEGER", "line": line_num})
                elif kind == "STRING":
                    tokens.append({"token": val, "type": "STRING", "line": line_num})
                elif kind == "CHAR":
                    tokens.append({"token": val, "type": "CHARACTER", "line": line_num})
                elif kind == "OPERATOR":
                    tokens.append({"token": val, "type": "OPERATOR", "line": line_num})
                elif kind == "SEPARATOR":
                    tokens.append({"token": val, "type": "SEPARATOR", "line": line_num})
                elif kind == "MISMATCH":
                    # Unknown character
                    errors.append({
                        "type": "lexical_error",
                        "message": f"ERROR: Unrecognized token '{val}' at line {line_num}",
                        "line": line_num,
                        "token": val
                    })

        return tokens, errors

    def analyze(self, code):
        """
        Performs full Lexical & Syntax/Scope analysis on C code.
        Returns:
            {
                "tokens": list of tokens,
                "symbols": list of extracted symbols,
                "errors": list of compiler errors (duplicate, undeclared, etc.)
            }
        """
        tokens, lexical_errors = self.tokenize(code)
        symbols = []
        errors = list(lexical_errors)

        # Scope management stack: Global is base
        scope_stack = ["global"]
        scope_counters = {}  # Tracks numbering e.g. "calculate.if": 1

        def enter_subscope(scope_type):
            parent = scope_stack[-1]
            key = f"{parent}.{scope_type}"
            scope_counters[key] = scope_counters.get(key, 0) + 1
            new_scope = f"{key}.{scope_counters[key]}"
            return new_scope

        # Tracks declared identifiers per scope for duplicate checking
        # dict: (name, scope) -> symbol_dict
        declared_in_scope = set()
        all_declared_names = set()

        def is_visible(name, from_scope):
            """Checks if an identifier is declared in current or any parent scope."""
            curr = from_scope
            while curr:
                if (name, curr) in declared_in_scope:
                    return True
                # Parent lookup
                if "." in curr:
                    parts = curr.rsplit(".", 2)
                    if len(parts) >= 2 and parts[-2] in ("if", "for", "while", "block"):
                        curr = curr.rsplit(".", 2)[0]
                    else:
                        curr = curr.rsplit(".", 1)[0]
                elif curr != "global":
                    curr = "global"
                else:
                    break
            return False

        # State tracking during token stream processing
        i = 0
        n = len(tokens)
        pending_scope = None
        for_awaiting_brace = False

        while i < n:
            tok = tokens[i]
            t_val = tok["token"]
            t_type = tok["type"]
            t_line = tok["line"]

            # ----------------------------------------------------
            # 1. SCOPE OPEN / CLOSE BRACES
            # ----------------------------------------------------
            if t_val == "{":
                if for_awaiting_brace:
                    for_awaiting_brace = False
                elif pending_scope:
                    scope_stack.append(pending_scope)
                    pending_scope = None
                else:
                    # Anonymous block
                    anon_scope = enter_subscope("block")
                    scope_stack.append(anon_scope)
                i += 1
                continue

            if t_val == "}":
                if len(scope_stack) > 1:
                    scope_stack.pop()
                pending_scope = None
                for_awaiting_brace = False
                i += 1
                continue

            # ----------------------------------------------------
            # 2. CONTROL FLOW SCOPES (IF, FOR, WHILE)
            # ----------------------------------------------------
            if t_val in ("if", "while") and t_type == "KEYWORD":
                # Next opening brace will trigger this subscope
                sub = enter_subscope(t_val)
                pending_scope = sub
                i += 1
                continue

            if t_val == "for" and t_type == "KEYWORD":
                # For loops create their scope immediately at the header (for int i = 0...)
                for_scope = enter_subscope("for")
                scope_stack.append(for_scope)
                pending_scope = None
                for_awaiting_brace = True

                i += 1
                # Parse through header: for ( ... )
                if i < n and tokens[i]["token"] == "(":
                    i += 1
                    # Check if there is a variable declaration inside for header: for (int i = 0; ...)
                    if i < n and tokens[i]["token"] in self.DATA_TYPES:
                        decl_type = tokens[i]["token"]
                        i += 1
                        # Parse loop variable(s) up to semicolon
                        while i < n and tokens[i]["token"] != ";":
                            if tokens[i]["type"] == "IDENTIFIER":
                                var_name = tokens[i]["token"]
                                var_line = tokens[i]["line"]
                                var_val = ""
                                i += 1
                                if i < n and tokens[i]["token"] == "=":
                                    i += 1
                                    val_tokens = []
                                    while i < n and tokens[i]["token"] not in (";", ","):
                                        val_tokens.append(tokens[i]["token"])
                                        i += 1
                                    var_val = " ".join(val_tokens)

                                # Register variable in for scope
                                if (var_name, for_scope) in declared_in_scope:
                                    errors.append({
                                        "type": "duplicate",
                                        "message": f"ERROR: Duplicate identifier '{var_name}' in scope '{for_scope}' at line {var_line}",
                                        "line": var_line,
                                        "name": var_name,
                                        "scope": for_scope
                                    })
                                else:
                                    declared_in_scope.add((var_name, for_scope))
                                    all_declared_names.add(var_name)
                                    symbols.append({
                                        "name": var_name,
                                        "type": decl_type,
                                        "token_type": "identifier",
                                        "value": var_val if var_val else "null",
                                        "scope": for_scope,
                                        "line": var_line
                                    })
                                continue
                            i += 1
                continue

            # ----------------------------------------------------
            # 3. FUNCTION DECLARATIONS & PARAMETERS
            # ----------------------------------------------------
            # Lookahead check for function pattern: <TYPE> <IDENTIFIER> (
            if (t_val in self.DATA_TYPES and t_type == "KEYWORD" and 
                i + 2 < n and tokens[i + 1]["type"] == "IDENTIFIER" and tokens[i + 2]["token"] == "("):
                
                ret_type = t_val
                func_name = tokens[i + 1]["token"]
                func_line = tokens[i + 1]["line"]
                func_scope = scope_stack[-1]

                # Record function in current scope (global)
                if (func_name, func_scope) in declared_in_scope:
                    errors.append({
                        "type": "duplicate",
                        "message": f"ERROR: Duplicate identifier '{func_name}' in scope '{func_scope}' at line {func_line}",
                        "line": func_line,
                        "name": func_name,
                        "scope": func_scope
                    })
                else:
                    declared_in_scope.add((func_name, func_scope))
                    all_declared_names.add(func_name)
                    symbols.append({
                        "name": func_name,
                        "type": ret_type,
                        "token_type": "function",
                        "value": "",
                        "scope": func_scope,
                        "line": func_line
                    })

                # Parameters belong to the function scope
                i += 3  # Move past <type>, <name>, '('
                param_scope = func_name
                pending_scope = func_name

                # Parse parameters inside ( ... )
                while i < n and tokens[i]["token"] != ")":
                    if tokens[i]["token"] in self.DATA_TYPES:
                        p_type = tokens[i]["token"]
                        i += 1

                        # Skip pointer asterisks if any: char *argv[]
                        while i < n and tokens[i]["token"] == "*":
                            p_type += "*"
                            i += 1

                        if i < n and tokens[i]["type"] == "IDENTIFIER":
                            p_name = tokens[i]["token"]
                            p_line = tokens[i]["line"]
                            i += 1

                            # Check for array brackets: argv[]
                            while i < n and tokens[i]["token"] == "[":
                                p_type += "[]"
                                while i < n and tokens[i]["token"] != "]":
                                    i += 1
                                if i < n and tokens[i]["token"] == "]":
                                    i += 1

                            # Add parameter
                            if (p_name, param_scope) in declared_in_scope:
                                errors.append({
                                    "type": "duplicate",
                                    "message": f"ERROR: Duplicate parameter '{p_name}' in function '{param_scope}' at line {p_line}",
                                    "line": p_line,
                                    "name": p_name,
                                    "scope": param_scope
                                })
                            else:
                                declared_in_scope.add((p_name, param_scope))
                                all_declared_names.add(p_name)
                                symbols.append({
                                    "name": p_name,
                                    "type": p_type,
                                    "token_type": "parameter",
                                    "value": "",
                                    "scope": param_scope,
                                    "line": p_line
                                })
                            continue
                    i += 1

                if i < n and tokens[i]["token"] == ")":
                    i += 1
                continue

            # ----------------------------------------------------
            # 4. VARIABLE DECLARATIONS (Multi-variable supported)
            # ----------------------------------------------------
            if t_val in self.DATA_TYPES and t_type == "KEYWORD":
                decl_type = t_val
                decl_line = t_line
                curr_scope = scope_stack[-1]
                i += 1

                # Parse comma-separated list of declarators until ';'
                while i < n and tokens[i]["token"] != ";":
                    # Handle pointer symbol if any
                    full_type = decl_type
                    while i < n and tokens[i]["token"] == "*":
                        full_type += "*"
                        i += 1

                    if i < n and tokens[i]["type"] == "IDENTIFIER":
                        var_name = tokens[i]["token"]
                        var_line = tokens[i]["line"]
                        var_val = ""
                        i += 1

                        # Handle array notation e.g. arr[10]
                        while i < n and tokens[i]["token"] == "[":
                            full_type += "[]"
                            while i < n and tokens[i]["token"] != "]":
                                i += 1
                            if i < n and tokens[i]["token"] == "]":
                                i += 1

                        # Check for initialization: = value
                        if i < n and tokens[i]["token"] == "=":
                            i += 1
                            val_tokens = []
                            paren_depth = 0
                            while i < n:
                                if tokens[i]["token"] == "(":
                                    paren_depth += 1
                                elif tokens[i]["token"] == ")":
                                    paren_depth -= 1
                                elif tokens[i]["token"] in (";", ",") and paren_depth <= 0:
                                    break
                                val_tokens.append(tokens[i]["token"])
                                i += 1
                            var_val = " ".join(val_tokens)

                        # Scope duplicate validation (Task 5):
                        # Duplicate ONLY if same identifier in same scope
                        if (var_name, curr_scope) in declared_in_scope:
                            errors.append({
                                "type": "duplicate",
                                "message": f"ERROR: Duplicate identifier '{var_name}' in scope '{curr_scope}' at line {var_line}",
                                "line": var_line,
                                "name": var_name,
                                "scope": curr_scope
                            })
                        else:
                            declared_in_scope.add((var_name, curr_scope))
                            all_declared_names.add(var_name)
                            symbols.append({
                                "name": var_name,
                                "type": full_type,
                                "token_type": "identifier",
                                "value": var_val if var_val else "null",
                                "scope": curr_scope,
                                "line": var_line
                            })

                        # Next token should be ',' or ';'
                        if i < n and tokens[i]["token"] == ",":
                            i += 1
                            continue
                        elif i < n and tokens[i]["token"] == ";":
                            break
                    else:
                        i += 1

                if i < n and tokens[i]["token"] == ";":
                    i += 1
                continue

            # ----------------------------------------------------
            # 5. SEMANTIC CHECK: UNDECLARED IDENTIFIER
            # ----------------------------------------------------
            if t_type == "IDENTIFIER":
                # Identifier used in expression/statement
                curr_scope = scope_stack[-1]
                # If not declared in scope hierarchy, record error
                if not is_visible(t_val, curr_scope):
                    # Check if next token is '(' - might be an external function call like printf
                    is_func_call = (i + 1 < n and tokens[i + 1]["token"] == "(")
                    if not is_func_call:
                        errors.append({
                            "type": "undeclared",
                            "message": f"ERROR: Undeclared identifier '{t_val}' at line {t_line}",
                            "line": t_line,
                            "name": t_val
                        })

            i += 1

        return {
            "tokens": tokens,
            "symbols": symbols,
            "errors": errors
        }