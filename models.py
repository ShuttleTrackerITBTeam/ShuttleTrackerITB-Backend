from pydantic import BaseModel 

class SignUp(BaseModel):
    email: str
    password: str
    username: str

    class Config:
        schema_extra = {
            "example" : {
                "email" : "sample",
                "password" : "sample12345",
                "username" : "Ex Sample"
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

