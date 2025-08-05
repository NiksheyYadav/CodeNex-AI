import sys
import os

def main():
    print("Python Test Script")
    print("Python version:", sys.version)
    print("Current working directory:", os.getcwd())
    print("Environment variables:")
    for key, value in os.environ.items():
        if 'PYTHON' in key or 'PATH' in key:
            print(f"{key}: {value}")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
