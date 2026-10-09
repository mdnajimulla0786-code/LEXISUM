import csv
import io
import json
from flask import Flask, request, jsonify, render_template, Response
from symbol_table import SymbolTable
from code_analyzer import CodeAnalyzer

app = Flask(__name__)
sym_table = SymbolTable(size=10)
analyzer = CodeAnalyzer()

# ----------------------------------------------------
# HTML Pages Routes
# ----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols-page')
def symbols_page():
    return render_template('symbols.html')

@app.route('/add-page')
def add_page():
    return render_template('add.html')

@app.route('/hashing-page')
def hashing_page():
    return render_template('hashing.html')

@app.route('/scope-page')
def scope_page():
    return render_template('scope.html')

@app.route('/analyzer-page')
def analyzer_page():
    return render_template('analyzer.html')

# ----------------------------------------------------
# REST API Endpoints
# ----------------------------------------------------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(sym_table.get_stats())

@app.route('/symbols', methods=['GET'])
def get_symbols():
    return jsonify(sym_table.get_all_symbols())

@app.route('/add-symbol', methods=['POST'])
def add_symbol():
    data = request.json or {}
    name = data.get('name')
    datatype = data.get('type') or data.get('data_type', 'int')
    value = data.get('value', 'null')
    scope = data.get('scope', 'global')
    line = int(data.get('line', 1))
    token_type = data.get('token_type', 'identifier')

    if not name:
        return jsonify({"error": "Identifier name is required"}), 400

    success, msg = sym_table.add_symbol(
        name=name,
        datatype=datatype,
        value=value,
        scope=scope,
        line=line,
        token_type=token_type
    )
    if success:
        return jsonify({"message": msg}), 201
    return jsonify({"error": msg}), 400

@app.route('/search/<name>', methods=['GET'])
def search_symbol(name):
    scope = request.args.get('scope')
    if scope:
        # Lexical scope-aware lookup
        symbol = sym_table.lookup(name, current_scope=scope)
    else:
        symbol = sym_table.search_symbol(name)

    if symbol:
        return jsonify({"found": True, "symbol": symbol})
    return jsonify({"found": False, "message": f"Undeclared identifier '{name}'"}), 404

@app.route('/update/<name>', methods=['PUT'])
def update_symbol(name):
    data = request.json or {}
    datatype = data.get('type') or data.get('data_type', 'int')
    value = data.get('value', '')
    scope = data.get('scope', 'global')
    line = int(data.get('line', 1))
    token_type = data.get('token_type')

    success, msg = sym_table.update_symbol(
        name=name,
        datatype=datatype,
        value=value,
        scope=scope,
        line=line,
        token_type=token_type
    )
    if success:
        return jsonify({"message": msg}), 200
    return jsonify({"error": msg}), 400

@app.route('/delete/<name>', methods=['DELETE'])
def delete_symbol(name):
    scope = request.args.get('scope')
    success, msg = sym_table.delete_symbol(name, scope=scope)
    if success:
        return jsonify({"message": msg}), 200
    return jsonify({"error": msg}), 404

@app.route('/api/clear', methods=['POST'])
def clear_table():
    sym_table.clear()
    return jsonify({"message": "Symbol table cleared successfully"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json or {}
    code = data.get('code', '')
    if data.get('clear', False):
        sym_table.clear()

    analysis_res = analyzer.analyze(code)
    symbols = analysis_res['symbols']
    tokens = analysis_res['tokens']
    errors = analysis_res['errors']

    added_count = 0
    for sym in symbols:
        success, _ = sym_table.add_symbol(
            name=sym['name'],
            datatype=sym['type'],
            value=sym['value'],
            scope=sym['scope'],
            line=sym['line'],
            token_type=sym.get('token_type', 'identifier')
        )
        if success:
            added_count += 1

    return jsonify({
        "symbols": symbols,
        "tokens": tokens,
        "errors": errors,
        "message": f"Detected {len(symbols)} symbols, {len(tokens)} tokens ({len(errors)} error{'s' if len(errors) != 1 else ''}). Added {added_count} to symbol table."
    })

@app.route('/hash-table', methods=['GET'])
def get_hash_table():
    return jsonify({
        "size": sym_table.hash_table.size,
        "state": sym_table.get_hash_table_state()
    })

@app.route('/api/scopes', methods=['GET'])
def get_scopes():
    return jsonify(sym_table.get_scope_hierarchy())

# ----------------------------------------------------
# Export Endpoints (Task 13)
# ----------------------------------------------------
@app.route('/export/csv', methods=['GET'])
def export_csv():
    symbols = sym_table.get_all_symbols()
    output = io.StringIO()
    writer = csv.writer(output)

    # Header columns as required by Task 13
    writer.writerow([
        "Name", "Data Type", "Token Type", "Value", "Scope", "Line Number", "Hash Index"
    ])

    for sym in symbols:
        writer.writerow([
            sym.get("name", ""),
            sym.get("type") or sym.get("data_type", ""),
            sym.get("token_type", "identifier"),
            sym.get("value", ""),
            sym.get("scope", "global"),
            sym.get("line") or sym.get("line_number", 1),
            sym.get("hash_index", 0)
        ])

    csv_data = output.getvalue()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=symbol_table.csv"}
    )

@app.route('/export/json', methods=['GET'])
def export_json():
    symbols = sym_table.get_all_symbols()
    formatted = []
    for sym in symbols:
        formatted.append({
            "name": sym.get("name", ""),
            "data_type": sym.get("type") or sym.get("data_type", ""),
            "token_type": sym.get("token_type", "identifier"),
            "value": sym.get("value", ""),
            "scope": sym.get("scope", "global"),
            "line_number": sym.get("line") or sym.get("line_number", 1),
            "hash_index": sym.get("hash_index", 0)
        })

    json_data = json.dumps(formatted, indent=2)
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=symbol_table.json"}
    )

if __name__ == '__main__':
    app.run(debug=True)