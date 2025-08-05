import ast
import os

def fix_syntax_errors(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        code = f.read()
    try:
        ast.parse(code)
        return None  # No syntax errors
    except SyntaxError as e:
        # Basic syntax error fixes (e.g., missing colons, incorrect indentation)
        lines = code.split("\n")
        error_line = e.lineno - 1
        if "unexpected indent" in str(e).lower():
            lines[error_line] = lines[error_line].lstrip()
        elif "expected ':'" in str(e).lower():
            lines[error_line] = lines[error_line].rstrip() + ":"
        fixed_code = "\n".join(lines)
        try:
            ast.parse(fixed_code)
            return fixed_code
        except SyntaxError:
            return None  # Unable to fix