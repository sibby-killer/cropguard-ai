@echo off
echo 🚀 CropGuard AI - Quick APK Builder
echo ===================================

echo.
echo 🔍 Step 1: Finding Flutter...

REM Check if Flutter is in PATH
flutter --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ Flutter found in PATH
    goto :build
)

REM Try common Flutter locations
set "FLUTTER_PATH1=C:\flutter\bin"
set "FLUTTER_PATH2=C:\Users\%USERNAME%\flutter\bin"
set "FLUTTER_PATH3=C:\src\flutter\bin"

if exist "%FLUTTER_PATH1%\flutter.exe" (
    echo ✅ Found Flutter at: %FLUTTER_PATH1%
    set "PATH=%PATH%;%FLUTTER_PATH1%"
    goto :build
)

if exist "%FLUTTER_PATH2%\flutter.exe" (
    echo ✅ Found Flutter at: %FLUTTER_PATH2%
    set "PATH=%PATH%;%FLUTTER_PATH2%"
    goto :build
)

if exist "%FLUTTER_PATH3%\flutter.exe" (
    echo ✅ Found Flutter at: %FLUTTER_PATH3%
    set "PATH=%PATH%;%FLUTTER_PATH3%"
    goto :build
)

echo ❌ Flutter not found in common locations
echo.
echo 🔧 Please install Flutter or add to PATH:
echo   1. Download Flutter SDK from: https://flutter.dev/docs/get-started/install/windows
echo   2. Extract to C:\flutter
echo   3. Add C:\flutter\bin to your PATH
echo   4. Run this script again
echo.
pause
exit /b 1

:build
echo.
echo 🔍 Step 2: Checking Android SDK...

REM Set common Android SDK path
set "ANDROID_SDK=C:\Users\%USERNAME%\AppData\Local\Android\Sdk"
if exist "%ANDROID_SDK%" (
    echo ✅ Found Android SDK at: %ANDROID_SDK%
    set "ANDROID_HOME=%ANDROID_SDK%"
    flutter config --android-sdk "%ANDROID_SDK%"
) else (
    echo ⚠️  Android SDK not found at common location
    echo Will try to build anyway...
)

echo.
echo 🔍 Step 3: Building APK...

if not exist "mobile" (
    echo ❌ mobile directory not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

cd mobile

echo 📦 Cleaning previous builds...
flutter clean

echo 📥 Getting dependencies...
flutter pub get

echo 🔨 Building debug APK (faster than release)...
flutter build apk --debug --verbose

if %ERRORLEVEL% == 0 (
    echo.
    echo 🎉 SUCCESS! APK built successfully!
    echo.
    echo 📱 APK Location: mobile\build\app\outputs\flutter-apk\app-debug.apk
    
    REM Check if file exists and show size
    if exist "build\app\outputs\flutter-apk\app-debug.apk" (
        for %%A in ("build\app\outputs\flutter-apk\app-debug.apk") do (
            set "size=%%~zA"
        )
        echo 📦 APK Size: %size% bytes
        echo.
        echo 📋 Next Steps:
        echo   1. Copy APK to your phone
        echo   2. Enable "Unknown sources" in Android settings
        echo   3. Install the APK
        echo   4. Launch CropGuard AI and test!
        echo.
        echo 🌐 Also try the web version: https://cropguard-ai.vercel.app
    ) else (
        echo ❌ APK file not found after build
        echo Check the build output above for errors
    )
) else (
    echo.
    echo ❌ APK build failed!
    echo.
    echo 🔧 Common solutions:
    echo   1. Install Android SDK via Android Studio
    echo   2. Accept Android licenses: flutter doctor --android-licenses
    echo   3. Update Flutter: flutter upgrade
    echo   4. Check internet connection for dependencies
    echo.
    echo 🆘 Alternative: Use GitHub Actions for automatic building
    echo    Push your code and download APK from GitHub Actions
)

echo.
pause