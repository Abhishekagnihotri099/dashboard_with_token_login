from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

# Initialize FastAPI app
app = FastAPI()

# Predefined secret key and token configuration
SECRET_KEY = "q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6j7k8l9z0x1c2v3b4n5m6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Pydantic model for user authentication request
class TokenRequest(BaseModel):
    username: str

# Function to generate a JWT token
def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/generate-token")
def generate_token(request: TokenRequest):
    # Validate the username (you can enhance this with real validation logic)
    if not request.username:
        raise HTTPException(status_code=400, detail="Invalid username")

    # Create payload for the token
    payload = {"sub": request.username, "iat": datetime.utcnow()}

    # Generate token
    token = create_jwt_token(data=payload)
    
    return {"token": token}
