# Complete Setup Guide

## Step 1: Supabase Setup

1. Go to https://supabase.com
2. Create new project
3. Go to SQL Editor and run:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  role VARCHAR(50) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

4. Get credentials from Settings → API

## Step 2: Backend Deployment

```bash
cd backend
npm install
cp .env.example .env
# Edit .env with Supabase credentials
npm install -g vercel
vercel --prod
```

## Step 3: Frontend Deployment

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Deploy new app
4. Add BACKEND_URL in Secrets

## Step 4: Verify

- Backend: https://your-backend.vercel.app/health
- Frontend: https://your-app.streamlit.app
