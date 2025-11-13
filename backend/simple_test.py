#!/usr/bin/env python3
"""
Simple test script to verify CropGuard AI backend setup
"""

import os
import sys

def test_environment():
    """Test if environment variables are configured"""
    print("🔧 Checking Environment Variables...")
    
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loaded successfully")
    except ImportError:
        print("⚠️ python-dotenv not installed (optional)")
    except FileNotFoundError:
        print("⚠️ .env file not found")
    except Exception as e:
        print(f"⚠️ Error loading .env: {e}")
    
    # Check required environment variables
    required_vars = {
        'GROQ_API_KEY': 'Groq AI API Key',
        'SUPABASE_URL': 'Supabase Project URL', 
        'SUPABASE_KEY': 'Supabase Anon Key'
    }
    
    configured = []
    missing = []
    
    for var, description in required_vars.items():
        if var in os.environ and os.environ[var]:
            configured.append(f"✅ {var} - {description}")
        else:
            missing.append(f"❌ {var} - {description}")
    
    print(f"\n📊 Environment Status: {len(configured)}/{len(required_vars)} configured")
    
    for item in configured:
        print(f"   {item}")
    
    if missing:
        print("\n⚠️ Missing Variables:")
        for item in missing:
            print(f"   {item}")
    
    return len(missing) == 0

def test_python_dependencies():
    """Test if all required Python packages are installed"""
    print("\n📦 Checking Python Dependencies...")
    
    required_packages = {
        'cv2': 'opencv-python-headless',
        'PIL': 'Pillow', 
        'groq': 'groq',
        'supabase': 'supabase',
        'flask': 'flask',
        'requests': 'requests',
        'numpy': 'numpy'
    }
    
    installed = []
    missing = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            installed.append(f"✅ {package_name}")
        except ImportError:
            missing.append(f"❌ {package_name}")
    
    print(f"\n📊 Dependencies Status: {len(installed)}/{len(required_packages)} installed")
    
    for item in installed:
        print(f"   {item}")
    
    if missing:
        print("\n⚠️ Missing Packages:")
        for item in missing:
            print(f"   {item}")
        
        print("\n🔧 To install missing packages:")
        print("   pip install -r requirements.txt")
    
    return len(missing) == 0

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Checking File Structure...")
    
    required_files = [
        'requirements.txt',
        'vercel.json',
        '.env.example',
        'api/__init__.py',
        'api/detect.py',
        'api/health.py', 
        'api/diseases.py',
        'api/history.py',
        'utils/__init__.py',
        'utils/groq_client.py',
        'utils/image_processor.py',
        'utils/disease_info.py'
    ]
    
    existing = []
    missing = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            existing.append(f"✅ {file_path}")
        else:
            missing.append(f"❌ {file_path}")
    
    print(f"\n📊 Files Status: {len(existing)}/{len(required_files)} found")
    
    if missing:
        print("\n⚠️ Missing Files:")
        for item in missing:
            print(f"   {item}")
    
    return len(missing) == 0

def test_basic_imports():
    """Test basic imports without dependencies that might fail"""
    print("\n🐍 Testing Basic Imports...")
    
    try:
        # Test if we can import our modules
        sys.path.append('.')
        
        # Test basic Python modules
        import json
        import base64
        import os
        print("✅ Standard library modules imported")
        
        # Test if our files can be found
        if os.path.exists('utils/disease_info.py'):
            print("✅ Disease database file found")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def show_next_steps(env_ok, deps_ok, files_ok):
    """Show appropriate next steps based on test results"""
    print("\n" + "="*60)
    print("🎯 NEXT STEPS")
    print("="*60)
    
    if not env_ok:
        print("1. 🔑 Set up your API keys:")
        print("   - Copy .env.example to .env")
        print("   - Get Groq API key from https://console.groq.com")
        print("   - Get Supabase credentials from https://supabase.com")
        print("   - Add keys to .env file")
        
    if not deps_ok:
        print("2. 📦 Install missing dependencies:")
        print("   pip install -r requirements.txt")
        
    if not files_ok:
        print("3. 📁 Some project files are missing")
        print("   - Make sure you've cloned the complete repository")
        
    if env_ok and deps_ok and files_ok:
        print("🎉 Backend setup looks good!")
        print("\n🚀 Ready for deployment:")
        print("   1. Install Vercel CLI: npm install -g vercel")
        print("   2. Deploy: vercel --prod")
        print("   3. Set environment variables in Vercel dashboard")
        print("   4. Test with: curl https://your-app.vercel.app/api/health")
        
        print("\n📱 For mobile app:")
        print("   1. cd ../mobile")
        print("   2. flutter pub get")
        print("   3. Update API URL in lib/services/api_service.dart")
        print("   4. flutter run")

def main():
    """Run all tests"""
    print("🌱 CropGuard AI - Simple Backend Test")
    print("="*60)
    
    env_ok = test_environment()
    deps_ok = test_python_dependencies()  
    files_ok = test_file_structure()
    imports_ok = test_basic_imports()
    
    show_next_steps(env_ok, deps_ok, files_ok)

if __name__ == "__main__":
    main()