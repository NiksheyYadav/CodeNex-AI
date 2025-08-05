from typing import List, Dict
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def generate_code(prompt, config):
    """
    Generate code based on the given prompt and configuration.
    
    Args:
        prompt: The prompt to generate code from
        config: Configuration dictionary containing model settings
        
    Returns:
        List of dictionaries containing file paths and their generated code
    """
    if not prompt or not isinstance(prompt, str) or not prompt.strip():
        print("Error: Prompt cannot be None or empty")
        return []
        
    model_name = config.get("model", "mistralai/Mistral-7B-v0.1")
    use_mock = config.get("use_mock", True)  # Default to mock for now
    
    # If we're not using mock and transformers is available, try to use the real model
    if not use_mock and TRANSFORMERS_AVAILABLE:
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
            outputs = model.generate(
                **inputs,
                max_new_tokens=1000,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return parse_code_response(response)
            
        except Exception as e:
            print(f"Warning: Failed to generate code with {model_name}: {str(e)}")
            print("Falling back to mock response...")
    
    # Use mock response based on task
    print(f"Using mock response for prompt: {prompt[:100]}...")
    
    # Check for different types of tasks to provide appropriate mock responses
    task = prompt.lower()
    
    # Flask app generation
    if "flask" in task:
        mock_response = """
FILE: app.py
```python
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        return jsonify({"status": "Item created"}), 201
    return jsonify([{"id": 1, "name": "Sample Item"}])

if __name__ == '__main__':
    app.run(debug=True)
```

FILE: requirements.txt
```
flask==2.0.1
python-dotenv==0.19.0
```

FILE: templates/index.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask App</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-6">Welcome to Flask App</h1>
        <div id="content" class="bg-white p-6 rounded-lg shadow">
            <p>Loading data from API...</p>
        </div>
    </div>
    <script>
        // Fetch data from the API
        fetch('/api/hello')
            .then(response => response.json())
            .then(data => {
                document.getElementById('content').innerHTML = 
                    `<p class="text-green-600">${data.message}</p>`;
            });
    </script>
</body>
</html>
```
"""
    # FastAPI app generation
    elif "fastapi" in task:
        mock_response = """
FILE: main.py
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

items = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

FILE: requirements.txt
```
fastapi==0.68.0
uvicorn==0.15.0
pydantic==1.8.2
```
"""
    # Basic Python script
    elif any(keyword in task for keyword in ["script", "function", "calculate"]):
        mock_response = """
FILE: main.py
```python
def main():
    print("Hello, World!")
    
    # Example function based on the task
    if "calculate" in """ + task.lower() + """:
        result = 42  # Example calculation
        print(f"The answer is: {result}")
        return result

if __name__ == "__main__":
    main()
```
"""
    # Default response
    else:
        mock_response = """
FILE: main.py
```python
# This is a generated Python script
# TODO: Add your code here

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
```
"""
    
    return parse_code_response(mock_response)

def parse_code_response(response: str) -> List[Dict[str, str]]:
    """
    Parse the response from the code generation into a list of files.
    
    Args:
        response: The raw response string from the model
        
    Returns:
        List of dictionaries containing file paths and their code
    """
    files = []
    current_file = None
    current_code = []
    in_code_block = False
    
    for line in response.split("\n"):
        if line.startswith("FILE:"):
            # Save the previous file if it exists
            if current_file and current_code:
                files.append({
                    "path": current_file.strip(),
                    "code": "\n".join(current_code).strip(),
                    "task": "edit" if any(keyword in response.lower() 
                                      for keyword in ["add", "edit", "update", "modify", "fix"]) 
                            else "create"
                })
            # Start a new file
            current_file = line.replace("FILE:", "").strip()
            current_code = []
            in_code_block = False
        elif line.strip() == "```" or line.strip().startswith("```"):
            in_code_block = not in_code_block
        elif in_code_block or (line.strip() and not line.startswith("```")):
            current_code.append(line)
    
    # Add the last file if it exists
    if current_file and current_code:
        files.append({
            "path": current_file.strip(),
            "code": "\n".join(current_code).strip(),
            "task": "edit" if any(keyword in response.lower() 
                               for keyword in ["add", "edit", "update", "modify", "fix"]) 
                    else "create"
        })
    
    return files