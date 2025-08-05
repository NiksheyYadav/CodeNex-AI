import sys
import os
import traceback
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('diagnostic.log')
        ]
    )
    return logging.getLogger(__name__)

def test_imports(logger):
    logger.info("Testing imports...")
    try:
        import fastapi
        import uvicorn
        logger.info(f"FastAPI version: {fastapi.__version__}")
        logger.info(f"Uvicorn version: {uvicorn.__version__}")
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error(traceback.format_exc())
        return False

def test_fastapi(logger):
    logger.info("Testing FastAPI...")
    try:
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/")
        async def root():
            return {"message": "Hello World"}
            
        logger.info("FastAPI app created successfully")
        return app
    except Exception as e:
        logger.error(f"FastAPI error: {e}")
        logger.error(traceback.format_exc())
        return None

def run_server(app, logger):
    if not app:
        logger.error("Cannot run server: No app created")
        return
        
    logger.info("Starting Uvicorn server...")
    try:
        import uvicorn
        uvicorn.run("diagnostic:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.error(f"Uvicorn error: {e}")
        logger.error(traceback.format_exc())

def main():
    logger = setup_logging()
    logger.info("Starting diagnostic...")
    
    # Test Python environment
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python path: {sys.path}")
    
    # Test imports
    if not test_imports(logger):
        logger.error("Failed to import required packages")
        return
    
    # Test FastAPI
    app = test_fastapi(logger)
    if not app:
        logger.error("Failed to create FastAPI app")
        return
    
    # Run the server
    run_server(app, logger)
    
    logger.info("Diagnostic complete")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
