from pydantic import BaseModel 

class SignUp(BaseModel):
    email: str
    password: str
    full_name: str

    class Config:
        schema_extra = {
            "example" : {
                "email" : "sample",
                "password" : "sample12345",
                "full_name" : "Ex Sample"
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

