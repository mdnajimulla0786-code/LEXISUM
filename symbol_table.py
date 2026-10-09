"""
Symbol Table Manager with Lexical Scoping, Shadowing, and Scope-Aware Lookup.
"""

from hash_table import HashTable


class SymbolTable:
    def __init__(self, size=10):
        self.hash_table = HashTable(size)
        self.total_symbols = 0
        self.global_symbols = 0
        self.local_symbols = 0

    @staticmethod
    def compute_parent_scope(scope):
        """Deduces parent scope from hierarchical naming (e.g. main.if.1 -> main)."""
        if not scope or scope.lower() == "global":
            return None
        parts = scope.rsplit(".", 2)
        if len(parts) >= 2 and parts[-2] in ("if", "for", "while", "block", "switch"):
            # e.g. "calculate.if.1" -> parent is "calculate"
            return scope.rsplit(".", 2)[0]
        if "." in scope:
            return scope.rsplit(".", 1)[0]
        return "global"

    def add_symbol(self, name, datatype, value, scope, line, token_type="identifier", parent_scope=None):
        """
        Inserts a new symbol.
        Duplicate check: Rejected ONLY if the exact same identifier exists in the SAME scope.
        Shadowing across different scopes is allowed.
        """
        # Exact scope duplicate check
        if self.search_symbol(name, scope=scope):
            return False, f"Duplicate identifier '{name}' in scope '{scope}'"

        if parent_scope is None:
            parent_scope = self.compute_parent_scope(scope)

        symbol_data = {
            "name": name,
            "type": datatype,
            "data_type": datatype,
            "token_type": token_type,
            "value": value,
            "scope": scope,
            "parent_scope": parent_scope,
            "line": line,
            "line_number": line,
            "hash_index": self.hash_table.hash_function(name)
        }

        self.hash_table.insert(name, symbol_data)

        self.total_symbols += 1
        if scope.lower() == "global":
            self.global_symbols += 1
        else:
            self.local_symbols += 1

        return True, "Symbol added successfully"

    def search_symbol(self, name, scope=None):
        """Finds symbol by name, optionally filtered by scope."""
        return self.hash_table.search(name, scope=scope)

    def lookup(self, name, current_scope):
        """
        Lexical Scope Lookup Order (Task 6):
        Current Scope -> Parent Scope -> Grandparent Scope -> Global Scope.
        Returns first match found, or None if undeclared.
        """
        curr = current_scope
        visited = set()

        while curr and curr not in visited:
            visited.add(curr)
            found = self.search_symbol(name, scope=curr)
            if found:
                return found
            curr = self.compute_parent_scope(curr)

        # Check global scope as final fallback if not already checked
        if "global" not in visited:
            return self.search_symbol(name, scope="global")

        return None

    def update_symbol(self, name, datatype, value, scope, line, token_type=None):
        """Updates an existing symbol in a given scope."""
        existing = self.search_symbol(name, scope=scope)
        if not existing:
            # Fall back to finding any symbol with matching name
            existing = self.search_symbol(name, scope=None)
            if not existing:
                return False, "Symbol not found"

        old_scope = existing["scope"]
        new_scope = scope if scope else old_scope

        # Adjust scope counts if scope changed
        if old_scope.lower() != new_scope.lower():
            if old_scope.lower() == "global":
                self.global_symbols -= 1
                self.local_symbols += 1
            else:
                self.local_symbols -= 1
                self.global_symbols += 1

        symbol_data = {
            "name": name,
            "type": datatype,
            "data_type": datatype,
            "token_type": token_type or existing.get("token_type", "identifier"),
            "value": value,
            "scope": new_scope,
            "parent_scope": self.compute_parent_scope(new_scope),
            "line": line,
            "line_number": line,
            "hash_index": self.hash_table.hash_function(name)
        }

        # If scope changed, delete old node first to preserve scope index
        if old_scope != new_scope:
            self.hash_table.delete(name, scope=old_scope)

        self.hash_table.insert(name, symbol_data)
        return True, "Symbol updated successfully"

    def delete_symbol(self, name, scope=None):
        """Removes a symbol from the table."""
        existing = self.search_symbol(name, scope=scope)
        if not existing:
            return False, "Symbol not found"

        target_scope = existing.get("scope")
        self.hash_table.delete(name, scope=target_scope)
        self.total_symbols -= 1

        if target_scope and target_scope.lower() == "global":
            self.global_symbols -= 1
        else:
            self.local_symbols -= 1

        return True, "Symbol deleted successfully"

    def clear(self):
        """Resets the symbol table."""
        self.hash_table = HashTable(self.hash_table.size)
        self.total_symbols = 0
        self.global_symbols = 0
        self.local_symbols = 0

    def get_all_symbols(self):
        """Returns flat list of all symbols with hash_index."""
        symbols = self.hash_table.get_all()
        result = []
        for index, sym in symbols:
            sym_copy = sym.copy() if isinstance(sym, dict) else {"name": str(sym)}
            sym_copy["hash_index"] = index
            result.append(sym_copy)
        return result

    def get_stats(self):
        """Returns comprehensive statistics including collisions and load factor."""
        symbols = self.get_all_symbols()
        unique_scopes = set(s.get("scope", "global") for s in symbols)
        if not unique_scopes:
            unique_scopes.add("global")

        state = self.hash_table.get_table_state()
        occupied_buckets = sum(1 for b in state if len(b["chain"]) > 0)
        collisions = sum(1 for b in state if len(b["chain"]) > 1)
        load_factor = round(self.total_symbols / self.hash_table.size, 2) if self.hash_table.size > 0 else 0.0

        return {
            "total": self.total_symbols,
            "global": self.global_symbols,
            "local": self.local_symbols,
            "hash_size": self.hash_table.size,
            "total_scopes": len(unique_scopes),
            "occupied_buckets": occupied_buckets,
            "collisions": collisions,
            "load_factor": load_factor
        }

    def get_hash_table_state(self):
        return self.hash_table.get_table_state()

    def get_scope_hierarchy(self):
        """Builds a tree structure of all scopes and their enclosed symbols."""
        symbols = self.get_all_symbols()
        scopes_dict = {}

        for sym in symbols:
            sc = sym.get("scope", "global")
            if sc not in scopes_dict:
                scopes_dict[sc] = {
                    "scope": sc,
                    "parent": sym.get("parent_scope") or self.compute_parent_scope(sc),
                    "symbols": []
                }
            scopes_dict[sc]["symbols"].append(sym)

        if "global" not in scopes_dict:
            scopes_dict["global"] = {"scope": "global", "parent": None, "symbols": []}

        return scopes_dict