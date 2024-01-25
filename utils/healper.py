
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt

secret = "DARJIKARTVYA"

token = HTTPBearer()



