#!/usr/bin/env python3
"""
Complete test of CropGuard AI app - Backend, Frontend, and Mobile build
"""

import requests
import json
import base64
import subprocess
import os
from pathlib import Path

def test_backend_api():
    """Test the backend API endpoints"""
    print("🔍 Testing Backend API...")
    
    base_url = "https://cropguard-ai.vercel.app/api"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check: {health_data.get('status', 'unknown')}")
            print(f"🔑 Groq configured: {health_data.get('environment', {}).get('groq_configured', False)}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check error: {e}")
        return False
    
    # Test detection endpoint with mock data
    try:
        test_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAAAAAAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCABIAGQDASIAAhEBAxEB/8QAGwAAAgIDAQAAAAAAAAAAAAAABQYEBwIDCAH/xAAxEAABBAEEAQMDAwIGBwAAAAACAAEDBAURBhIhByITMQgUQVEJI3GBkaGx8P/EABkBAAMBAQEAAAAAAAAAAAAAAAABAgMEBf/EACQRAAICAgIBBAMBAAAAAAAAAAABAhEDEhMhMQQiQVFhcYGR/9oADAMBAAIRAxEAPwDwGvQM9AcEEA=="
        
        test_data = {
            "image": test_image,
            "crop_type": "tomato",
            "user_id": "test-user"
        }
        
        response = requests.post(
            f"{base_url}/detect",
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Detection API: {result.get('disease', 'Unknown')}")
                print(f"🎯 Confidence: {result.get('confidence', '0')}%")
                return True
            else:
                print(f"❌ Detection failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Detection API failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Detection API error: {e}")
        return False

def test_flutter_setup():
    """Test Flutter setup and configuration"""
    print("\n🔍 Testing Flutter Setup...")
    
    try:
        # Check Flutter doctor
        result = subprocess.run(['flutter', 'doctor'], 
                              capture_output=True, text=True, timeout=30)
        
        doctor_output = result.stdout
        
        # Check for key indicators
        flutter_ok = '✓' in doctor_output and 'Flutter' in doctor_output
        android_ok = '✓' in doctor_output and 'Android toolchain' in doctor_output
        
        print(f"✅ Flutter installed: {flutter_ok}")
        print(f"{'✅' if android_ok else '❌'} Android toolchain: {android_ok}")
        
        if not android_ok:
            print("⚠️  Android SDK needs configuration")
            print("🔧 Run: fix_android_setup.bat")
            return False
            
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Flutter doctor timed out")
        return False
    except FileNotFoundError:
        print("❌ Flutter not found - please install Flutter SDK")
        return False
    except Exception as e:
        print(f"❌ Flutter check error: {e}")
        return False

def try_build_apk():
    """Try to build APK if possible"""
    print("\n🔍 Testing APK Build...")
    
    mobile_dir = Path("mobile")
    if not mobile_dir.exists():
        print("❌ Mobile directory not found")
        return False
    
    try:
        # Try flutter pub get first
        result = subprocess.run(['flutter', 'pub', 'get'], 
                              cwd=mobile_dir, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"❌ Flutter pub get failed: {result.stderr}")
            return False
        
        print("✅ Flutter dependencies resolved")
        
        # Try building debug APK (faster)
        print("🔨 Building debug APK...")
        result = subprocess.run(['flutter', 'build', 'apk', '--debug'], 
                              cwd=mobile_dir, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            apk_path = mobile_dir / "build" / "app" / "outputs" / "flutter-apk" / "app-debug.apk"
            if apk_path.exists():
                size_mb = apk_path.stat().st_size / (1024 * 1024)
                print(f"✅ APK built successfully!")
                print(f"📱 Location: {apk_path}")
                print(f"📦 Size: {size_mb:.1f} MB")
                return True
            else:
                print("❌ APK file not found after build")
                return False
        else:
            print(f"❌ APK build failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ APK build timed out (this can take 5-10 minutes)")
        return False
    except Exception as e:
        print(f"❌ APK build error: {e}")
        return False

def check_web_deployment():
    """Check if web deployment is working"""
    print("\n🔍 Testing Web Deployment...")
    
    try:
        response = requests.get("https://cropguard-ai.vercel.app", timeout=10)
        if response.status_code == 200:
            if "CropGuard AI" in response.text:
                print("✅ Web app deployed and accessible")
                return True
            else:
                print("⚠️  Web app accessible but content might be wrong")
                return False
        else:
            print(f"❌ Web app not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web app check error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 CropGuard AI - Complete App Test")
    print("=" * 50)
    
    test_results = {}
    
    # Run all tests
    test_results['backend'] = test_backend_api()
    test_results['web'] = check_web_deployment() 
    test_results['flutter'] = test_flutter_setup()
    test_results['apk'] = try_build_apk() if test_results['flutter'] else False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 COMPLETE TEST RESULTS")
    print("=" * 50)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name.upper()}")
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    print(f"\n📈 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 PERFECT! Everything is working!")
        print("🌐 Web App: https://cropguard-ai.vercel.app")
        if test_results['apk']:
            print("📱 APK: mobile/build/app/outputs/flutter-apk/app-debug.apk")
            
    elif test_results['backend'] and test_results['web']:
        print("\n✅ Web application is fully working!")
        print("🌐 Live at: https://cropguard-ai.vercel.app")
        if not test_results['apk']:
            print("📱 For mobile app: Fix Android SDK and run 'flutter build apk'")
            
    else:
        print("\n🔧 Issues to fix:")
        if not test_results['backend']:
            print("   - Backend API needs fixing")
        if not test_results['web']:
            print("   - Web deployment needs fixing")  
        if not test_results['flutter']:
            print("   - Android SDK setup needed (run fix_android_setup.bat)")
    
    print("\n📚 Quick fixes:")
    print("   - Backend: Check Vercel deployment and environment variables")
    print("   - Android: Run fix_android_setup.bat and accept licenses")
    print("   - APK: flutter build apk --debug in mobile/ directory")

if __name__ == "__main__":
    main()