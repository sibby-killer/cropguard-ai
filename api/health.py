import json
import os
from datetime import datetime

def handler(request):
    """Vercel serverless function for health check"""
    
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
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "environment": {
            "groq_configured": bool(os.environ.get('GROQ_API_KEY')),
            "supabase_configured": bool(os.environ.get('SUPABASE_URL'))
        },
        "version": "2.0.0",
        "endpoints": ["/api/health", "/api/detect"]
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(health_data, indent=2)
    }