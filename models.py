from pydantic import BaseModel 

class SignUp(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example" : {
                "email" : "sample",
                "password" : "sample12345"
            }
        }

class Login(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example" : {
                "email" : "sample",
                "password" : "sample12345"
            }
        }

class TokenData(BaseModel):
    access_token: str