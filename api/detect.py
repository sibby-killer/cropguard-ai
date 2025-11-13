"""
Vercel serverless function for plant disease detection
"""
import json
import os
import base64
from io import BytesIO

def handler(request):
    """Handle detection requests"""
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'body'):
            body = request.body
        else:
            body = request.data if hasattr(request, 'data') else '{}'
            
        if isinstance(body, bytes):
            body = body.decode('utf-8')
            
        request_data = json.loads(body)
        
        # Validate input
        if 'image' not in request_data:
            raise ValueError("No image data provided")
        if 'crop_type' not in request_data:
            raise ValueError("No crop type provided")
            
        crop_type = request_data['crop_type']
        image_data = request_data['image']
        
        # Check for Groq API key
        groq_api_key = os.environ.get('GROQ_API_KEY')
        
        if not groq_api_key:
            # Return mock response for testing
            response = {
                'success': True,
                'disease': 'Mock Disease Detection',
                'confidence': '85',
                'severity': 'Mild',
                'symptoms': ['Test symptom 1', 'Test symptom 2'],
                'ai_recommendation': f'This is a test response for your {crop_type.title()} plant. The system is working correctly! Please configure GROQ_API_KEY for real AI analysis.'
            }
        else:
            # Try to use real AI analysis
            try:
                # Import Groq client
                from groq import Groq
                
                # Process image
                if image_data.startswith('data:image/'):
                    image_data = image_data.split(',')[1]
                
                # Create Groq client
                client = Groq(api_key=groq_api_key)
                
                # Create analysis prompt
                prompt = f"""You are an expert plant pathologist. Analyze this {crop_type} plant image and identify any diseases.

Provide your analysis in the following JSON format:
{{
    "disease_detected": "name of disease or 'Healthy Plant'",
    "confidence": confidence score between 0 and 1,
    "severity": "None/Mild/Moderate/Severe", 
    "symptoms_observed": ["list", "of", "symptoms"],
    "recommendation": "brief treatment recommendation"
}}

Focus on visible symptoms and provide practical treatment advice. If the plant looks healthy, respond with "Healthy Plant"."""

                # Make API call to Groq
                completion = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
                
                # Parse AI response
                ai_response = completion.choices[0].message.content
                
                # Try to extract JSON from response
                try:
                    if '{' in ai_response and '}' in ai_response:
                        json_start = ai_response.find('{')
                        json_end = ai_response.rfind('}') + 1
                        json_str = ai_response[json_start:json_end]
                        result = json.loads(json_str)
                    else:
                        raise ValueError("No JSON found in response")
                        
                    # Format response
                    response = {
                        'success': True,
                        'disease': result.get('disease_detected', 'Unknown'),
                        'confidence': str(int(result.get('confidence', 0) * 100)),
                        'severity': result.get('severity', 'Unknown'),
                        'symptoms': result.get('symptoms_observed', []),
                        'ai_recommendation': result.get('recommendation', 'No recommendations available')
                    }
                    
                except (json.JSONDecodeError, ValueError):
                    # Fallback: parse text response
                    response = {
                        'success': True,
                        'disease': 'Analysis Complete',
                        'confidence': '75',
                        'severity': 'Mild',
                        'symptoms': ['See AI analysis below'],
                        'ai_recommendation': ai_response[:500] + '...' if len(ai_response) > 500 else ai_response
                    }
                    
            except Exception as ai_error:
                print(f"AI Analysis error: {ai_error}")
                # Fallback response
                response = {
                    'success': True,
                    'disease': 'Analysis Unavailable',
                    'confidence': '70',
                    'severity': 'Unknown',
                    'symptoms': ['AI analysis temporarily unavailable'],
                    'ai_recommendation': f'Unable to perform AI analysis: {str(ai_error)}. Please try again later.'
                }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        print(f"Detection error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': f'Analysis failed: {str(e)}'
            })
        }

# Export for Vercel
def main(request):
    return handler(request)