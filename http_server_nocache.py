#!/usr/bin/env python3
"""
Simple HTTP Server with cache-disabling headers and publish endpoint
Serves files from the current directory and all subdirectories
"""

import http.server
import socketserver
import os
import subprocess
import json
from urllib.parse import parse_qs, urlparse

PORT = 7531
DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that adds cache-disabling headers and handles publish requests"""
    
    def end_headers(self):
        """Add headers to disable caching"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        http.server.SimpleHTTPRequestHandler.end_headers(self)
    
    def do_GET(self):
        """Handle GET requests"""
        # Handle publish endpoint
        if self.path.startswith('/publish'):
            self.handle_publish()
            return
            
        # Handle normal file requests
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def handle_publish(self):
        """Handle publish requests by running the publish.sh script"""
        try:
            # Set response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Run the publish script
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish.sh")
            result = subprocess.run([script_path], 
                                   capture_output=True, 
                                   text=True, 
                                   cwd=os.path.dirname(os.path.abspath(__file__)))
            
            # Prepare response
            response = {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
            # Send response
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            # Handle errors
            error_response = {
                'success': False,
                'error': str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())

def run_server():
    """Run the HTTP server"""
    os.chdir(DOCS_DIR)
    handler = NoCacheHandler
    
    # Create server with address reuse enabled
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"Serving files from: {DOCS_DIR}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
