# 🕌 Al Falah Academy — CRM System

A comprehensive, production-grade CRM web application tailored for Al Falah Academy, a K-12 Private Islamic School in Norcross, GA.

## 📋 Project Overview

**Client:** Al Falah Academy (AFA)  
**Mission:** "Developing Muslim Youth in Academics and Character"  
**Scale:** ~550 students, ~2,000 total constituents, 8-10 major events/year

This CRM system replaces fragmented QuickBooks + Excel workflows with a centralized platform for:
- Donor & fundraising management
- Islamic calendar-based giving campaigns (Ramadan, Dhul Hijjah)
- Event management & ticketing with QR check-in
- Constituent communications & email marketing
- GaSSO scholarship & pledge tracking
- Reporting & data export
- QuickBooks + JupiterEd integration

## 🛠️ Tech Stack

### Frontend
- **Framework:** Nuxt.js 3 (Vue 3 Composition API)
- **Styling:** Tailwind CSS v3 (custom AFA brand colors)
- **Animation:** GSAP 3 + @vueuse/motion
- **State:** Pinia
- **Charts:** Chart.js + Apache ECharts
- **Forms:** VeeValidate + Zod
- **Calendar:** vue-cal + Hijri converter

### Backend
- **Framework:** FastAPI (Python 3.12+)
- **ORM:** SQLAlchemy 2.0 + Alembic
- **Database:** PostgreSQL 16 + Redis
- **Auth:** JWT + OAuth2 with MFA
- **Payment:** Stripe SDK
- **Email:** FastAPI-Mail + SendGrid
- **Background Jobs:** Celery + Redis

### Infrastructure
- Docker + Docker Compose
- Nginx reverse proxy
- GitHub Actions CI/CD

## 🎨 Design System

### Color Palette
- **Primary Gold:** `#C9A84C` (CTAs, highlights)
- **Deep Navy:** `#1B2A4A` (headers, backgrounds)
- **Ivory White:** `#FAF8F3` (page backgrounds)
- **Emerald Green:** `#2E7D52` (success, Islamic accent)
- **Warm Charcoal:** `#2D2D2D` (body text)

### Typography
- **Display:** Playfair Display
- **Body:** Inter
- **Arabic:** Amiri
- **Mono:** JetBrains Mono

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)

### Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd "AL FALAH ACADEMY — CRM SYSTEM"
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
alfalah-crm/
├── frontend/              # Nuxt.js application
│   ├── components/        # Vue components
│   ├── composables/       # Vue composables
│   ├── layouts/           # Nuxt layouts
│   ├── pages/             # Nuxt pages
│   ├── stores/            # Pinia stores
│   └── utils/             # Utilities
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── routers/       # API routes
│   │   ├── services/      # Business logic
│   │   └── tasks/         # Celery tasks
│   ├── migrations/        # Alembic migrations
│   └── tests/             # Pytest tests
├── docker-compose.yml
├── nginx.conf
└── README.md
```

## 🔐 Authentication

### Roles
- `super_admin` - Full access
- `admin` - All modules except user management
- `development` - Donors, donations, campaigns, GaSSO, reports
- `events` - Events module only
- `read_only` - View-only access

### Default Admin
Create first admin via API:
```bash
POST /api/auth/register
{
  "email": "admin@alfalahacademy.com",
  "password": "your-secure-password",
  "role": "super_admin"
}
```

## 🕌 Islamic Features

### Hijri Calendar
- Dual date display: "June 19, 2026 | 23 Dhul Hijjah 1447"
- Islamic campaign automation (Ramadan, Dhul Hijjah)
- Hijri-based recurring donations

### Islamic UX
- Bismillah in donation forms
- Islamic significance donation presets ($5, $30, $313, $1,000)
- Crescent moon + star icons
- Geometric Islamic pattern backgrounds

## 📊 Key Features

### Donor Management
- Constituent CRUD with flexible codes
- Soft delete only (never hard delete)
- Giving history with trend analysis
- Soft credit tracking

### Donation Tracking
- One-time, recurring, pledge, in-kind
- Multiple payment methods (Stripe, PayPal, Square, Zelle, Check, Cash)
- Hijri date storage
- Anonymous donations

### Campaign Management
- General, Ramadan, Dhul Hijjah, Annual, Event, GaSSO types
- Goal tracking with progress
- Islamic calendar integration

### Event Management
- Ticketing with QR codes
- Mobile check-in with camera
- Sponsorship tracking
- Capacity management

### GaSSO Scholarship
- Pipeline: Pledged → Approved → Partially Funded → Fully Funded
- Soft credit application
- Stage history audit trail
- Reconciliation reports

## 🧪 Testing

**Backend:**
```bash
cd backend
pytest
```

**Frontend:**
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Production Deployment
1. Set up Railway/Render account
2. Configure environment variables
3. Push to GitHub
4. Connect repository to Railway/Render
5. Deploy

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 🔗 Integrations

- **QuickBooks Online** - Two-way sync
- **JupiterEd** - Student data for GaSSO
- **Stripe** - Payment processing
- **SendGrid** - Email delivery
- **AWS S3** - File storage

## 📝 License

Proprietary - Al Falah Academy

## 🙏 Acknowledgments

Built for Al Falah Academy to support their mission of "Developing Muslim Youth in Academics and Character."
