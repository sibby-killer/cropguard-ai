# 🚀 CropGuard AI - Quick Start Guide

Get CropGuard AI running in **30 minutes** with this step-by-step guide.

## ⚡ Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9+ installed
- [ ] Flutter 3.0+ and Dart SDK
- [ ] Node.js 18+ (for Vercel CLI)
- [ ] Git installed
- [ ] Android device or emulator

## 🔑 Step 1: Get Your API Keys (5 minutes)

### Groq API Key (FREE)
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up with Google/GitHub
3. Go to "API Keys" → "Create API Key"
4. Copy key (starts with `gsk_`)

### Supabase Setup (FREE)
1. Visit [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings → API
4. Copy URL and anon key

## 📥 Step 2: Clone & Setup (10 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/cropguard-ai.git
cd cropguard-ai

# Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env

# Edit .env file with your keys
# GROQ_API_KEY=your_groq_key_here
# SUPABASE_URL=your_supabase_url_here
# SUPABASE_KEY=your_supabase_key_here
```

## 🗄️ Step 3: Database Setup (5 minutes)

In Supabase SQL Editor, paste and run:

```sql
-- Create scans table
CREATE TABLE scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    image_url TEXT NOT NULL,
    crop_type VARCHAR(100),
    disease_detected VARCHAR(200) NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    severity VARCHAR(20),
    recommendations TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE scans ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can only view own scans" ON scans
    FOR ALL USING (auth.uid() = user_id);

-- Create storage bucket
INSERT INTO storage.buckets (id, name, public) 
VALUES ('scan-images', 'scan-images', true);

-- Storage policies
CREATE POLICY "Anyone can upload scan images" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'scan-images');

CREATE POLICY "Anyone can view scan images" ON storage.objects
    FOR SELECT USING (bucket_id = 'scan-images');
```

## 🚀 Step 4: Deploy Backend (5 minutes)

```bash
# Install Vercel CLI
npm install -g vercel

# Login and deploy
vercel login
vercel

# Set environment variables
vercel env add GROQ_API_KEY
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY

# Deploy to production
vercel --prod

# Copy the URL (e.g., https://cropguard-ai.vercel.app)
```

## 📱 Step 5: Setup Mobile App (5 minutes)

```bash
cd mobile

# Install dependencies
flutter pub get

# Update API URL in lib/services/api_service.dart
# Change line 10: static const String baseUrl = 'https://YOUR-APP.vercel.app/api';

# Update Supabase config in lib/main.dart
# Change lines 12-15 with your Supabase URL and key

# Run the app
flutter run

# Or build APK
flutter build apk --release
```

## ✅ Step 6: Test Everything

1. **Health Check:**
   ```bash
   curl https://your-app.vercel.app/api/health
   ```

2. **Mobile App:**
   - Open app
   - Tap "Scan Your Crop"
   - Select "Tomato"
   - Take/upload plant photo
   - Tap "Analyze Disease"
   - View results!

## 🎉 You're Done!

Your CropGuard AI system is now running! 

### Next Steps:
- [ ] Test with different crop photos
- [ ] Check scan history
- [ ] Share APK with friends
- [ ] Contribute to the project

### Need Help?
- 📖 Full README: [README.md](../README.md)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/cropguard-ai/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/cropguard-ai/discussions)

---
**Made with 💚 for farmers worldwide**