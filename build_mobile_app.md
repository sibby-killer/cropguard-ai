# Mobile App Build Instructions

## Prerequisites

### Option 1: Using Flutter (Recommended)
1. **Install Flutter SDK**
   ```bash
   # Windows (using PowerShell)
   git clone https://github.com/flutter/flutter.git -b stable
   # Add Flutter to PATH: flutter/bin
   
   # Verify installation
   flutter doctor
   ```

2. **Install Android Studio** (for Android builds)
   - Download from https://developer.android.com/studio
   - Install Android SDK and emulator
   - Accept licenses: `flutter doctor --android-licenses`

### Option 2: Using Android Studio Only (APK Build)
1. Download Android Studio
2. Install SDK and build tools
3. Create virtual device for testing

## Building the Mobile App

### Method 1: Flutter Build (Full Development)

1. **Navigate to mobile directory**
   ```bash
   cd mobile
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Build APK**
   ```bash
   # Debug APK (for testing)
   flutter build apk --debug
   
   # Release APK (for distribution)
   flutter build apk --release
   ```

4. **Build App Bundle (for Play Store)**
   ```bash
   flutter build appbundle --release
   ```

5. **Install on device**
   ```bash
   # Connect Android device via USB
   flutter install
   
   # Or install APK manually
   adb install build/app/outputs/flutter-apk/app-release.apk
   ```

### Method 2: Quick APK Generation (No Flutter Setup)

1. **Using GitHub Actions** (Automated)
   - Create `.github/workflows/build-apk.yml`
   - Push to GitHub
   - Download APK from Actions artifacts

2. **Using Codemagic** (Online Builder)
   - Connect GitHub repository
   - Configure build settings
   - Download generated APK

## Build Configuration

### Update App Information
Edit `mobile/pubspec.yaml`:
```yaml
name: cropguard_ai
description: AI-powered plant disease detection
version: 1.0.0+1

flutter:
  uses-material-design: true
  assets:
    - assets/images/
```

### App Signing (Release Build)
Create `mobile/android/key.properties`:
```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=your_key_alias
storeFile=path/to/keystore.jks
```

### Update App Icons
1. Replace icons in `mobile/android/app/src/main/res/mipmap-*/`
2. Or use Flutter launcher icons package:
   ```bash
   flutter pub add flutter_launcher_icons
   flutter pub run flutter_launcher_icons:main
   ```

## Build Output Locations

- **APK**: `mobile/build/app/outputs/flutter-apk/`
- **App Bundle**: `mobile/build/app/outputs/bundle/release/`
- **iOS** (macOS only): `mobile/build/ios/`

## Quick Build Script

Create `build_app.bat` (Windows) or `build_app.sh` (Linux/Mac):

```bash
#!/bin/bash
echo "Building CropGuard AI Mobile App..."
cd mobile
flutter clean
flutter pub get
flutter build apk --release
echo "APK built successfully!"
echo "Location: build/app/outputs/flutter-apk/app-release.apk"
```

## Testing the App

1. **Enable Developer Options** on Android device
2. **Enable USB Debugging**
3. **Connect device and run:**
   ```bash
   flutter run --release
   ```

## Distribution Options

### Direct Distribution
1. Build release APK
2. Share APK file directly
3. Users enable "Install from unknown sources"

### Google Play Store
1. Build App Bundle (`.aab` file)
2. Create Google Play Developer account ($25)
3. Upload app bundle and complete store listing

### Alternative App Stores
- Amazon Appstore
- Samsung Galaxy Store
- F-Droid (for open source)

## Troubleshooting

### Common Issues
1. **Flutter not recognized**: Add Flutter to system PATH
2. **Android license errors**: Run `flutter doctor --android-licenses`
3. **Gradle build failed**: Update Android SDK and build tools
4. **APK too large**: Enable code shrinking in `android/app/build.gradle`

### Size Optimization
```gradle
android {
    buildTypes {
        release {
            shrinkResources true
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### Performance Tips
- Use release builds for testing performance
- Enable R8 code shrinking
- Optimize images in assets folder
- Use vector drawables instead of multiple PNG sizes

## Automated Build (GitHub Actions)

Create `.github/workflows/build-apk.yml`:
```yaml
name: Build APK
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-java@v3
      with:
        distribution: 'zulu'
        java-version: '11'
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
    - name: Build APK
      working-directory: mobile
      run: |
        flutter pub get
        flutter build apk --release
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: app-release-apk
        path: mobile/build/app/outputs/flutter-apk/app-release.apk
```

This will automatically build APK on every push and make it downloadable from GitHub Actions.