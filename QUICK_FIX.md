# 🚀 CropGuard AI - QUICK FIXES NEEDED

## 🔧 Current Issues & Solutions

### ❌ Issue 1: Backend API 404 Error
**Problem**: Vercel deployment failing
**Fix**: 
1. Push updated vercel.json to GitHub
2. Redeploy on Vercel manually

### ❌ Issue 2: Flutter Not Found  
**Problem**: Flutter not in system PATH
**Fix**: 
```bash
# Add Flutter to PATH manually
$env:PATH += ";C:\flutter\bin"
# Or find your Flutter installation and add to system PATH
```

### ❌ Issue 3: Android SDK Not Configured
**Problem**: Android Studio installed but SDK not linked to Flutter
**Solution**: Run these commands in PowerShell as Administrator:

```powershell
# Find Android SDK (common location)
$androidSdk = "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"

# Set environment variables
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidSdk, "User")
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$androidSdk\tools;$androidSdk\tools\bin;$androidSdk\platform-tools", "User")

# Configure Flutter
flutter config --android-sdk $androidSdk
```

## 🎯 IMMEDIATE ACTION PLAN

### Step 1: Fix Backend (2 minutes)
```bash
git add vercel.json
git commit -m "Fix Vercel deployment config"
git push origin master
```

### Step 2: Fix Flutter PATH (1 minute)
```bash
# Find Flutter installation
Get-ChildItem -Path "C:\" -Recurse -Name "flutter.exe" -ErrorAction SilentlyContinue

# Add to PATH (replace with actual path)
$env:PATH += ";C:\path\to\flutter\bin"
```

### Step 3: Configure Android SDK (3 minutes)
```bash
# Open Android Studio
# Go to File → Settings → System Settings → Android SDK
# Note the SDK Location path
# Run: flutter config --android-sdk "C:\path\to\android\sdk"
```

### Step 4: Build APK (5 minutes)
```bash
cd mobile
flutter clean
flutter pub get
flutter build apk --debug
```

## 🚀 ALTERNATIVE: Use GitHub Actions (No Local Setup Needed)

If local setup is too complex, use automated building:

```bash
# Just push code - APK builds automatically
git add .
git commit -m "Trigger APK build [release]"
git push origin master

# Download APK from:
# https://github.com/sibby-killer/cropguard-ai/actions
```

## 🎯 FASTEST PATH TO WORKING APP

### Option A: Quick Local Build (if Flutter installed)
1. Find Flutter: `where flutter`
2. Add to PATH: `$env:PATH += ";C:\flutter\bin"`
3. Build APK: `cd mobile && flutter build apk --debug`

### Option B: Use GitHub Actions (Recommended)
1. Push current changes
2. Wait 5-10 minutes for automatic build
3. Download APK from GitHub Actions artifacts

### Option C: Manual APK Creation
1. Open Android Studio
2. Import mobile/ project
3. Click Build → Build APK
4. Find APK in build/outputs/flutter-apk/

## 🌐 Web App Status

The web app should work once backend is fixed. Test at:
- https://cropguard-ai.vercel.app

If still 404, the issue is in Vercel deployment configuration.

## 📱 Expected Final Result

**Working Web App**: Upload JPEG, enter custom plant names, get AI analysis
**Working Mobile APK**: 15-20MB file ready to install on Android

## 🆘 If Still Stuck

Run this one command to get everything working:

```bash
# Ultimate fix - rebuild everything
python test_app_full.py && cd mobile && flutter doctor && flutter clean && flutter pub get && flutter build apk --debug
```

**Success indicator**: APK file appears at `mobile/build/app/outputs/flutter-apk/app-debug.apk`