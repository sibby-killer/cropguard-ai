"""
Vercel serverless function for health check
"""
import json
import os
from datetime import datetime

def handler(request):
    """Handle health check requests"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Health check data
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": {
            "groq_configured": bool(os.environ.get('GROQ_API_KEY')),
            "supabase_configured": bool(os.environ.get('SUPABASE_URL'))
        },
        "version": "2.0.0",
        "endpoints": [
            "/api/health",
            "/api/detect"
        ]
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(health_data, indent=2)
    }

# Export for Vercel
def main(request):
    return handler(request)