"""
Get disease information endpoint
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.disease_info import get_disease_info, search_diseases, DISEASE_DATABASE

class handler(BaseHTTPRequestHandler):
    """Diseases endpoint handler"""
    
    def do_GET(self):
        """Handle GET request for disease info"""
        try:
            from urllib.parse import urlparse, parse_qs
            
            # Parse query parameters
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            disease_name = params.get('name', [None])[0]
            search_query = params.get('search', [None])[0]
            
            # If searching
            if search_query:
                results = search_diseases(search_query)
                response_data = {
                    'success': True,
                    'count': len(results),
                    'diseases': results
                }
            
            # If getting specific disease
            elif disease_name:
                disease_info = get_disease_info(disease_name)
                response_data = {
                    'success': True,
                    'disease': disease_name,
                    **disease_info
                }
            
            # If listing all diseases
            else:
                all_diseases = [
                    {'name': name, **info}
                    for name, info in DISEASE_DATABASE.items()
                ]
                response_data = {
                    'success': True,
                    'count': len(all_diseases),
                    'diseases': all_diseases
                }
            
            self._send_json_response(200, response_data)
        
        except Exception as e:
            print(f"Disease info error: {str(e)}")
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
            'success': False,
            'error': message
        })
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')