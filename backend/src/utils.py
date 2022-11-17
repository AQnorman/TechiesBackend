import fastapi.security as _security

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "techiessecurity"
JWT_ALGORITHM = "HS256"
