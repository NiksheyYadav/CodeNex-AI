import sys

def main():
    print("This is a test output")
    print("Python version:", sys.version)
    print("Current working directory:", os.getcwd())
    print("Environment variables:")
    for key in os.environ:
        print(f"{key}: {os.environ[key]}")
    
    # Write to a file to verify file system access
    with open("test_output.txt", "w") as f:
        f.write("Test successful!")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    import os
    main()
