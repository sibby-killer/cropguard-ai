#!/usr/bin/env python3
"""
Deploy CropGuard AI to production
This script helps commit and push changes to trigger deployment
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {cmd}")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {cmd}")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {cmd} - Exception: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 CropGuard AI - Production Deployment")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not a git repository. Please run from the project root.")
        return
    
    # Get current status
    print("📋 Checking repository status...")
    
    # Check for changes
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Found changes to commit:")
        print(result.stdout)
        
        # Add all changes
        if run_command("git add ."):
            # Commit changes
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"Production deployment update - {timestamp} [release]"
            
            if run_command(f'git commit -m "{commit_msg}"'):
                print("✅ Changes committed successfully")
            else:
                print("⚠️  Commit failed, but continuing...")
    else:
        print("✅ No changes to commit")
    
    # Push to GitHub
    print("\n🚀 Deploying to production...")
    if run_command("git push origin main"):
        print("✅ Code pushed to GitHub")
        print("\n🎯 Deployment Status:")
        print("   📍 Web App: Deploying to Vercel automatically")
        print("   📍 Mobile APK: Building via GitHub Actions")
        print("   📍 Release: Will be created automatically")
        
        print("\n⏳ Expected completion:")
        print("   🌐 Web deployment: ~2-3 minutes")
        print("   📱 APK build: ~5-7 minutes")
        print("   🔗 Release creation: ~8-10 minutes")
        
        print("\n📋 What happens next:")
        print("   1. GitHub Actions builds Android APK")
        print("   2. Vercel deploys web application")
        print("   3. New release created with APK download")
        print("   4. README updated with latest links")
        
        print("\n🔗 Monitor progress:")
        print("   • GitHub Actions: https://github.com/sibby-killer/cropguard-ai/actions")
        print("   • Vercel Dashboard: https://vercel.com/dashboard")
        print("   • Live Web App: https://cropguard-ai.vercel.app")
        
        print("\n✅ PRODUCTION DEPLOYMENT INITIATED!")
        print("🎉 Your app will be live in a few minutes!")
        
    else:
        print("❌ Failed to push to GitHub")
        print("🔧 Please check your git configuration and network connection")

if __name__ == "__main__":
    main()