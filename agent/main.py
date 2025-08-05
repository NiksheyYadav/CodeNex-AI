import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from agent.prompt_engine import generate_prompt
from agent.codegen import generate_code
from agent.file_ops import save_project_files, load_file_map, update_file_map
from agent.bugfixer import fix_syntax_errors
from agent.utils import load_config

def run_task(task: str, project_dir: str = "projects", fix: bool = False) -> Dict[str, Any]:
    """
    Execute a task with the AI code agent.
    
    Args:
        task: The task description
        project_dir: Directory containing projects
        fix: Whether to fix syntax errors
        
    Returns:
        Dictionary with status, message, and optional file_map
    """
    config = load_config("config.yaml")
    project_path = Path(project_dir) / "generated_project"
    file_map = load_file_map("memory/file_map.json")

    if fix:
        # Extract file path from task (e.g., "Fix syntax error in hello.py")
        file_path = task.split("in")[-1].strip() if "in" in task else "hello.py"
        full_path = project_path / file_path
        
        if not full_path.exists():
            return {
                "status": "error",
                "message": f"File {full_path} does not exist"
            }
            
        fixed_code = fix_syntax_errors(str(full_path))
        if not fixed_code:
            return {
                "status": "warning",
                "message": f"No syntax errors found in {file_path}"
            }
            
        # Update the file with fixed code
        file_map[str(file_path)] = {"status": "fixed"}
        with open(full_path, "w") as f:
            f.write(fixed_code)
            
        update_file_map(file_map, "memory/file_map.json")
        return {
            "status": "success",
            "message": f"Fixed syntax errors in {file_path}",
            "file_map": file_map
        }

    # For generate/edit operations
    prompt = generate_prompt(task, file_map)
    code_response = generate_code(prompt, config)
    
    # Ensure project directory exists
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Save the generated/edited files
    save_project_files(code_response, str(project_path), file_map)
    update_file_map(file_map, "memory/file_map.json")
    
    return {
        "status": "success",
        "message": f"Task completed in {project_path}",
        "file_map": file_map
    }

def get_file_tree(project_dir: str = "projects") -> Dict[str, Any]:
    """
    Get the file tree of the generated project.
    
    Args:
        project_dir: Directory containing projects
        
    Returns:
        Dictionary with status and file tree in a structured format
    """
    project_path = Path(project_dir) / "generated_project"
    
    if not project_path.exists():
        return {
            "status": "success",
            "file_tree": []
        }
    
    def build_tree(directory):
        result = []
        try:
            for item in directory.iterdir():
                if item.name.startswith('.'):
                    continue
                    
                node = {
                    "name": item.name,
                    "path": str(item.relative_to(project_path)),
                    "type": "directory" if item.is_dir() else "file"
                }
                
                if item.is_dir():
                    node["children"] = build_tree(item)
                    
                result.append(node)
        except Exception as e:
            print(f"Error building file tree: {e}")
            
        return result
    
    file_tree = build_tree(project_path)
    
    return {
        "status": "success",
        "file_tree": file_tree
    }

def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="AI Code Agent CLI")
    parser.add_argument(
        "task", 
        nargs="?",
        default="",
        help="Task description (e.g., 'Create a Flask app with 3 routes')"
    )
    parser.add_argument(
        "--project-dir", 
        default="projects", 
        help="Directory to save projects"
    )
    parser.add_argument(
        "--tree", 
        action="store_true", 
        help="Show project file tree"
    )
    parser.add_argument(
        "--fix", 
        action="store_true", 
        help="Fix syntax errors in specified file"
    )
    
    args = parser.parse_args()

    try:
        if args.tree:
            result = get_file_tree(args.project_dir)
            print("Project file tree:")
            print(result["file_tree"])
            return

        if not args.task:
            parser.print_help()
            return

        result = run_task(args.task, args.project_dir, args.fix)
        print(result["message"])
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    code_response = generate_code(prompt, config)
    save_project_files(code_response, project_dir, file_map)
    update_file_map(file_map, "memory/file_map.json")
    print(f"Project generated in {project_dir}")

if __name__ == "__main__":
    main()