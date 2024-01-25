


from passlib.context import CryptContext
from model.model import Login

from serializer.serializer import convert_user
from config.config import user_collection

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from bson import ObjectId





# for password authentication

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(plain_password):
    return pwd_context.hash(plain_password)

def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

# user verification

def check_user(data : Login):
    user = user_collection.find_one({"email" : data.email})
    user = convert_user(user)
    print(user)

    if user.get("email") == data.email and verify_password(data.password, user.get("password")):
        return True
    return False

# token verification

secret = "DARJIKARTVYA"

token = HTTPBearer()

def create_token(payload) : 
    return jwt.encode(payload, secret)

def decode_token(token : str) :
    try :
        return jwt.decode(token, secret)
    except :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

def check_auth(token = Depends(token)):
    # print(token)
    token = token.credentials
    # print(token)
    user_data = decode_token(token)
    # print(user_data)
    user = user_collection.find_one({"_id" : ObjectId(user_data["_id"])})
    # print(user)
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user