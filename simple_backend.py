#!/usr/bin/env python3
"""
Super simple backend for testing JPEG upload
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/api/health':
            response = {"status": "healthy", "message": "Backend is running!"}
            self.wfile.write(json.dumps(response).encode())
        else:
            response = {"error": "Endpoint not found", "path": self.path}
            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/api/detect':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                crop_type = request_data.get('crop_type', 'unknown')
                
                # Mock response for testing
                response = {
                    "success": True,
                    "disease": "Test Detection Result",
                    "confidence": "85",
                    "ai_recommendation": f"This is a test response for your {crop_type.title()} plant. The JPEG upload is working correctly! Your image was processed successfully."
                }
                
                print(f"✅ Processed {crop_type} image successfully")
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            response = {"error": "POST endpoint not found", "path": self.path}
            self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    print("🌱 Simple CropGuard AI Backend")
    print("==============================")
    print("🚀 Starting on http://localhost:8000")
    print("🔍 Health: http://localhost:8000/api/health")
    print("🌱 Detect: http://localhost:8000/api/detect")
    print("🛑 Press Ctrl+C to stop")
    
    server = HTTPServer(('localhost', 8000), SimpleAPIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()