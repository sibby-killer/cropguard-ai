"""
Groq AI Client for Plant Disease Detection
Uses Groq's vision model to analyze plant images
"""

import os
from groq import Groq
import json

class GroqDiseaseDetector:
    """Client for Groq AI plant disease detection"""
    
    def __init__(self):
        """Initialize Groq client"""
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.2-90b-vision-preview"  # Groq's vision model
    
    def analyze_plant_image(self, base64_image, crop_type="unknown"):
        """
        Analyze plant image for diseases using Groq Vision AI
        
        Args:
            base64_image: Base64 encoded image string
            crop_type: Type of crop (tomato, potato, etc.)
            
        Returns:
            dict: Detection results with disease, confidence, and recommendations
        """
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(crop_type)
            
            # Ensure proper data URI format
            if not base64_image.startswith('data:image'):
                base64_image = f"data:image/jpeg;base64,{base64_image}"
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": base64_image
                                }
                            }
                        ]
                    }
                ],
                temperature=0.2,  # Lower temperature for more consistent results
                max_tokens=1000,
                top_p=0.9
            )
            
            # Parse response
            result_text = response.choices[0].message.content
            
            # Extract structured data from response
            result = self._parse_analysis_result(result_text, crop_type)
            
            return result
        
        except Exception as e:
            print(f"Groq API error: {str(e)}")
            raise Exception(f"Disease detection failed: {str(e)}")
    
    def _create_analysis_prompt(self, crop_type):
        """Create prompt for disease analysis"""
        return f"""You are an expert plant pathologist. Analyze this {crop_type} plant image and identify any diseases.

Provide your analysis in the following JSON format:
{{
    "disease_detected": "name of disease or 'Healthy'",
    "confidence": confidence score between 0 and 1,
    "severity": "None/Mild/Moderate/Severe",
    "symptoms_observed": ["list", "of", "symptoms"],
    "recommendation": "brief treatment recommendation"
}}

Common {crop_type} diseases to look for:
- Late Blight (dark water-soaked spots)
- Early Blight (concentric ring spots)
- Septoria Leaf Spot (small circular spots)
- Bacterial Spot (small dark lesions)
- Leaf Mold (yellowish spots with mold)
- Mosaic Virus (mottled yellowing)
- Healthy (no disease symptoms)

Focus on visible symptoms like:
- Leaf discoloration or spots
- Leaf curling or deformity
- Mold or fungal growth
- Stem lesions
- Overall plant health

Be specific about the disease name. If the plant looks healthy, say "Healthy Plant"."""
    
    def _parse_analysis_result(self, result_text, crop_type):
        """
        Parse AI response into structured format
        
        Args:
            result_text: Raw text response from Groq
            crop_type: Type of crop analyzed
            
        Returns:
            dict: Structured detection result
        """
        try:
            # Try to extract JSON from response
            # Look for JSON block in markdown code blocks
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                json_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                json_text = result_text[json_start:json_end].strip()
            elif "{" in result_text and "}" in result_text:
                json_start = result_text.find("{")
                json_end = result_text.rfind("}") + 1
                json_text = result_text[json_start:json_end]
            else:
                json_text = result_text
            
            # Parse JSON
            data = json.loads(json_text)
            
            # Validate and normalize
            disease = data.get('disease_detected', 'Unknown').strip()
            confidence = float(data.get('confidence', 0.5))
            severity = data.get('severity', 'Unknown')
            symptoms = data.get('symptoms_observed', [])
            recommendation = data.get('recommendation', '')
            
            # Ensure confidence is between 0 and 1
            if confidence > 1:
                confidence = confidence / 100
            
            return {
                'disease': disease,
                'confidence': confidence,
                'severity': 'Unknown',
                'symptoms': [],
                'ai_recommendation': result_text[:200],
                'raw_response': result_text
            }
        
        except Exception as e:
            print(f"Parse error: {str(e)}")
            return {
                'disease': 'Analysis Error',
                'confidence': 0.0,
                'severity': 'Unknown',
                'symptoms': [],
                'ai_recommendation': 'Failed to analyze image',
                'raw_response': result_text
            }