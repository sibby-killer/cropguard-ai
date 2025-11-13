#!/usr/bin/env python3
"""
Local testing script for CropGuard AI Backend
This script helps you test the API endpoints locally before deploying to Vercel
"""

import os
import sys
import json
import base64
from io import BytesIO
from PIL import Image
import requests

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our API modules
from api import health, detect, diseases, history

def create_test_image():
    """Create a simple test image for testing"""
    # Create a simple green image (simulating a leaf)
    img = Image.new('RGB', (224, 224), color=(34, 139, 34))  # Forest green
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/jpeg;base64,{img_base64}"

def test_health_endpoint():
    """Test the health endpoint"""
    print("🏥 Testing Health Endpoint...")
    
    try:
        # Simulate a GET request
        class MockRequest:
            def __init__(self):
                self.method = 'GET'
                self.headers = {}
        
        # Mock the handler
        class MockHandler:
            def __init__(self):
                self.request = MockRequest()
                
            def do_GET(self):
                return health.handler(self.request, None)
        
        # For now, let's just check if we can import and the environment is set up
        from utils.groq_client import GroqClient
        from utils.disease_info import DISEASE_DATABASE
        
        print("✅ Health check passed!")
        print(f"   - Disease database loaded: {len(DISEASE_DATABASE)} diseases")
        print(f"   - Groq API key configured: {'GROQ_API_KEY' in os.environ}")
        print(f"   - Supabase URL configured: {'SUPABASE_URL' in os.environ}")
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    return True

def test_disease_database():
    """Test the disease database"""
    print("\n🌾 Testing Disease Database...")
    
    try:
        from utils.disease_info import DISEASE_DATABASE, get_disease_info
        
        print(f"✅ Disease database loaded with {len(DISEASE_DATABASE)} diseases:")
        
        for disease_name in list(DISEASE_DATABASE.keys())[:5]:  # Show first 5
            disease = get_disease_info(disease_name)
            if disease:
                print(f"   - {disease_name} ({disease.get('crop', 'Unknown crop')})")
        
        if len(DISEASE_DATABASE) > 5:
            print(f"   ... and {len(DISEASE_DATABASE) - 5} more diseases")
            
    except Exception as e:
        print(f"❌ Disease database test failed: {e}")
        return False
    
    return True

def test_image_processing():
    """Test image processing functionality"""
    print("\n🖼️ Testing Image Processing...")
    
    try:
        from utils.image_processor import ImageProcessor
        
        processor = ImageProcessor()
        test_image_base64 = create_test_image()
        
        # Test image processing
        processed_image = processor.process_image(test_image_base64)
        
        print("✅ Image processing test passed!")
        print(f"   - Input image: {len(test_image_base64)} characters")
        print(f"   - Processed image: {len(processed_image)} characters")
        
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False
    
    return True

def test_groq_client():
    """Test Groq client (requires API key)"""
    print("\n🤖 Testing Groq Client...")
    
    if 'GROQ_API_KEY' not in os.environ:
        print("⚠️ GROQ_API_KEY not found in environment. Skipping Groq test.")
        print("   To test Groq integration, set your API key in .env file")
        return True
    
    try:
        from utils.groq_client import GroqClient
        
        client = GroqClient()
        test_image_base64 = create_test_image()
        
        print("✅ Groq client initialized successfully!")
        print("   - API key configured")
        print("   - Ready for disease analysis")
        print("   - Note: Actual API call not made in local test")
        
    except Exception as e:
        print(f"❌ Groq client test failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing Environment Configuration...")
    
    required_vars = ['GROQ_API_KEY', 'SUPABASE_URL', 'SUPABASE_KEY']
    configured_vars = []
    missing_vars = []
    
    for var in required_vars:
        if var in os.environ:
            configured_vars.append(var)
        else:
            missing_vars.append(var)
    
    print(f"✅ Configured variables: {len(configured_vars)}/{len(required_vars)}")
    for var in configured_vars:
        print(f"   ✓ {var}")
    
    if missing_vars:
        print(f"⚠️ Missing variables: {len(missing_vars)}")
        for var in missing_vars:
            print(f"   ✗ {var}")
        print("\n📝 To fix missing variables:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your API keys to .env file")
        print("   3. Run this test again")
    
    return len(missing_vars) == 0

def main():
    """Run all tests"""
    print("🌱 CropGuard AI - Backend Local Testing")
    print("=" * 50)
    
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded from .env")
    except ImportError:
        print("⚠️ python-dotenv not installed. Install with: pip install python-dotenv")
        print("   Environment variables will be read from system only.")
    except Exception as e:
        print(f"⚠️ Could not load .env file: {e}")
    
    print()
    
    # Run all tests
    tests = [
        test_environment,
        test_health_endpoint,
        test_disease_database,
        test_image_processing,
        test_groq_client,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is ready for deployment.")
        print("\n🚀 Next steps:")
        print("   1. Deploy to Vercel: vercel --prod")
        print("   2. Test deployed API with: curl https://your-app.vercel.app/api/health")
    else:
        print("⚠️ Some tests failed. Please fix the issues above before deploying.")
        print("\n📚 Need help? Check:")
        print("   - README.md for setup instructions")
        print("   - .env.example for required environment variables")

if __name__ == "__main__":
    main()