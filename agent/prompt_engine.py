def generate_prompt(task, file_map):
    base_prompt = """
You are a coding assistant using Llama-3.1-Nemotron-70B-Instruct. Generate or edit production-ready code based on the user task.
- For new code, return the complete code with file structure.
- For editing, modify only the specified file and preserve existing content unless instructed otherwise.
- For bug fixing, return corrected code for the specified file.
- Support templates for Flask and FastAPI projects.
- Return only the code and file structure in the format below.
- Do not include explanations or comments unless explicitly requested.
- Use proper file paths for a project directory.

Format:
FILE: <file_path>
```<language>
<code>
"""