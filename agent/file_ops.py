import os
import json
import ast

def save_project_files(files, project_dir, file_map):
    os.makedirs(project_dir, exist_ok=True)
    for file_info in files:
        file_path = os.path.join(project_dir, file_info["path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if os.path.exists(file_path) and file_info.get("task") == "edit":
            with open(file_path, "r") as f:
                existing_content = f.read()
            try:
                # Parse existing code with AST
                existing_ast = ast.parse(existing_content)
                new_content = file_info["code"]
                new_ast = ast.parse(new_content)
                # Merge: append new functions to existing code
                existing_functions = {n.name for n in existing_ast.body if isinstance(n, ast.FunctionDef)}
                new_functions = [n for n in new_ast.body if isinstance(n, ast.FunctionDef) and n.name not in existing_functions]
                if new_functions:
                    existing_ast.body.extend(new_functions)
                    merged_code = ast.unparse(existing_ast)
                    with open(file_path, "w") as f:
                        f.write(merged_code)
                    file_map[file_info["path"]] = {"status": "edited"}
                else:
                    with open(file_path, "w") as f:
                        f.write(new_content)
                    file_map[file_info["path"]] = {"status": "edited"}
            except SyntaxError:
                # Fallback to overwrite if AST parsing fails
                with open(file_path, "w") as f:
                    f.write(file_info["code"])
                file_map[file_info["path"]] = {"status": "edited"}
        else:
            with open(file_path, "w") as f:
                f.write(file_info["code"])
            file_map[file_info["path"]] = {"status": "created"}

def load_file_map(file_map_path):
    if os.path.exists(file_map_path) and os.path.getsize(file_map_path) > 0:
        try:
            with open(file_map_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def update_file_map(file_map, file_map_path):
    os.makedirs(os.path.dirname(file_map_path), exist_ok=True)
    with open(file_map_path, "w") as f:
        json.dump(file_map, f, indent=4)