import sys
import traceback

def main():
    try:
        print("Starting FastAPI server with error capture...")
        import uvicorn
        from fastapi import FastAPI
        
        app = FastAPI()
        
        @app.get("/")
        async def root():
            return {"message": "Hello World"}
            
        print("Starting Uvicorn server...")
        uvicorn.run("run_server:app", host="0.0.0.0", port=8000, reload=True)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nTraceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
