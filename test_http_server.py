import sys
import os
import http.server
import socketserver
import threading
import time

def run_http_server(port=8000):
    """Run a simple HTTP server in a separate thread."""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Hello from test HTTP server!')
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving HTTP on port {port}... (Press Ctrl+C to stop)")
        httpd.serve_forever()

def main():
    print("=== Python Environment Test ===")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    
    # Test file writing
    test_file = "test_http_server_output.txt"
    try:
        with open(test_file, "w") as f:
            f.write("Test successful!")
        print(f"Successfully wrote to {test_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
    
    # Start HTTP server in a separate thread
    port = 8000
    print(f"Starting test HTTP server on port {port}...")
    
    server_thread = threading.Thread(target=run_http_server, args=(port,), daemon=True)
    server_thread.start()
    
    try:
        print("Server is running. Open http://localhost:8000 in your browser.")
        print("Press Ctrl+C to stop the server.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    main()
