# Find Android SDK for CropGuard AI
Write-Host "🔍 Searching for Android SDK..." -ForegroundColor Green

# Common Android SDK locations
$locations = @(
    "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk",
    "C:\Android\Sdk",
    "C:\Program Files\Android\Sdk", 
    "C:\Program Files (x86)\Android\Sdk",
    "C:\Users\$env:USERNAME\Android\Sdk"
)

foreach ($location in $locations) {
    if (Test-Path $location) {
        Write-Host "✅ Found Android SDK at: $location" -ForegroundColor Green
        
        # Set environment variable
        [Environment]::SetEnvironmentVariable("ANDROID_HOME", $location, "User")
        $env:ANDROID_HOME = $location
        
        # Configure Flutter
        flutter config --android-sdk $location
        
        Write-Host "✅ Configured Flutter with Android SDK" -ForegroundColor Green
        
        # Test if it works
        Write-Host "🧪 Testing Flutter doctor..." -ForegroundColor Yellow
        flutter doctor
        
        exit 0
    }
}

# If not found, check Android Studio installation
Write-Host "⚠️  Android SDK not found in common locations" -ForegroundColor Yellow
Write-Host "🔧 Let's set it up via Android Studio..." -ForegroundColor Blue

# Open Android Studio SDK Manager
Write-Host "📋 Next steps:"
Write-Host "1. Open Android Studio"
Write-Host "2. Go to File → Settings (or Configure → Settings)"
Write-Host "3. Go to Appearance & Behavior → System Settings → Android SDK"
Write-Host "4. Note the 'Android SDK Location' path"
Write-Host "5. Run: flutter config --android-sdk `"path_from_step_4`""
Write-Host "6. Run: flutter doctor --android-licenses"
Write-Host "7. Accept all licenses by typing 'y'"

# Try to open Android Studio
try {
    Start-Process "studio64.exe"
    Write-Host "✅ Opened Android Studio" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not auto-open Android Studio" -ForegroundColor Yellow
    Write-Host "Please open it manually from Start menu" -ForegroundColor Blue
}