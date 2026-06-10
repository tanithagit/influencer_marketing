# Influencer Marketing Platform

A full-stack SaaS platform that connects **Brands** with **Influencers** through structured campaigns, with real payment handling, deliverable tracking and analytics.

---

##  Tech Stack

### Backend
- **FastAPI** — Python web framework
- **PostgreSQL** — Database
- **SQLAlchemy** — ORM
- **Alembic** — Database migrations
- **JWT** — Authentication
- **Stripe** — Payment processing
- **FastAPI-Mail** — Email notifications

### Frontend
- **React + Vite** — UI framework
- **Tailwind CSS** — Styling
- **React Router** — Navigation
- **Axios** — HTTP client

---

##  System Roles

| Role | Permissions |
|------|-------------|
| **Brand** | Create campaigns, review applications, approve deliverables, release payments |
| **Influencer** | Browse campaigns, apply, submit deliverables, track earnings |
| **Admin** | Verify users, monitor all transactions, platform overview |

---

## Project Structure

influencer-marketing-platform/
├── backend/
│   ├── app/
│   │   ├── api/routes/      # All API endpoints
│   │   ├── core/            # Config, database, dependencies
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # JWT, password helpers
│   ├── alembic/             # Database migrations
│   ├── tests/               # Pytest tests
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/           # Auth, Brand, Influencer, Admin pages
│       ├── components/      # Reusable UI components
│       ├── services/        # API service functions
│       └── context/         # Auth context
└── uploads/                 # User uploaded files

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+

---

### 1. Clone Repository
```bash
git clone https://github.com/tanithagit/influencer_marketing.git
cd influencer_marketing
```

---

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your actual values
```

---

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE influencer_db;
\q

# Run migrations
alembic upgrade head
```

---

### 4. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

---

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:5173`



##  Campaign Workflow

## Payment Flow

>  Payment CANNOT be released before deliverable is approved

---

##  Subscription Plans

| Plan | Role | Limits |
|------|------|--------|
| Free Brand | Brand | Max 3 active campaigns |
| Premium Brand | Brand | Unlimited campaigns + advanced analytics |
| Free Influencer | Influencer | Max 10 applications/month |
| Pro Influencer | Influencer | Unlimited applications + priority ranking |

---

##  Authentication

- JWT Bearer token authentication
- Tokens expire after 30 minutes
- Role-based route protection
- Three roles: `brand`, `influencer`, `admin`

---

## 📧 Email Notifications

Emails are sent for:
- ✅ New user registration (welcome email)
- ✅ Application approved/rejected
- ✅ Deliverable reviewed
- ✅ Payment released

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get token |
| GET | `/api/auth/me` | Get current user |

### Campaigns
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/campaigns/` | List active campaigns |
| POST | `/api/campaigns/` | Create campaign (Brand) |
| GET | `/api/campaigns/{id}` | Get campaign by ID |
| PUT | `/api/campaigns/{id}` | Update campaign |
| DELETE | `/api/campaigns/{id}` | Cancel campaign |

### Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/applications/campaign/{id}` | Apply to campaign |
| GET | `/api/applications/my-applications` | Get my applications |
| PUT | `/api/applications/{id}/approve` | Approve application |
| PUT | `/api/applications/{id}/reject` | Reject application |

### Deliverables
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/deliverables/campaign/{id}` | Submit deliverable |
| GET | `/api/deliverables/my-deliverables` | Get my deliverables |
| PUT | `/api/deliverables/{id}/approve` | Approve deliverable |
| PUT | `/api/deliverables/{id}/reject` | Reject deliverable |

### Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/create-intent` | Create escrow payment |
| PUT | `/api/payments/{id}/release` | Release payment |
| GET | `/api/payments/my-earnings` | Get earnings |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/brand/dashboard` | Brand analytics |
| GET | `/api/analytics/influencer/dashboard` | Influencer analytics |
| GET | `/api/analytics/admin/overview` | Admin overview |

---

##  Running Tests

```bash
cd backend
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

##  Architecture Decisions

### Why FastAPI?
- Automatic API documentation with Swagger UI
- Built-in data validation with Pydantic
- High performance async support
- Easy JWT integration

### Why PostgreSQL?
- Reliable relational database
- Excellent support for complex queries
- Strong data integrity with foreign keys

### Why Alembic?
- Version-controlled database schema
- Safe migrations in production
- Easy rollback support

### Why Stripe?
- Industry standard payment processing
- Secure escrow-style payment holding
- Webhook support for payment events

### Escrow Payment Design
Payments are held in escrow until deliverable is approved, protecting both brands (don't pay for bad work) and influencers (payment is secured before work begins).

---

##  Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Brand | brand@test.com | password123 |
| Influencer | influencer@test.com | password123 |
| Admin | Set via database | password123 |

---

##  License

MIT License — Free to use for educational purposes.