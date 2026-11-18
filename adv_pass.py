from fastapi import HTTPException, Depends
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "mysecret"

ALGORITHM = "HS256"

ACESS_TOKEN_EXPIRE = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl = "login")

fake_db = {
    "admin":{
        "username": "admin",
        "hashed_password": pwd_context.hash("pich")
    }
}

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hased_password):
    return pwd_context.verify(plain_password, hased_password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    to_encode.update({
        "exp": expire
    })
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

'''@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code= 401,
            detail= "user name or password is worng"
        )

    acces_token = create_token({"sub":form_data.username})

    return{
        "acess token": acces_token,
        "token type": "bearer"
    }
'''

def verify_token(token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code= 401,
                detail="wrong or expire token"
            )
        return username
    except jwt.JWTError:
        raise HTTPException(
            status_code= 401,
            detail="wrong or expire token"
        )