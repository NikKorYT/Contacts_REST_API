# Contacts REST API

A full-featured REST API for contact management with user authentication, built with FastAPI and PostgreSQL. Features include JWT authentication, email verification, avatar uploads, rate limiting, and comprehensive testing.

## What This Project Simulates

This project simulates a contact management service similar to Google Contacts or phone contact apps. Users can:

- Register accounts and verify emails
- Securely log in with JWT tokens  
- Create, read, update, and delete personal contacts
- Upload and manage profile avatars
- Search and filter through their contact lists
- Access rate-limited API endpoints for security

This represents a real-world backend service that could power a contact management application or CRM system.

## Technologies Used

- Framework: FastAPI with async/await support
- Database: PostgreSQL with SQLAlchemy ORM
- Authentication: JWT tokens with refresh token support
- Caching/Rate Limiting: Redis
- File Storage: Cloudinary for avatar uploads
- Email: SMTP integration for verification emails
- Testing: Pytest with async support and coverage
- Database Migrations: Alembic
- Containerization: Docker Compose for development
- Documentation: Sphinx for API docs

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Redis server
- Cloudinary account for file uploads
- SMTP server for emails (or MailHog for development)

## Installation

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd Contacts_REST_API
   ```

2. Install dependencies using Poetry
   ```bash
   pip install poetry
   poetry install
   ```

3. Set up environment variables
   
   Create `.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/contacts_db
   DATABASE_TEST_URL=postgresql+asyncpg://user:password@localhost:5432/test_contacts_db
   SECRET_KEY=your-secret-key-here
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-email-password
   MAIL_FROM=noreply@yourapp.com
   MAIL_PORT=587
   MAIL_SERVER=smtp.gmail.com
   CLOUDINARY_NAME=your-cloudinary-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=contacts_db
   ```

4. Start services with Docker Compose
   ```bash
   docker-compose up -d
   ```

5. Run database migrations
   ```bash
   poetry run alembic upgrade head
   ```

## Usage

### Start the API server
```bash
poetry run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token
- `POST /auth/refresh` - Refresh access token
- `GET /auth/verify/{token}` - Verify email address
- `POST /auth/avatar` - Upload user avatar

#### Contacts
- `GET /contacts/` - Get user's contacts (with pagination)
- `POST /contacts/` - Create new contact
- `GET /contacts/{contact_id}` - Get specific contact
- `PUT /contacts/{contact_id}` - Update contact
- `DELETE /contacts/{contact_id}` - Delete contact
- `GET /contacts/search` - Search contacts by name or email
- `GET /contacts/birthdays` - Get upcoming birthdays

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src

# Run specific test file
poetry run pytest tests/test_auth.py
```


## Key Features

### Authentication & Authorization
- JWT-based authentication with access and refresh tokens
- Password hashing with bcrypt
- Email verification for new accounts
- Protected endpoints requiring valid tokens

### Contact Management
- Full CRUD operations for contacts
- Search functionality by name and email
- Birthday tracking and upcoming birthday queries
- Pagination for large contact lists
- User-specific contact isolation

### API Security
- Rate limiting using Redis to prevent abuse
- CORS middleware for cross-origin requests
- Input validation with Pydantic schemas
- SQL injection protection with SQLAlchemy ORM

### File Management
- Avatar upload integration with Cloudinary
- Image processing and optimization
- Secure file storage with cloud CDN

### Development Features
- Async/await for high performance
- Comprehensive test suite with fixtures
- Database migrations with Alembic
- Docker Compose for easy development setup
- API documentation generation

## Development

### Database Migrations
```bash
# Create new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

### Testing
The project includes comprehensive tests covering:
- Authentication flows
- Contact CRUD operations
- Repository layer unit tests
- API endpoint integration tests

## Workflow

1. User Registration: Create account with email verification
2. Authentication: Login to receive JWT access token
3. Contact Management: Create and organize personal contacts
4. Profile Management: Upload avatar and manage account settings
5. Search & Filter: Find contacts using various criteria