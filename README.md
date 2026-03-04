# Events API

A Flask-based REST API for managing events and RSVPs with different access levels. Features a complete CI/CD pipeline with Docker containerization and automated deployment to Render.

## Features

- **Public Events**: Anyone can RSVP without authentication
- **Protected Events**: Requires user authentication to RSVP
- **Admin Events**: Requires admin role to RSVP
- **JWT Authentication**: Secure token-based authentication
- **Swagger Documentation**: Interactive API documentation at `/apidocs`
- **Automated CI/CD**: GitHub Actions pipeline with Docker Hub integration
- **Cloud Deployment**: Automated deployment to Render with smoke tests

## Tech Stack

### Backend
- Flask 3.0.0
- Flask-SQLAlchemy (SQLite database)
- Flask-CORS
- Flask-JWT-Extended (JWT authentication)
- Flask-Swagger-UI

### DevOps & Infrastructure
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Container Registry**: Docker Hub
- **Deployment**: Render
- **Testing**: pytest

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ell-716/Events-API.git
   cd Events-API
   ```

2. **Create and activate a virtual environment:**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Running with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t events-api:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 5000:5000 --name events-api events-api:latest
   ```

3. **Access the API:**
   - API: `http://localhost:5000`
   - Swagger UI: `http://localhost:5000/apidocs`

4. **Stop and remove the container:**
   ```bash
   docker stop events-api
   docker rm events-api
   ```

### Using Docker Hub Image

```bash
docker pull elenabai83/events-api:latest
docker run -d -p 5000:5000 elenabai83/events-api:latest
```

## Testing

The project includes comprehensive unit and integration tests using `pytest`.

### Running Tests Locally

1. **Make sure the API server is running:**
   ```bash
   python app.py
   ```

2. **In a separate terminal, activate the virtual environment and run:**
   ```bash
   pytest -v
   ```

### Test Structure

- `tests/test_models.py` — Unit tests (e.g. password hashing), no server required
- `tests/test_api.py` — Integration tests against the running API
- `tests/conftest.py` — Shared test configuration and helpers

### CI/CD Testing

Tests run automatically on every push to `main` via GitHub Actions:
1. Docker image is built
2. Container is started
3. Health check is performed
4. Full test suite runs with pytest
5. Container is cleaned up

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Stages

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│   Build &   │ ──> │  Run Tests   │ ──> │  Push to    │ ──> │   Deploy to  │
│  Container  │     │  (pytest)    │     │ Docker Hub  │     │    Render    │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                                                                      │
                                                                      ▼
                                                              ┌──────────────┐
                                                              │ Smoke Tests  │
                                                              │ (Health API) │
                                                              └──────────────┘
```

### Workflow Steps

1. **Build**: Docker image is built from `Dockerfile`
2. **Test**: 
   - Container starts and health check runs
   - Full pytest suite executes
3. **Push**: Image is tagged and pushed to Docker Hub
   - `latest` tag
   - Git SHA tag for versioning
4. **Deploy**: Render deployment is triggered via webhook
5. **Smoke Test**: Health endpoint is verified on production

### Environment Secrets

Required GitHub environment secrets (`prod` environment):
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token
- `RENDER_DEPLOY_HOOK` - Render deploy webhook URL
- `RENDER_BASE_URL` - Production API base URL

## API Documentation

### Swagger UI

The API includes interactive Swagger UI documentation:

1. **Local**: Navigate to `http://localhost:5000/apidocs`
2. **Production**: Navigate to `https://events-api-8dv6.onrender.com/apidocs`

Features:
- Browse all available endpoints
- See request/response schemas
- Test endpoints directly from the browser
- Authenticate using the "Authorize" button

**To authenticate:**
1. Login via `/api/auth/login` to get your JWT token
2. Click "Authorize" button at the top
3. Enter: `Bearer <your_jwt_token>`
4. Test protected endpoints directly

**OpenAPI Spec**: Available at `/apispec_1.json`

## API Endpoints

### Health Check

- `GET /api/health` - API health status (no authentication required)

### Authentication

- `POST /api/auth/register` - Register a new user
  ```json
  {
    "username": "user123",
    "email": "user@example.com",
    "password": "password123"
  }
  ```

- `POST /api/auth/login` - Login and get JWT token
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```
  **Response:**
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```

### Events

- `GET /api/events` - Get all events
- `GET /api/events/<id>` - Get a specific event
- `POST /api/events` - Create a new event (requires authentication)
  ```json
  {
    "title": "Python Meetup",
    "description": "Monthly Python developer meetup",
    "date": "2026-01-15T18:00:00",
    "location": "Tech Hub, Room 101",
    "capacity": 50,
    "is_public": true,
    "requires_admin": false
  }
  ```

### RSVPs

- `POST /api/rsvps/event/<event_id>` - RSVP to an event
  ```json
  {
    "attending": true
  }
  ```

- `GET /api/rsvps/event/<event_id>` - Get all RSVPs for an event (requires authentication)

## Authentication

For protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Project Structure

```
Events-API/
├── app.py                  # Main application entry point
├── models.py               # Database models (User, Event, RSVP)
├── config.py               # Configuration settings
├── openapi.yaml            # OpenAPI specification
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI/CD pipeline
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Authentication endpoints
│   ├── events.py           # Event management endpoints
│   └── rsvps.py            # RSVP endpoints
└── tests/
    ├── conftest.py         # pytest configuration
    ├── test_models.py      # Unit tests
    └── test_api.py         # Integration tests
```

## Database

The application uses SQLite by default. The database file (`events.db`) will be created automatically on first run.

**Schema:**
- **Users**: id, username, email, password_hash, is_admin
- **Events**: id, title, description, date, location, capacity, is_public, requires_admin
- **RSVPs**: id, user_id, event_id, attending

**Note**: The first user registered automatically becomes an admin for demo purposes.

## Deployment

### Manual Deployment to Render

1. **Create a new Web Service** on Render
2. **Deploy from Docker Image**: `elenabai83/events-api:latest`
3. **Configure**:
   - Port: `5000`
   - Environment variables (if needed): `JWT_SECRET_KEY`

### Automated Deployment

Deployment happens automatically on every push to `main`:
1. GitHub Actions builds and tests the Docker image
2. Image is pushed to Docker Hub
3. Render deployment webhook is triggered
4. New version deploys to production
5. Smoke tests verify the deployment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational purposes.

---

**Built with ❤️ as part of the "From Dev to Prod" course**