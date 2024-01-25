from fastapi import APIRouter, Depends, HTTPException, Query, status
from model.model import Sample, SignUp, Login
from config.config import user_collection, sample_collection
from serializer.serializer import convert_samples, convert_user, convert_users

from auth.auth import check_user, get_hash_password, verify_password, create_token,  check_auth

route = APIRouter()

@route.post("/user/signup", tags=["signup"])
def sign_up(user : SignUp):
    check_user = user_collection.find_one({"email" : user.email})
    if check_user is None :
        if user.password == user.confirm_password:
            user.password = get_hash_password(user.password)
            user.confirm_password = get_hash_password(user.confirm_password)
            user_collection.insert_one(dict(user))
            return {
                "Status" : "OK",
                "Message" : "Sign-Up Successfully"
            }
        else : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password and Confirm-Password do not match")
    else : 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Alread Exist !")


@route.post("/user/login", tags=["login"])
def login_user(user : Login):

    if not check_user(user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User")

    user = user_collection.find_one({"email": user.email})
    # print(user)
    user = convert_user(user)
    # print(user)
    token_payload = {
        "_id" : user.get('_id')
    }
    print(token_payload)

    token = create_token(token_payload)

    return {
        "user" : user,
        "token" : token
    }
    

@route.post("/sample/post", tags=["sample"])
def post_sample(post: Sample, user = Depends(check_auth)):
    print("This post is created by", user.get("fullname"))
    sample_collection.insert_one(dict(post))
    return{
        "status" : "OK",
        "Message" : "Post added Successfully"
    }

@route.get("/sample/get", tags=["sample"])
def read_all_sample():
    samples = sample_collection.find()
    samples = convert_samples(samples)
    return {
        "status" : "OK",
        "data" : samples
    }


# aggregate

@route.get("/aggregate", tags=["pagination"])
def read_by_conditions(page: int = Query(ge=1), limit: int = Query(ge=1,le=20), title: str = Query(min_length=1), sort: bool = Query(default=None)):

    sort_value = 1 if sort else -1

    new_data = sample_collection.aggregate([
        {
            "$match" : {
                "title" : {
                    "$regex" : title
                }
            }
        },
        {
            "$skip" : (page-1) * limit
        },
        {
            "$limit" : limit
        },
        {
            "$sort" :  {
                "price" : sort_value
            }
        }
    ])

    data = convert_samples(new_data)

    return {
        "status" : "OK",
        "data" : data
    }