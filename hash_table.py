"""
Hash Table Implementation using Separate Chaining for Compiler Symbol Table.
Hash Function: sum(ord(c) for c in key) % size
"""

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        """Deterministic ASCII-sum modulo hash function."""
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, value):
        """
        Insert or update a symbol record.
        Uniqueness in separate chaining is governed by (key, scope).
        """
        index = self.hash_function(key)
        target_scope = value.get("scope") if isinstance(value, dict) else None

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            return

        current = self.table[index]
        while True:
            curr_scope = current.value.get("scope") if isinstance(current.value, dict) else None
            # Update if both key and scope match
            if current.key == key and (target_scope is None or curr_scope == target_scope):
                current.value = value
                return
            if current.next is None:
                break
            current = current.next

        current.next = Node(key, value)

    def search(self, key, scope=None):
        """
        Search for a key in the hash table.
        If scope is specified, searches for matching (key, scope).
        If scope is None, returns the first node matching key.
        """
        index = self.hash_function(key)
        current = self.table[index]
        first_match = None

        while current:
            if current.key == key:
                if scope is None:
                    return current.value
                curr_scope = current.value.get("scope") if isinstance(current.value, dict) else None
                if curr_scope == scope:
                    return current.value
                if first_match is None:
                    first_match = current.value
            current = current.next

        return None if scope is not None else first_match

    def delete(self, key, scope=None):
        """
        Delete a symbol record from the hash table.
        If scope is provided, deletes matching (key, scope).
        """
        index = self.hash_function(key)
        current = self.table[index]
        prev = None

        while current:
            curr_scope = current.value.get("scope") if isinstance(current.value, dict) else None
            match = (current.key == key) and (scope is None or curr_scope == scope)

            if match:
                if prev:
                    prev.next = current.next
                else:
                    self.table[index] = current.next
                return True

            prev = current
            current = current.next

        return False

    def get_all(self):
        """Retrieve all stored symbols across all buckets."""
        result = []
        for index in range(self.size):
            current = self.table[index]
            while current:
                result.append((index, current.value))
                current = current.next
        return result

    def get_table_state(self):
        """Returns bucket index, key chains, and detailed node metadata for visualization."""
        state = []
        for i in range(self.size):
            chain = []
            nodes = []
            current = self.table[i]
            while current:
                chain.append(current.key)
                if isinstance(current.value, dict):
                    nodes.append({
                        "name": current.key,
                        "type": current.value.get("type", "id"),
                        "value": current.value.get("value", ""),
                        "scope": current.value.get("scope", "global"),
                        "line": current.value.get("line", 1)
                    })
                else:
                    nodes.append({"name": current.key, "type": "id", "value": "", "scope": "global", "line": 1})
                current = current.next
            state.append({
                "index": i,
                "chain": chain,
                "nodes": nodes
            })
        return state