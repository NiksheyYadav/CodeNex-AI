import sys
import os
import uvicorn
from fastapi import FastAPI

def main():
    try:
        print("=== Starting FastAPI Test ===")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        
        # Create a simple FastAPI app
        app = FastAPI()
        
        @app.get("/")
        async def root():
            return {"message": "Hello from FastAPI!"}
        
        print("FastAPI app created successfully")
        print("Starting Uvicorn server...")
        
        # Run the server with explicit host and port
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="debug",
            reload=True
        )
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
