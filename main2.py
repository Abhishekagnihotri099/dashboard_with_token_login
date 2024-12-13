from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import jwt

# Initialize FastAPI app
app = FastAPI()

# Predefined secret key and token configuration
SECRET_KEY = "q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6j7k8l9z0x1c2v3b4n5m6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Function to generate a JWT token
def create_jwt_token(expires_delta: timedelta = None):
    to_encode = {"iat": datetime.utcnow()}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/generate-token")
def generate_token():
    # Generate token without any payload
    token = create_jwt_token()
    return {"token": token}
