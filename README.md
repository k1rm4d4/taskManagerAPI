# Task Manager API

A simple RESTful API built with Flask for managing tasks, including CRUD operations and JWT-based user authentication.

## Setup Instructions

1. Clone the repository: git clone: https://github.com/k1rm4d4/taskManagerAPI
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables: Create .env file with:
```
DATABASE_URL="sqlite:///./tasks_manager.sqlite"
SECRET_KEY="<your_secret_key>"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
   You can have any secret key for testing.
   
4. Initialize the database: 
   From root of project, run: `alembic upgrade head`

## Running the Application

From root of project:
1. Run the app: `flask --app app/ run`
2. Access the API at http://localhost:5000/
3. For Swagger UI: http://localhost:5000/swagger

## API Documentation

- Swagger UI available at /swagger for interactive docs, including request/response examples.

## Testing

- Run tests(from root of project): `python3 -m pytest -q`

## Additional Notes

- Authentication: Use /auth/register and /auth/login to get JWT. Protected routes require Bearer token.