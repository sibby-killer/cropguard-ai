#!/usr/bin/env python3
"""
Quick test script to verify JPEG upload functionality
Tests both local backend and live API
"""

import requests
import base64
import json
import os
from pathlib import Path

def create_test_image():
    """Create a simple test image for testing"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a simple plant-like image
        img = Image.new('RGB', (400, 300), color='lightgreen')
        draw = ImageDraw.Draw(img)
        
        # Draw some leaf-like shapes
        draw.ellipse([50, 50, 150, 150], fill='green', outline='darkgreen', width=3)
        draw.ellipse([200, 100, 300, 200], fill='green', outline='darkgreen', width=3)
        draw.ellipse([100, 150, 200, 250], fill='darkgreen', outline='black', width=2)
        
        # Add some "disease" spots
        draw.ellipse([80, 90, 100, 110], fill='brown')
        draw.ellipse([230, 130, 250, 150], fill='yellow')
        
        # Add text
        try:
            draw.text((10, 10), "Test Plant Image", fill='black')
        except:
            pass  # Font might not be available
        
        # Save as JPEG bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=90)
        img_byte_arr.seek(0)
        
        # Convert to base64
        base64_str = base64.b64encode(img_byte_arr.getvalue()).decode()
        return f"data:image/jpeg;base64,{base64_str}"
        
    except ImportError:
        print("⚠️  PIL not available, using a simple text-based image")
        # Fallback: create a minimal base64 image
        return "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCABIAGQDASIAAhEBAxEB/8QAGwAAAgIDAQAAAAAAAAAAAAAABQYEBwIDCAH/xAAxEAABBAEEAQMDAwIGBwAAAAACAAEDBAURBhIhByITMQgUQVEjMmEJI3GBkaGx8P/EABkBAAMBAQEAAAAAAAAAAAAAAAABAgMEBf/EACQRAAICAgIBBAMBAAAAAAAAAAABAhEhMQMSQUEEUWGhEyJx/9oADAMBAAIRAxEAPwDwGvQM9AcEEA=="

def test_api_endpoint(api_url, test_data, endpoint_name):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing {endpoint_name}")
    print(f"📍 URL: {api_url}")
    
    try:
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ Success! Disease: {result.get('disease', 'N/A')}")
                print(f"🎯 Confidence: {result.get('confidence', 'N/A')}%")
                print(f"💡 Recommendation: {result.get('ai_recommendation', 'N/A')[:100]}...")
                return True
            except json.JSONDecodeError:
                print(f"⚠️  Valid response but not JSON: {response.text[:200]}")
                return False
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - server might not be running")
        return False
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    print(f"\n🔍 Testing Health Endpoint")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data.get('status', 'unknown')}")
            print(f"🔑 Groq configured: {data.get('environment', {}).get('groq_configured', False)}")
            print(f"💾 Supabase configured: {data.get('environment', {}).get('supabase_configured', False)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Main test function"""
    print("🌱 CropGuard AI - JPEG Upload Test")
    print("=" * 50)
    
    # Create test image
    print("🖼️  Creating test image...")
    test_image = create_test_image()
    print(f"✅ Test image created (length: {len(test_image)} chars)")
    
    # Test data
    test_cases = [
        {
            "name": "Tomato Test",
            "data": {
                "image": test_image,
                "crop_type": "tomato",
                "user_id": "test-user"
            }
        },
        {
            "name": "Custom Plant Test",
            "data": {
                "image": test_image,
                "crop_type": "mango",
                "user_id": "test-user"
            }
        }
    ]
    
    # API endpoints to test
    endpoints = [
        {
            "name": "Local API",
            "base_url": "http://localhost:8000/api",
            "detect_url": "http://localhost:8000/api/detect"
        },
        {
            "name": "Live API",
            "base_url": "https://cropguard-oji3662ur-sibby-killers-projects.vercel.app/api",
            "detect_url": "https://cropguard-oji3662ur-sibby-killers-projects.vercel.app/api/detect"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        print(f"\n{'='*60}")
        print(f"🔧 Testing {endpoint['name']}")
        print(f"{'='*60}")
        
        # Test health first
        health_ok = test_health_endpoint(endpoint['base_url'])
        
        if health_ok:
            # Test detection endpoints
            for test_case in test_cases:
                success = test_api_endpoint(
                    endpoint['detect_url'], 
                    test_case['data'], 
                    f"{endpoint['name']} - {test_case['name']}"
                )
                results.append({
                    'endpoint': endpoint['name'],
                    'test': test_case['name'],
                    'success': success
                })
        else:
            print(f"⚠️  Skipping {endpoint['name']} - health check failed")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} - {result['endpoint']} - {result['test']}")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['success'])
    
    print(f"\n📈 Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == 0:
        print("\n🚨 All tests failed. Common issues:")
        print("   1. Backend not running (start with: python start_local_server.py)")
        print("   2. Missing GROQ_API_KEY environment variable")
        print("   3. CORS issues (should be fixed in the updated code)")
        print("   4. Network connectivity issues")
        
        print("\n🔧 Quick fixes:")
        print("   - For local testing: python start_local_server.py")
        print("   - Check .env file in backend/ directory")
        print("   - Try the web interface at http://localhost:3000/local-dev.html")
    
    elif passed_tests < total_tests:
        print("\n⚠️  Some tests failed. This might be expected if:")
        print("   - Local server is not running")
        print("   - Live API has temporary issues")
        print("   - Environment variables are not set")
    
    else:
        print("\n🎉 All tests passed! Your JPEG upload functionality is working!")
        print("\n🌐 You can now:")
        print("   - Test via web interface: http://localhost:3000/local-dev.html")
        print("   - Upload real JPEG/PNG images")
        print("   - Try custom plant names")
        print("   - Build and test the mobile app")

if __name__ == "__main__":
    main()