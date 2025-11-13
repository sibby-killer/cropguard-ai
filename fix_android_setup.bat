@echo off
echo 🔧 CropGuard AI - Android Setup Fix
echo =====================================

echo.
echo 🔍 Searching for Android SDK...

REM Common Android SDK locations
set "SDK_PATH1=C:\Users\%USERNAME%\AppData\Local\Android\Sdk"
set "SDK_PATH2=C:\Android\Sdk" 
set "SDK_PATH3=C:\Program Files\Android\Sdk"
set "SDK_PATH4=C:\Users\%USERNAME%\Android\Sdk"

REM Check each location
if exist "%SDK_PATH1%" (
    echo ✅ Found Android SDK at: %SDK_PATH1%
    set "ANDROID_HOME=%SDK_PATH1%"
    goto :configure
)

if exist "%SDK_PATH2%" (
    echo ✅ Found Android SDK at: %SDK_PATH2%
    set "ANDROID_HOME=%SDK_PATH2%"
    goto :configure
)

if exist "%SDK_PATH3%" (
    echo ✅ Found Android SDK at: %SDK_PATH3%
    set "ANDROID_HOME=%SDK_PATH3%"
    goto :configure
)

if exist "%SDK_PATH4%" (
    echo ✅ Found Android SDK at: %SDK_PATH4%
    set "ANDROID_HOME=%SDK_PATH4%"
    goto :configure
)

echo ❌ Android SDK not found in common locations
echo.
echo 🔧 Setting up Android SDK manually...
echo Please run Android Studio and go to:
echo   File > Settings > Appearance & Behavior > System Settings > Android SDK
echo   Note the SDK Location path and run this script again
echo.
echo Or set ANDROID_HOME manually:
echo   setx ANDROID_HOME "C:\path\to\your\android\sdk"
pause
exit /b 1

:configure
echo.
echo 🔧 Configuring environment variables...

REM Set environment variables
setx ANDROID_HOME "%ANDROID_HOME%"
setx PATH "%PATH%;%ANDROID_HOME%\tools;%ANDROID_HOME%\tools\bin;%ANDROID_HOME%\platform-tools"

echo ✅ ANDROID_HOME set to: %ANDROID_HOME%
echo ✅ PATH updated with Android tools

echo.
echo 🔧 Configuring Flutter...
flutter config --android-sdk "%ANDROID_HOME%"

echo.
echo 📋 Checking Flutter doctor...
flutter doctor

echo.
echo 🎯 Next steps:
echo   1. Restart your command prompt/IDE
echo   2. Run: flutter doctor --android-licenses
echo   3. Accept all licenses by typing 'y'
echo   4. Run: cd mobile && flutter build apk
echo.
pause