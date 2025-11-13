# 🧪 Quick Test Guide - JPEG Upload

## The Problem You Encountered

```
CORS policy: Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

This happens when testing locally because browsers block cross-origin requests for security.

## ✅ Solutions (Choose One)

### Option 1: Use the Local Development Server (Recommended)

```bash
# Start both frontend and backend servers
python start_local_server.py
```

This will:
- Start backend API at `http://localhost:8000`
- Start frontend at `http://localhost:3000`
- Open `http://localhost:3000/local-dev.html` automatically
- Handle CORS properly

### Option 2: Test with Python Script

```bash
# Quick automated test
python test_jpeg_upload.py
```

This tests both local and live APIs programmatically.

### Option 3: Use Live Web Version

Visit: **[cropguard-ai.vercel.app](https://cropguard-ai.vercel.app)**
- No setup required
- Upload JPEG/PNG instantly
- Test custom plant names

## 🔧 If Backend Not Running

1. **Install Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   Create `backend/.env`:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

3. **Start Backend:**
   ```bash
   cd backend
   python -m http.server 8000
   ```

## 📱 Test JPEG Upload - Step by Step

### Web Version Test:

1. **Go to:** [cropguard-ai.vercel.app](https://cropguard-ai.vercel.app) OR `http://localhost:3000/local-dev.html`

2. **Upload Test:**
   - Drag & drop any JPEG/PNG plant image
   - OR click to browse and select file

3. **Custom Plant Test:**
   - Select "Custom Plant..." from dropdown
   - Enter any plant name: "Mango", "Spinach", "Rose", etc.

4. **Analyze:**
   - Click "Analyze Disease"
   - Wait for AI results

### Mobile App Test:

1. **Build APK:**
   ```bash
   cd mobile
   flutter build apk --release
   ```

2. **Install on Device:**
   - Enable "Unknown sources" in Android settings
   - Install `build/app/outputs/flutter-apk/app-release.apk`

3. **Test Features:**
   - Take photo with camera (auto-detects JPEG)
   - Select custom plant option
   - Enter custom plant name
   - Get instant analysis

## 🐛 Troubleshooting

### Common CORS Errors:
- **Solution:** Use local development server or live version
- **Cause:** Direct file opening in browser blocks API calls

### "Feature is disabled":
- **Check:** Environment variables are set correctly
- **Verify:** Groq API key is valid and has credits

### Upload Fails:
- **File Size:** Must be under 10MB
- **Format:** Only JPEG, JPG, PNG supported
- **Network:** Check internet connection

### Backend Issues:
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Expected response:
{"status": "healthy", "groq_configured": true, ...}
```

## 🧪 Test with Sample Images

Create test images or use:
- **Healthy plant:** Any clear plant photo
- **Diseased plant:** Plant with visible spots/damage
- **Custom crops:** Any fruit/vegetable/flower images

## 🎯 Expected Results

**Healthy Plant:**
```json
{
  "disease": "Healthy Plant",
  "confidence": "85%",
  "ai_recommendation": "Plant appears healthy..."
}
```

**Diseased Plant:**
```json
{
  "disease": "Leaf Spot Disease",
  "confidence": "76%", 
  "ai_recommendation": "Apply fungicide treatment..."
}
```

## 🚀 Next Steps After Testing

1. **If tests pass:** Deploy web version and build mobile app
2. **If tests fail:** Check environment setup and API keys
3. **For production:** Set up custom domain and app store distribution

## 📞 Quick Support

**Most Common Issue:** Missing GROQ_API_KEY
- Get free key at: [console.groq.com/keys](https://console.groq.com/keys)
- Add to `backend/.env` file

**Still having issues?**
- Check browser console for detailed errors
- Try the live web version as fallback
- Use the Python test script for debugging

---

**🎉 Success Indicator:** When you can upload a JPEG image, enter a custom plant name like "Banana" or "Mango", and get an AI analysis result - you're all set!