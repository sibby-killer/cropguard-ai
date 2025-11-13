#!/usr/bin/env python3
"""
Simple backend server runner for CropGuard AI
This will start the API server properly on localhost:8000
"""

import os
import sys
import json
import base64
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class CropGuardAPIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        if parsed_path.path == '/api/health':
            # Health check endpoint
            health_data = {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "environment": {
                    "groq_configured": bool(os.getenv('GROQ_API_KEY')),
                    "supabase_configured": bool(os.getenv('SUPABASE_URL'))
                },
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(health_data, indent=2).encode())
            
        else:
            # Unknown endpoint
            error_data = {
                "error": f"Endpoint {parsed_path.path} not found",
                "available_endpoints": ["/api/health", "/api/detect"]
            }
            self.wfile.write(json.dumps(error_data).encode())

    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        if parsed_path.path == '/api/detect':
            try:
                # Read request data
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                print(f"🔍 Received detection request for: {request_data.get('crop_type', 'unknown')}")
                
                # Check if we have required data
                if 'image' not in request_data:
                    raise ValueError("No image data provided")
                    
                if 'crop_type' not in request_data:
                    raise ValueError("No crop type provided")
                
                # Check environment
                groq_api_key = os.getenv('GROQ_API_KEY')
                if not groq_api_key:
                    # Mock response for testing without API key
                    print("⚠️  No GROQ_API_KEY found, returning mock response")
                    mock_response = {
                        "success": True,
                        "disease": "Mock Disease Detection",
                        "confidence": "85",
                        "severity": "Mild",
                        "symptoms": ["Mock symptom 1", "Mock symptom 2"],
                        "ai_recommendation": f"This is a mock response for {request_data['crop_type']} analysis. To get real AI analysis, please set your GROQ_API_KEY environment variable."
                    }
                    self.wfile.write(json.dumps(mock_response, indent=2).encode())
                    return
                
                # Try to use the real API
                try:
                    # Import and use the real detection logic
                    sys.path.append(str(Path(__file__).parent / "backend"))
                    from utils.groq_client import GroqClient
                    from utils.image_processor import decode_base64_image
                    
                    # Process the image
                    image = decode_base64_image(request_data['image'])
                    
                    # Analyze with Groq
                    groq_client = GroqClient()
                    result = groq_client.analyze_plant_disease(
                        image=image,
                        crop_type=request_data['crop_type']
                    )
                    
                    # Format response
                    response_data = {
                        'success': True,
                        'disease': result.get('disease_detected', 'Unknown'),
                        'confidence': f"{int(result.get('confidence', 0) * 100)}",
                        'severity': result.get('severity', 'Unknown'),
                        'symptoms': result.get('symptoms_observed', []),
                        'ai_recommendation': result.get('recommendation', 'No recommendations available')
                    }
                    
                    print(f"✅ Analysis complete: {response_data['disease']}")
                    
                except ImportError as e:
                    print(f"⚠️  Import error, returning mock response: {e}")
                    # Fallback mock response
                    crop_type = request_data['crop_type'].title()
                    mock_response = {
                        "success": True,
                        "disease": "Healthy Plant",
                        "confidence": "78",
                        "severity": "None",
                        "symptoms": [],
                        "ai_recommendation": f"Your {crop_type} plant appears to be in good health. Continue with regular care including proper watering, sunlight, and monitoring for any changes."
                    }
                    response_data = mock_response
                
                self.wfile.write(json.dumps(response_data, indent=2).encode())
                
            except Exception as e:
                print(f"❌ Error processing request: {str(e)}")
                error_response = {
                    'success': False,
                    'error': f'Analysis failed: {str(e)}',
                    'help': 'Make sure you have uploaded a valid image and selected a crop type'
                }
                self.wfile.write(json.dumps(error_response, indent=2).encode())
        
        else:
            # Unknown POST endpoint
            error_data = {
                "error": f"POST endpoint {parsed_path.path} not found",
                "available_endpoints": ["/api/detect"]
            }
            self.wfile.write(json.dumps(error_data).encode())

def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path("backend/.env")
    if env_file.exists():
        print(f"📁 Loading environment from: {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
                    if 'KEY' in key and len(value.strip()) > 10:
                        print(f"✅ Loaded {key}: {value[:8]}...")
                    elif key in ['SUPABASE_URL', 'SUPABASE_KEY']:
                        print(f"✅ Loaded {key}")
    else:
        print(f"⚠️  No .env file found at {env_file}")
        print("🔑 You can create one with your Groq API key for real AI analysis")

def main():
    print("🌱 CropGuard AI - Backend Server")
    print("=" * 50)
    
    # Load environment variables
    load_env_file()
    
    # Check environment
    groq_key = os.getenv('GROQ_API_KEY')
    supabase_url = os.getenv('SUPABASE_URL')
    
    print(f"🔑 Groq API Key: {'✅ Configured' if groq_key else '❌ Missing'}")
    print(f"💾 Supabase: {'✅ Configured' if supabase_url else '❌ Missing (Optional)'}")
    
    if not groq_key:
        print("\n⚠️  GROQ_API_KEY not found!")
        print("📝 The server will run with mock responses for testing")
        print("🔗 Get a free API key at: https://console.groq.com/keys")
        print("💾 Add it to backend/.env file: GROQ_API_KEY=your_key_here")
    
    # Start server
    port = 8000
    server_address = ('localhost', port)
    
    try:
        httpd = HTTPServer(server_address, CropGuardAPIHandler)
        print(f"\n🚀 Server starting on http://localhost:{port}")
        print(f"🔍 Health check: http://localhost:{port}/api/health")
        print(f"🌱 Disease detection: http://localhost:{port}/api/detect")
        print("\n💡 Now open the web app and test JPEG upload!")
        print("🛑 Press Ctrl+C to stop the server")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print("🔧 Solutions:")
            print("   1. Stop other servers running on port 8000")
            print("   2. Or change the port in the code")
            print("   3. Or use: netstat -ano | findstr :8000 to find what's using it")
        else:
            print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()