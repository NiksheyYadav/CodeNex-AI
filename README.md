# AI Code Agent

A CLI tool powered by Mistral-7B-v0.1 to generate and manage code projects from natural language prompts.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Configure the model:
   ```bash
   cp config.yaml.example config.yaml
   ```

3. Run the agent:
   ```bash
   python main.py "Create a Flask app with 3 routes"
   ```

## Usage

```bash
python main.py "Create a Flask app with 3 routes"
```

## Project Structure

```
agent/
├── agent/
│   ├── __init__.py
│   ├── main.py
│   ├── prompt_engine.py
│   ├── codegen.py
│   ├── file_ops.py
│   └── utils.py
├── config.yaml
├── memory/
│   └── file_map.json
├── projects/
│   └── generated_project/
│       ├── app.py
│       └── requirements.txt
├── requirements.txt
└── templates/
    ├── flask_app.txt
    └── react_app.txt
```

## License

MIT

## Author
https://github.com/NiksheyYadav
[Your Name](https://github.com/yourusername)

## Version

1.0.0
