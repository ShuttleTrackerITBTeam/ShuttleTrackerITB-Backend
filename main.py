from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pyrebase import pyrebase
from models import SignUp, Login
from jose import jwt, JWTError

import uvicorn

app = FastAPI(
    title="Shuttle Tracker",
    description="API untuk melacak lokasi shuttle bus",
    version="0.0.1",
    docs_url="/",
)
# Use a service account.
firebaseConfig = {
  "apiKey": "AIzaSyBFXji0tc6nLJfv-NFcuKod-IHU-5jTZX8",
  "authDomain": "esp32-firebase-demo-f2551.firebaseapp.com",
  "databaseURL": "https://esp32-firebase-demo-f2551-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "esp32-firebase-demo-f2551",
  "storageBucket": "esp32-firebase-demo-f2551.appspot.com",
  "messagingSenderId": "578289339512",
  "appId": "1:578289339512:web:079eab3e0cca5dc31ff18d"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Atur origins yang diizinkan, misalnya ["http://localhost", "https://example.com"]
    allow_credentials=True,  # Izinkan penggunaan credentials (mis. cookies, auth headers) saat request
    allow_methods=["*"],  # Izinkan semua metode HTTP (GET, POST, dll.)
    allow_headers=["*"],  # Izinkan semua headers pada request
    expose_headers=["Content-Disposition"]  # Headers yang diizinkan pada response
)

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def makeException(status_code, detail):
    return HTTPException(status_code=status_code, detail=detail)


@app.post("/signup/")
async def create_an_account(user_data: SignUp):
    email = user_data.email
    password = user_data.password
    full_name = user_data.full_name
    

    try:
        user = auth.create_user_with_email_and_password(email, password)
        uid = user["localId"]
        data = {"full_name" : full_name, "email" : email}
        data_to_save = {"UsersData/" + uid : data}
        store_data = db.update(data_to_save, user["idToken"])
        if(store_data):
            return(JSONResponse(status_code=200, content={"message" : "User created successfully", "data" : user}))
    
    except Exception as e:
        print("Error: ", e)
        raise makeException(409, "User already exist")
        

@app.post("/login/")
async def create_access_token(user_data: Login ):
    email = user_data.email
    password = user_data.password
    invalid_exception = HTTPException(status_code=401, detail="Invalid username or password", headers={"WWW-Authenticate" : "Bearer"})

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        
        return {"access_token" : user["idToken"], "token_type" : "bearer"}
    
    except Exception as e:
        print("Error: ", e)
        raise invalid_exception


def get_current_user(authorization: str = Depends(oauth2_scheme)):
    try:
        user = auth.get_account_info(authorization)
        return user
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
          headers={"WWW-Authenticate": "Bearer"},
        )


# Example usage in an endpoint
@app.post("/track-shuttle/")
async def track_shuttle(latitude: float, longitude: float, user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    uid = user['users'][0]['localId']
    idToken = token
    shuttle_location_data = {"latitude": latitude, "longitude": longitude}
    db.child("ShuttleData").child(uid).set(shuttle_location_data, idToken)
    return JSONResponse(status_code=200, content={"message": "Lokasi shuttle berhasil dilacak"})

# track shuttle get
@app.get("/track-shuttle/")
async def get_shuttle_location(user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    uid = user['users'][0]['localId']
    idToken = token
    shuttle_location_data = db.child("ShuttleData").child(uid).get(idToken)
    return JSONResponse(status_code=200, content={"message": "Lokasi shuttle berhasil dilacak", "data": shuttle_location_data.val()})

#track shuttle get by id without login
@app.get("/track-shuttle/{uid}")
async def get_shuttle_location_by_id(uid: str):
    shuttle_location_data = db.child("ShuttleData").child(uid).get()
    return JSONResponse(status_code=200, content={"message": "Lokasi shuttle berhasil dilacak", "data": shuttle_location_data.val()})

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)