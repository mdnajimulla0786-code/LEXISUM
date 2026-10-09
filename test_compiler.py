"""
Comprehensive Automated Test Suite for Compiler Design Symbol Table & Lexical Analyzer.
Covers all 18+ required test cases from Task 17 & Task 18.
"""

import unittest
import json
from hash_table import HashTable
from symbol_table import SymbolTable
from code_analyzer import CodeAnalyzer
from app import app


class TestCompilerDesignProject(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=10)
        self.st = SymbolTable(size=10)
        self.analyzer = CodeAnalyzer()
        self.client = app.test_client()

    # ----------------------------------------------------
    # TEST 1: Insert Symbol
    # ----------------------------------------------------
    def test_01_insert_symbol(self):
        ok, msg = self.st.add_symbol("x", "int", "10", "global", 1)
        self.assertTrue(ok)
        self.assertEqual(self.st.total_symbols, 1)
        self.assertEqual(self.st.global_symbols, 1)

    # ----------------------------------------------------
    # TEST 2: Search Symbol
    # ----------------------------------------------------
    def test_02_search_symbol(self):
        self.st.add_symbol("varA", "float", "3.14", "global", 5)
        found = self.st.search_symbol("varA")
        self.assertIsNotNone(found)
        self.assertEqual(found["name"], "varA")
        self.assertEqual(found["value"], "3.14")
        self.assertIsNone(self.st.search_symbol("nonExistent"))

    # ----------------------------------------------------
    # TEST 3: Update Symbol
    # ----------------------------------------------------
    def test_03_update_symbol(self):
        self.st.add_symbol("count", "int", "0", "global", 2)
        ok, msg = self.st.update_symbol("count", "int", "5", "global", 3)
        self.assertTrue(ok)
        sym = self.st.search_symbol("count")
        self.assertEqual(sym["value"], "5")
        self.assertEqual(sym["line"], 3)

    # ----------------------------------------------------
    # TEST 4: Delete Symbol
    # ----------------------------------------------------
    def test_04_delete_symbol(self):
        self.st.add_symbol("temp", "int", "99", "global", 4)
        ok, msg = self.st.delete_symbol("temp")
        self.assertTrue(ok)
        self.assertIsNone(self.st.search_symbol("temp"))
        self.assertEqual(self.st.total_symbols, 0)

    # ----------------------------------------------------
    # TEST 5: Hash Collision Handling (Separate Chaining)
    # ----------------------------------------------------
    def test_05_collision_handling(self):
        # Two keys that produce the same ASCII sum % 10
        # 'a' = 97 % 10 = 7. 'k' = 107 % 10 = 7.
        idx_a = self.ht.hash_function("a")
        idx_k = self.ht.hash_function("k")
        self.assertEqual(idx_a, idx_k)

        self.ht.insert("a", {"name": "a", "val": 1})
        self.ht.insert("k", {"name": "k", "val": 2})

        # Both should be retrievable without overwriting
        res_a = self.ht.search("a")
        res_k = self.ht.search("k")
        self.assertIsNotNone(res_a)
        self.assertIsNotNone(res_k)
        self.assertEqual(res_a["val"], 1)
        self.assertEqual(res_k["val"], 2)

        # Verify bucket chain length is 2
        state = self.ht.get_table_state()
        bucket_7 = [b for b in state if b["index"] == idx_a][0]
        self.assertEqual(len(bucket_7["chain"]), 2)

    # ----------------------------------------------------
    # TEST 6: Duplicate in Same Scope (Must be rejected)
    # ----------------------------------------------------
    def test_06_duplicate_in_same_scope(self):
        ok1, _ = self.st.add_symbol("x", "int", "10", "main", 1)
        self.assertTrue(ok1)
        ok2, err = self.st.add_symbol("x", "float", "20", "main", 2)
        self.assertFalse(ok2)
        self.assertIn("Duplicate", err)

    # ----------------------------------------------------
    # TEST 7: Same Identifier in Different Scopes (Allowed)
    # ----------------------------------------------------
    def test_07_shadowing_allowed_different_scopes(self):
        ok_global, _ = self.st.add_symbol("x", "int", "10", "global", 1)
        ok_func, _ = self.st.add_symbol("x", "int", "20", "test", 4)
        ok_block, _ = self.st.add_symbol("x", "int", "30", "test.if.1", 7)
        self.assertTrue(ok_global)
        self.assertTrue(ok_func)
        self.assertTrue(ok_block)
        self.assertEqual(self.st.total_symbols, 3)

    # ----------------------------------------------------
    # TEST 8: Global Scope Lookup
    # ----------------------------------------------------
    def test_08_global_lookup(self):
        self.st.add_symbol("g_var", "int", "100", "global", 1)
        # Search from deep inner scope should resolve to global
        found = self.st.lookup("g_var", current_scope="main.if.1.for.1")
        self.assertIsNotNone(found)
        self.assertEqual(found["value"], "100")
        self.assertEqual(found["scope"], "global")

    # ----------------------------------------------------
    # TEST 9: Local Scope Lookup & Nearest Scope Shadowing
    # ----------------------------------------------------
    def test_09_local_lookup_shadowing(self):
        self.st.add_symbol("x", "int", "10", "global", 1)
        self.st.add_symbol("x", "int", "20", "funcA", 5)

        # Lookup from inside funcA returns 20, not 10
        found_local = self.st.lookup("x", current_scope="funcA")
        self.assertIsNotNone(found_local)
        self.assertEqual(found_local["value"], "20")

        # Lookup from global returns 10
        found_global = self.st.lookup("x", current_scope="global")
        self.assertIsNotNone(found_global)
        self.assertEqual(found_global["value"], "10")

    # ----------------------------------------------------
    # TEST 10: Nested Scope Traversal
    # ----------------------------------------------------
    def test_10_nested_scope_traversal(self):
        self.st.add_symbol("fn_var", "float", "2.71", "main", 3)
        # Should resolve fn_var from inner if block
        found = self.st.lookup("fn_var", current_scope="main.if.1")
        self.assertIsNotNone(found)
        self.assertEqual(found["value"], "2.71")

    # ----------------------------------------------------
    # TEST 11: Shadowing Priority Order
    # ----------------------------------------------------
    def test_11_shadowing_priority(self):
        self.st.add_symbol("val", "int", "1", "global", 1)
        self.st.add_symbol("val", "int", "2", "compute", 3)
        self.st.add_symbol("val", "int", "3", "compute.if.1", 6)

        lookup_inner = self.st.lookup("val", "compute.if.1")
        self.assertEqual(lookup_inner["value"], "3")

        lookup_func = self.st.lookup("val", "compute")
        self.assertEqual(lookup_func["value"], "2")

        lookup_glob = self.st.lookup("val", "global")
        self.assertEqual(lookup_glob["value"], "1")

    # ----------------------------------------------------
    # TEST 12: Undeclared Identifier Detection
    # ----------------------------------------------------
    def test_12_undeclared_identifier(self):
        code = """
        int main() {
            int a = 10;
            b = 20;
        }
        """
        res = self.analyzer.analyze(code)
        errors = [e["message"] for e in res["errors"]]
        self.assertTrue(any("b" in err and "Undeclared" in err for err in errors))

    # ----------------------------------------------------
    # TEST 13: Multi-Variable Declarations
    # ----------------------------------------------------
    def test_13_multi_variable_declarations(self):
        code = "int a = 1, b = 2; float x, y, z; char c1 = 'X', c2 = 'Y';"
        res = self.analyzer.analyze(code)
        sym_names = [s["name"] for s in res["symbols"]]
        self.assertIn("a", sym_names)
        self.assertIn("b", sym_names)
        self.assertIn("x", sym_names)
        self.assertIn("y", sym_names)
        self.assertIn("z", sym_names)
        self.assertIn("c1", sym_names)
        self.assertIn("c2", sym_names)
        self.assertEqual(len(res["symbols"]), 7)

    # ----------------------------------------------------
    # TEST 14: Function Parameters Detection
    # ----------------------------------------------------
    def test_14_function_parameters(self):
        code = "void calculate(int x, float y, char grade) {}"
        res = self.analyzer.analyze(code)
        params = [s for s in res["symbols"] if s.get("token_type") == "parameter"]
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0]["name"], "x")
        self.assertEqual(params[0]["scope"], "calculate")
        self.assertEqual(params[1]["name"], "y")
        self.assertEqual(params[2]["name"], "grade")

    # ----------------------------------------------------
    # TEST 15: Nested Braces and Scope Stack Pop
    # ----------------------------------------------------
    def test_15_nested_braces(self):
        code = """
        void test() {
            int outer = 1;
            {
                int inner = 2;
                {
                    int deepest = 3;
                }
            }
            int after = 4;
        }
        """
        res = self.analyzer.analyze(code)
        symbols = {s["name"]: s["scope"] for s in res["symbols"]}
        self.assertEqual(symbols["outer"], "test")
        self.assertEqual(symbols["after"], "test")
        self.assertIn("block", symbols["inner"])
        self.assertIn("block", symbols["deepest"])

    # ----------------------------------------------------
    # TEST 16: Export CSV Endpoint
    # ----------------------------------------------------
    def test_16_export_csv(self):
        self.client.post('/add-symbol', json={"name": "expA", "type": "int", "value": "10", "scope": "global", "line": 1})
        resp = self.client.get('/export/csv')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'text/csv')
        csv_text = resp.data.decode('utf-8')
        self.assertIn("Name,Data Type,Token Type,Value,Scope,Line Number,Hash Index", csv_text)
        self.assertIn("expA", csv_text)

    # ----------------------------------------------------
    # TEST 17: Export JSON Endpoint
    # ----------------------------------------------------
    def test_17_export_json(self):
        self.client.post('/add-symbol', json={"name": "expB", "type": "float", "value": "9.9", "scope": "main", "line": 5})
        resp = self.client.get('/export/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.mimetype, 'application/json')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertTrue(isinstance(data, list))
        names = [item["name"] for item in data]
        self.assertIn("expB", names)

    # ----------------------------------------------------
    # TEST 18: Exact Task 18 Integration Program
    # ----------------------------------------------------
    def test_18_exact_task_18_program(self):
        program = """int globalVar = 10;
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
}"""
        res = self.analyzer.analyze(program)
        self.assertEqual(len(res["errors"]), 0, f"Unexpected errors: {res['errors']}")

        symbols = res["symbols"]
        sym_map = {}
        for s in symbols:
            key = (s["name"], s["scope"])
            sym_map[key] = s

        # Verify Global symbols
        self.assertIn(("globalVar", "global"), sym_map)
        self.assertIn(("pi", "global"), sym_map)
        self.assertIn(("calculate", "global"), sym_map)

        # Verify Function calculate symbols
        self.assertIn(("x", "calculate"), sym_map)
        self.assertIn(("y", "calculate"), sym_map)
        self.assertIn(("result", "calculate"), sym_map)
        self.assertEqual(sym_map[("result", "calculate")]["value"], "0")

        # Verify IF scope symbols
        self.assertIn(("result", "calculate.if.1"), sym_map)
        self.assertEqual(sym_map[("result", "calculate.if.1")]["value"], "20")
        self.assertIn(("afterLoop", "calculate.if.1"), sym_map)

        # Verify FOR scope symbols
        self.assertIn(("i", "calculate.if.1.for.1"), sym_map)
        self.assertIn(("temp", "calculate.if.1.for.1"), sym_map)

        # Verify closing back to calculate function
        self.assertIn(("finalValue", "calculate"), sym_map)

        # Check that both 'result' variables exist and are NOT duplicates
        results = [s for s in symbols if s["name"] == "result"]
        self.assertEqual(len(results), 2)
        scopes = {r["scope"] for r in results}
        self.assertEqual(scopes, {"calculate", "calculate.if.1"})


if __name__ == '__main__':
    unittest.main()
