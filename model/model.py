from pydantic import BaseModel, EmailStr


class SignUp(BaseModel):
    fullname : str
    email : EmailStr
    password : str
    confirm_password : str

    class Config:
        json_schema_extra = {
            "example" : {
                "fullname" : "darji kartvya",
                "email" : "abc@123.com",
                "password" : "123",
                "confirm_password" : "123"
            }
        }

class Login(BaseModel):
    email : EmailStr
    password : str

    class Config:
        json_schema_extra = {
            "example" : {
                "email" : "abc@123.com",
                "password" : "123"
            }
        }

class Sample(BaseModel): 
    title : str
    price : int
    rating : int
    content : str
    