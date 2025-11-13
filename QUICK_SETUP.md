# 🚀 CropGuard AI - Quick Setup Guide

## 🌐 Try Instantly (No Setup Required)
**Web Version:** [cropguard-ai.vercel.app](https://cropguard-ai.vercel.app)
- Upload JPEG/PNG images
- Enter custom plant names
- Get instant AI analysis

## 📱 Download Mobile App
**Android APK:** [Latest Release](https://github.com/sibikrishna/cropguard-ai/releases/latest/download/app-release.apk)

### Installation Steps:
1. Download APK file
2. Enable "Install from unknown sources" 
3. Install APK on Android device
4. Start scanning plants!

## 🔧 Developer Setup (5 Minutes)

### Backend Setup
```bash
git clone https://github.com/sibikrishna/cropguard-ai.git
cd cropguard-ai/backend
pip install -r requirements.txt

# Create .env file
GROQ_API_KEY=your_groq_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Run locally
python simple_test.py
```

### Mobile App Setup
```bash
cd mobile
flutter pub get
flutter run
```

## 🎯 Key Features Implemented

✅ **JPEG & PNG Support** - Upload any image format  
✅ **Custom Plant Names** - Not limited to predefined crops  
✅ **Web Version Live** - Instant browser access  
✅ **Mobile App Ready** - Download APK or build from source  
✅ **Enhanced Camera** - Better image quality and format detection  

## 🧪 Test JPEG Upload

### Web Version Test:
1. Go to [cropguard-ai.vercel.app](https://cropguard-ai.vercel.app)
2. Upload a JPEG image of any plant
3. Select "Custom Plant..." from dropdown
4. Enter plant name (e.g., "Mango", "Spinach", "Banana")
5. Click "Analyze Disease"
6. Get AI-powered results!

### Mobile App Test:
1. Install APK on Android device
2. Take photo with camera (auto-detects JPEG format)
3. Select "Custom Plant..." option
4. Enter custom plant name
5. Analyze and get treatment recommendations

## 🌍 Deployment Options

### Web Deployment (Vercel)
- Push to GitHub
- Connect to Vercel
- Auto-deploys on push
- **Guide:** [deploy_web.md](deploy_web.md)

### Mobile App Distribution
- **GitHub Releases**: Automatic APK builds
- **Direct APK**: Share file directly
- **Google Play**: Upload app bundle
- **Guide:** [build_mobile_app.md](build_mobile_app.md)

## 🆘 Quick Troubleshooting

### Web Version Issues:
- **Upload fails**: Check file size (max 10MB)
- **Analysis fails**: Verify internet connection
- **Custom plant not working**: Ensure text field has input

### Mobile App Issues:
- **APK won't install**: Enable unknown sources
- **Camera not working**: Grant camera permissions
- **Analysis slow**: Check network connection

### Backend Issues:
- **API errors**: Check Groq API key validity
- **Dependencies**: Run `pip install -r requirements.txt`
- **Environment**: Ensure `.env` file exists

## 📚 Next Steps

1. **Try the live demo** at [cropguard-ai.vercel.app](https://cropguard-ai.vercel.app)
2. **Download APK** and test on Android device
3. **Star the repository** if you find it useful
4. **Report issues** on GitHub if you encounter problems
5. **Contribute** by submitting PRs or suggestions

## 🤝 Get Involved

- **GitHub:** [sibikrishna/cropguard-ai](https://github.com/sibikrishna/cropguard-ai)
- **Issues:** [Report bugs](https://github.com/sibikrishna/cropguard-ai/issues/new)
- **Discussions:** [Feature requests](https://github.com/sibikrishna/cropguard-ai/discussions)

---

**Built with ❤️ for farmers worldwide | UN SDG 2 (Zero Hunger) Initiative**