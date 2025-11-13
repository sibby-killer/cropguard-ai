"""
Disease Detection API Endpoint
Analyzes plant images using Groq AI and returns disease information
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_processor import decode_base64_image, preprocess_image, validate_image, enhance_image
from utils.groq_client import GroqDiseaseDetector
from utils.disease_info import get_disease_info
from supabase import create_client

# Initialize clients
try:
    supabase = create_client(
        os.getenv("SUPABASE_URL", ""),
        os.getenv("SUPABASE_KEY", "")
    )
    detector = GroqDiseaseDetector()
except Exception as e:
    print(f"Initialization error: {str(e)}")
    supabase = None
    detector = None

class handler(BaseHTTPRequestHandler):
    """Main detection endpoint handler"""
    
    def do_POST(self):
        """Handle POST request for disease detection"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            # Extract parameters
            image_data = data.get('image', '')
            user_id = data.get('user_id')
            crop_type = data.get('crop_type', 'tomato').lower()
            
            # Validate input
            if not image_data:
                self._send_error(400, "No image provided")
                return
            
            print(f"Processing image for crop: {crop_type}")
            
            # Decode and validate image
            try:
                image = decode_base64_image(image_data)
                is_valid, error_msg = validate_image(image)
                
                if not is_valid:
                    self._send_error(400, f"Invalid image: {error_msg}")
                    return
                
                print(f"Image validated: {image.size}")
            
            except Exception as e:
                self._send_error(400, f"Image processing failed: {str(e)}")
                return
            
            # Enhance and preprocess image
            try:
                enhanced_image = enhance_image(image)
                processed_image = preprocess_image(enhanced_image)
                print("Image preprocessing complete")
            except Exception as e:
                print(f"Enhancement failed: {str(e)}, using original")
                processed_image = preprocess_image(image)
            
            # Detect disease using Groq AI
            try:
                if detector is None:
                    raise Exception("Groq detector not initialized")
                
                # Get base64 of processed image
                from utils.image_processor import image_to_base64
                processed_base64 = image_to_base64(processed_image)
                
                print("Calling Groq AI for detection...")
                ai_result = detector.analyze_plant_image(processed_base64, crop_type)
                
                disease_name = ai_result.get('disease', 'Unknown')
                confidence = ai_result.get('confidence', 0.0)
                severity = ai_result.get('severity', 'Unknown')
                ai_recommendation = ai_result.get('ai_recommendation', '')
                
                print(f"Detection result: {disease_name} ({confidence:.2%})")
            
            except Exception as e:
                print(f"AI detection error: {str(e)}")
                self._send_error(500, f"Disease detection failed: {str(e)}")
                return
            
            # Get detailed disease information from database
            disease_info = get_disease_info(disease_name)
            
            # Save to Supabase if user_id provided
            scan_id = None
            image_url = None
            
            if user_id and supabase:
                try:
                    # Upload image to Supabase Storage
                    filename = f"{user_id}_{int(datetime.now().timestamp())}.jpg"
                    
                    # Convert image to bytes
                    import io
                    img_byte_arr = io.BytesIO()
                    processed_image.save(img_byte_arr, format='JPEG')
                    img_byte_arr.seek(0)
                    
                    # Upload to storage
                    storage_response = supabase.storage.from_('scan-images').upload(
                        filename,
                        img_byte_arr.getvalue(),
                        {"content-type": "image/jpeg"}
                    )
                    
                    # Get public URL
                    image_url = supabase.storage.from_('scan-images').get_public_url(filename)
                    
                    # Save scan to database
                    scan_data = {
                        'user_id': user_id,
                        'image_url': image_url,
                        'crop_type': crop_type.title(),
                        'disease_detected': disease_name,
                        'confidence': float(confidence),
                        'severity': severity,
                        'recommendations': json.dumps(disease_info.get('treatment', []))
                    }
                    
                    result = supabase.table('scans').insert(scan_data).execute()
                    scan_id = result.data[0]['id'] if result.data else None
                    
                    print(f"Scan saved to database: {scan_id}")
                
                except Exception as e:
                    print(f"Database save error: {str(e)}")
                    # Continue even if DB save fails
            
            # Prepare response
            response_data = {
                'success': True,
                'scan_id': scan_id,
                'disease': disease_name,
                'confidence': round(confidence * 100, 2),
                'severity': severity,
                'crop_type': crop_type.title(),
                'description': disease_info.get('description', ''),
                'symptoms': disease_info.get('symptoms', []),
                'treatment': disease_info.get('treatment', []),
                'prevention': disease_info.get('prevention', []),
                'organic_treatment': disease_info.get('organic_treatment', []),
                'cost_estimate': disease_info.get('cost_estimate', 'Unknown'),
                'scientific_name': disease_info.get('scientific_name', 'Unknown'),
                'ai_recommendation': ai_recommendation,
                'image_url': image_url,
                'timestamp': datetime.now().isoformat()
            }
            
            # Send success response
            self._send_json_response(200, response_data)
            print("Response sent successfully")
        
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            self._send_error(500, f"Internal server error: {str(e)}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self._send_cors_headers()
        self.end_headers()
    
    def _send_json_response(self, status_code, data):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, status_code, message):
        """Send error response"""
        error_data = {
            'success': False,
            'error': message,
            'timestamp': datetime.now().isoformat()
        }
        self._send_json_response(status_code, error_data)
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')