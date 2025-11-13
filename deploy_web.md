# Web Version Deployment Guide

## Deploy to Vercel (Recommended)

### Prerequisites
- Vercel account (free)
- GitHub repository
- Environment variables configured

### Step 1: Prepare Files
Ensure these files exist in your repository:
- `web/index.html` (web application)
- `vercel.json` (deployment configuration)
- `backend/api/*.py` (API endpoints)

### Step 2: Deploy via Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel
```

### Step 3: Configure Environment Variables
In Vercel Dashboard, add:
- `GROQ_API_KEY` - Your Groq API key
- `SUPABASE_URL` - Supabase project URL  
- `SUPABASE_KEY` - Supabase anon key

### Step 4: Set Custom Domain (Optional)
1. Go to Vercel project dashboard
2. Add custom domain in Settings > Domains
3. Configure DNS records as instructed

## Deploy to Netlify (Alternative)

### Step 1: Prepare for Static Hosting
```bash
# Create _redirects file for SPA routing
echo "/* /index.html 200" > web/_redirects

# Create netlify.toml
cat > netlify.toml << EOF
[build]
  publish = "web"

[[redirects]]
  from = "/api/*"
  to = "https://your-vercel-backend.vercel.app/api/:splat"
  status = 200
EOF
```

### Step 2: Deploy
1. Connect GitHub repository to Netlify
2. Set publish directory to `web`
3. Deploy automatically on push

## Deploy to GitHub Pages

### Step 1: Enable GitHub Pages
1. Go to repository Settings > Pages
2. Select source: Deploy from branch
3. Choose branch: main, folder: /web

### Step 2: Update API URLs
Update `web/index.html` to use your backend URL:
```javascript
const API_BASE = 'https://your-backend.vercel.app/api';
```

## Local Development Server

### Simple Python Server
```bash
cd web
python -m http.server 8000
# Access at: http://localhost:8000
```

### Node.js Server
```bash
cd web
npx http-server -p 8000
# Access at: http://localhost:8000
```

## Testing Deployment

### Health Check URLs
- Web app: `https://your-domain.com`
- API health: `https://your-domain.com/api/health`
- Test detection: `https://your-domain.com/api/detect`

### Test Checklist
- [ ] Web page loads correctly
- [ ] Image upload works (drag & drop)
- [ ] Plant type selection works
- [ ] Custom plant name input works  
- [ ] Disease detection API responds
- [ ] Results display correctly
- [ ] Mobile responsive design
- [ ] CORS headers configured
- [ ] HTTPS enforced

## Troubleshooting

### Common Issues

**1. API CORS Errors**
```javascript
// Add to vercel.json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "POST, OPTIONS" },
        { "key": "Access-Control-Allow-Headers", "value": "Content-Type" }
      ]
    }
  ]
}
```

**2. Large Image Upload Fails**
- Increase Vercel function timeout in `vercel.json`
- Add image compression in frontend
- Validate file size before upload

**3. Environment Variables Not Working**
- Verify variable names match exactly
- Check variable values don't have extra spaces
- Restart deployment after adding variables

### Performance Optimization

**1. Image Compression**
```javascript
// Add to web frontend
function compressImage(file, quality = 0.8) {
  return new Promise((resolve) => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      
      canvas.toBlob(resolve, 'image/jpeg', quality);
    };
    
    img.src = URL.createObjectURL(file);
  });
}
```

**2. Caching Headers**
```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000" }
      ]
    }
  ]
}
```

## Custom Domain Setup

### Step 1: Purchase Domain
- Namecheap, GoDaddy, or Google Domains
- Choose something like: `cropguard.ai` or `plantdoctor.app`

### Step 2: Configure DNS
```
Type: CNAME
Name: www
Value: your-vercel-app.vercel.app

Type: A
Name: @
Value: 76.76.19.19 (Vercel's IP)
```

### Step 3: Add to Vercel
1. Project Settings > Domains
2. Add custom domain
3. Wait for SSL certificate generation

## Production Checklist

- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] Environment variables set
- [ ] API endpoints working
- [ ] Error handling implemented
- [ ] Analytics added (optional)
- [ ] SEO meta tags added
- [ ] Mobile responsiveness tested
- [ ] Load testing completed
- [ ] Backup strategy in place