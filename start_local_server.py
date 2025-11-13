#!/usr/bin/env python3
"""
Local development server for CropGuard AI
Starts the backend API with CORS support and serves the web interface
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support"""
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def start_web_server(port=3000):
    """Start the web server for the frontend"""
    print(f"🌐 Starting web server on http://localhost:{port}")
    
    # Change to web directory
    web_dir = Path(__file__).parent / "web"
    if not web_dir.exists():
        print("❌ Web directory not found. Creating basic index.html...")
        web_dir.mkdir(exist_ok=True)
        # Copy local-dev.html as index.html if it doesn't exist
        local_dev_file = web_dir / "local-dev.html"
        index_file = web_dir / "index.html"
        if local_dev_file.exists() and not index_file.exists():
            import shutil
            shutil.copy2(local_dev_file, index_file)
    
    os.chdir(web_dir)
    
    try:
        httpd = HTTPServer(('localhost', port), CORSHTTPRequestHandler)
        httpd.serve_forever()
    except OSError as e:
        print(f"❌ Failed to start web server on port {port}: {e}")
        print(f"🔄 Trying port {port + 1}...")
        start_web_server(port + 1)

def start_backend_server():
    """Start the backend API server"""
    print("🚀 Starting backend API server...")
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    os.chdir(backend_dir)
    
    # Check if requirements are installed
    try:
        import groq
        import supabase
        from PIL import Image
        print("✅ Backend dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("📦 Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Check environment variables
    required_env = ['GROQ_API_KEY']
    missing_env = [var for var in required_env if not os.getenv(var)]
    
    if missing_env:
        print(f"⚠️  Missing environment variables: {missing_env}")
        print("📝 Please create a .env file in the backend directory with:")
        for var in missing_env:
            print(f"   {var}=your_api_key_here")
        print("\n🔑 You can get a Groq API key from: https://console.groq.com/keys")
        
        # Try to load from .env file
        env_file = Path(".env")
        if env_file.exists():
            print("📁 Loading .env file...")
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
    
    # Start the backend server
    try:
        print("🎯 Starting backend on http://localhost:8000")
        subprocess.run([sys.executable, "-m", "http.server", "8000"], cwd="api")
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    
    return True

def main():
    """Main function to start both servers"""
    print("🌱 CropGuard AI - Local Development Server")
    print("=" * 50)
    
    # Create .env file if it doesn't exist
    backend_dir = Path(__file__).parent / "backend"
    env_file = backend_dir / ".env"
    
    if not env_file.exists() and backend_dir.exists():
        print("📝 Creating sample .env file...")
        env_content = """# CropGuard AI Environment Variables
# Get your Groq API key from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Supabase configuration (optional for local development)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created .env file at {env_file}")
        print("🔑 Please edit it with your actual API keys")
    
    try:
        # Start web server in a thread
        web_thread = threading.Thread(target=start_web_server, daemon=True)
        web_thread.start()
        
        # Give web server time to start
        time.sleep(1)
        
        # Open browser
        try:
            webbrowser.open('http://localhost:3000/local-dev.html')
            print("🌐 Opened browser to http://localhost:3000/local-dev.html")
        except:
            print("🌐 Visit http://localhost:3000/local-dev.html in your browser")
        
        print("\n📋 Development URLs:")
        print("   Frontend: http://localhost:3000/local-dev.html")
        print("   Backend:  http://localhost:8000/api/")
        print("   Health:   http://localhost:8000/api/health")
        print("\n💡 Tips:")
        print("   - Use the 'Test Health' button to check API connection")
        print("   - Switch between Local API and Live API as needed")
        print("   - Check browser console for detailed error messages")
        print("\n🛑 Press Ctrl+C to stop servers")
        
        # Start backend server (blocking)
        start_backend_server()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        print("👋 Thanks for using CropGuard AI!")

if __name__ == "__main__":
    main()