# analyzers/ast_scanner.py
import ast

class PythonASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        # Пример: ищем вызовы eval и exec
        if isinstance(node.func, ast.Name) and node.func.id in ["eval", "exec"]:
            self.findings.append({
                "type": f"Опасный вызов {node.func.id}",
                "line": node.lineno,
                "code": ast.unparse(node) if hasattr(ast, "unparse") else ""
            })
        self.generic_visit(node)

def analyze_python_file(file_path):
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=file_path)
        analyzer = PythonASTAnalyzer()
        analyzer.visit(tree)
        findings.extend(analyzer.findings)
    except Exception as e:
        print(f"Ошибка анализа {file_path}: {e}")
    return findings
