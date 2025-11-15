# GUI Full-Stack Application

A full-stack web application with **Node.js Backend + Streamlit Frontend + Supabase Database**.

## 🎯 Architecture

- **Frontend:** Streamlit (Python) - User Interface
- **Backend:** Node.js + Express - API Server
- **Database:** Supabase (PostgreSQL) - Cloud Database
- **Hosting:** Vercel (Backend) + Streamlit Cloud (Frontend)

## 📋 Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- Git
- Supabase account (https://supabase.com)
- Vercel account (https://vercel.com)

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your Supabase credentials
npm run dev
```

### 2. Frontend Setup

```bash
cd streamlit-app
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your backend URL
streamlit run app.py
```

### 3. Database Setup

Create a Supabase project and run this SQL:

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

## 📚 Documentation

See the documentation files:
- `SETUP.md` - Complete setup guide
- `MIGRATION.md` - How code was migrated from original
- `QUICK_REFERENCE.md` - File reference and commands

## 🚀 Deployment

### Backend (Vercel)
```bash
cd backend
vercel --prod
```

### Frontend (Streamlit Cloud)
1. Push code to GitHub
2. Deploy via Streamlit Community Cloud UI
3. Add environment variables in Secrets

## 📁 Project Structure

```
.
├── backend/              # Node.js Express API
│   ├── api/             # API endpoints
│   ├── db/              # Database config
│   ├── middleware/      # Auth middleware
│   ├── server.js        # Main server
│   └── package.json
│
├── streamlit-app/       # Python Streamlit frontend
│   ├── app.py          # Main login page
│   ├── api/            # Backend client
│   ├── pages/          # Streamlit pages
│   └── requirements.txt
│
└── README.md
```

## 🔑 Environment Variables

### Backend (.env)
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
JWT_SECRET=your-secret-key
PORT=5000
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```env
BACKEND_URL=http://localhost:5000
```

## 🆘 Troubleshooting

- **Backend not connecting:** Check SUPABASE_URL and SUPABASE_KEY
- **Login fails:** Verify users table exists in Supabase
- **CORS error:** Update FRONTEND_URL in backend config

## 📞 Support

For issues, check:
1. Vercel logs (backend errors)
2. Streamlit terminal (frontend errors)
3. Supabase dashboard (database issues)

## 📜 License

MIT
