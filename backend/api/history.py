"""
Get user scan history endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from supabase import create_client

# Initialize Supabase
try:
    supabase = create_client(
        os.getenv("SUPABASE_URL", ""),
        os.getenv("SUPABASE_KEY", "")
    )
except Exception as e:
    print(f"Supabase init error: {str(e)}")
    supabase = None

class handler(BaseHTTPRequestHandler):
    """History endpoint handler"""
    
    def do_GET(self):
        """Handle GET request for scan history"""
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            user_id = params.get('user_id', [None])[0]
            limit = int(params.get('limit', [50])[0])
            
            if not user_id:
                self._send_error(400, "user_id parameter required")
                return
            
            if not supabase:
                self._send_error(500, "Database not available")
                return
            
            # Query database
            result = supabase.table('scans') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .limit(limit) \
                .execute()
            
            scans = result.data if result.data else []
            
            # Prepare response
            response_data = {
                'success': True,
                'count': len(scans),
                'scans': scans
            }
            
            self._send_json_response(200, response_data)
        
        except Exception as e:
            print(f"History error: {str(e)}")
            self._send_error(500, f"Failed to fetch history: {str(e)}")
    
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
            'success': False,
            'error': message
        })
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')