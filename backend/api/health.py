"""
Health check endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    """Health check handler"""
    
    def do_GET(self):
        """Handle GET request"""
        try:
            # Check environment variables
            has_groq = bool(os.getenv('GROQ_API_KEY'))
            has_supabase_url = bool(os.getenv('SUPABASE_URL'))
            has_supabase_key = bool(os.getenv('SUPABASE_KEY'))
            
            status = 'healthy' if (has_groq and has_supabase_url and has_supabase_key) else 'degraded'
            
            response_data = {
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'environment': {
                    'groq_configured': has_groq,
                    'supabase_configured': has_supabase_url and has_supabase_key
                },
                'version': '1.0.0'
            }
            
            self._send_json_response(200, response_data)
        
        except Exception as e:
            self._send_error(500, str(e))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self._send_cors_headers()
        self.end_headers()
    
    def _send_json_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, status_code, message):
        """Send error response"""
        self._send_json_response(status_code, {
            'status': 'error',
            'error': message
        })
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')