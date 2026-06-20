# 🚀 Setup Guide - Al Falah Academy CRM

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)
- PostgreSQL 16 (if running locally without Docker)

### Option 1: Docker (Recommended)

1. **Clone and navigate to project**
```bash
cd "AL FALAH ACADEMY — CRM SYSTEM"
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp ../.env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

## Initial Setup

### 1. Create First Admin User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@alfalahacademy.com",
    "password": "your-secure-password",
    "role": "super_admin"
  }'
```

### 2. Configure Stripe (Required for payments)

1. Get your Stripe API keys from https://dashboard.stripe.com/
2. Add to your `.env` file:
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

3. Set up webhook endpoint in Stripe dashboard:
   - URL: `https://your-domain.com/api/webhooks/stripe`
   - Events: `payment_intent.succeeded`, `payment_intent.payment_failed`, `customer.subscription.*`

### 3. Configure SendGrid (Required for emails)

1. Get your SendGrid API key from https://sendgrid.com/
2. Add to your `.env` file:
```
SENDGRID_API_KEY=SG.your_api_key
FROM_EMAIL=no-reply@alfalahacademy.com
```

### 4. Configure AWS S3 (Optional, for file storage)

1. Create an S3 bucket
2. Add to your `.env` file:
```
AWS_S3_BUCKET=alfalah-crm-uploads
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

## Database Migrations

### Create a new migration
```bash
cd backend
alembic revision --autogenerate -m "description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Development Workflow

### Adding New Features

1. **Backend:**
   - Add model in `backend/app/models/`
   - Add schema in `backend/app/schemas/`
   - Add router in `backend/app/routers/`
   - Register router in `backend/app/main.py`
   - Create migration: `alembic revision --autogenerate -m "feature_name"`

2. **Frontend:**
   - Add component in `frontend/components/`
   - Add page in `frontend/pages/`
   - Add composable in `frontend/composables/`
   - Update types as needed

### Code Quality

**Backend:**
```bash
cd backend
black .
ruff check .
mypy app/
pytest
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run typecheck
```

## Deployment

### Railway (Recommended)

1. Push code to GitHub
2. Create Railway account
3. Import repository
4. Add environment variables
5. Deploy

### Render

1. Push code to GitHub
2. Create Render account
3. Connect repository
4. Add environment variables
5. Deploy

### Manual Deployment

1. **Build frontend:**
```bash
cd frontend
npm run build
```

2. **Build backend Docker image:**
```bash
cd backend
docker build -t alfalah-crm-backend .
```

3. **Deploy to your server**
4. Configure Nginx reverse proxy
5. Set up SSL with Let's Encrypt

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database credentials

### Frontend Build Errors
- Clear node_modules: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`
- Check Node.js version: `node --version` (should be 20+)

### Backend Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Stripe Webhook Failures
- Verify webhook secret in .env
- Check webhook URL is publicly accessible
- Test with Stripe CLI: `stripe listen --forward-to localhost:8000/api/webhooks/stripe`

## Security Notes

- **Never commit .env files** to version control
- **Use strong secrets** for SECRET_KEY and database passwords
- **Enable HTTPS** in production
- **Keep dependencies updated**
- **Review audit logs** regularly
- **Implement rate limiting** on public endpoints
- **Use environment-specific** API keys (test vs production)

## Support

For issues or questions:
1. Check the README.md for documentation
2. Review API docs at `/docs` endpoint
3. Check logs in Docker: `docker-compose logs -f`
4. Review database migrations status

## Next Steps (Phase 2)

After completing Phase 1 setup, consider implementing:
- GSAP animations for dashboard
- Email templates and automation
- Advanced reporting with Chart.js
- QuickBooks integration
- JupiterEd integration for GaSSO
- SMS notifications
- Advanced analytics dashboard
