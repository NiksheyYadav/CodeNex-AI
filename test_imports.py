import sys
print("Python path:", sys.path)

try:
    from agent.prompt_engine import generate_prompt
    print("Successfully imported generate_prompt")
except ImportError as e:
    print(f"Error importing generate_prompt: {e}")

try:
    from agent.codegen import generate_code
    print("Successfully imported generate_code")
except ImportError as e:
    print(f"Error importing generate_code: {e}")

# Add the project root to the Python path
import os
sys.path.insert(0, os.path.abspath('.'))

print("\nAfter adding project root to path:")
try:
    from agent.prompt_engine import generate_prompt
    print("Successfully imported generate_prompt")
except ImportError as e:
    print(f"Error importing generate_prompt: {e}")
