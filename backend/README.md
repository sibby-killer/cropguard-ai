# CropGuard AI - Backend API

Backend API for CropGuard AI plant disease detection system.

## Features

- 🤖 AI-powered disease detection using Groq Vision API
- 📸 Image preprocessing and enhancement
- 💾 Scan history storage in Supabase
- 🔍 Comprehensive disease information database
- 🌐 RESTful API with CORS support

## Tech Stack

- **Runtime**: Python 3.9+
- **AI**: Groq AI (llama-3.2-90b-vision-preview)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Hosting**: Vercel Serverless Functions

## API Endpoints

### 1. Detect Disease
POST /api/detect

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "user_id": "uuid",
  "crop_type": "tomato"
}
```

**Response:**
```json
{
  "success": true,
  "disease": "Late Blight",
  "confidence": 95.5,
  "severity": "Severe",
  "symptoms": [...],
  "treatment": [...],
  "prevention": [...]
}
```

### 2. Get History
GET /api/history?user_id=xxx&limit=50

### 3. Get Disease Info
GET /api/diseases?name=Late%20Blight
GET /api/diseases?search=tomato
GET /api/diseases (list all)

### 4. Health Check
GET /api/health

## Setup Instructions

See main README.md for complete setup guide.

## Environment Variables

- `GROQ_API_KEY`: Your Groq API key
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally (requires Vercel CLI)
vercel dev
```

## Deployment
```bash
# Deploy to Vercel
vercel

# Set environment variables
vercel env add GROQ_API_KEY
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY

# Deploy to production
vercel --prod
```