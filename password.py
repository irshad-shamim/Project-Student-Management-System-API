from fastapi import HTTPException, Header
from jose import jwt
from datetime import datetime, timedelta, timezone


SECRET_KEY = "mysecret"

ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    to_encode.update({
        "exp": expire
    })
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

'''@app.get("/login")
def login(username:str, password:str):
    if username != "irshad" or password != "pich":
        raise HTTPException(
            status_code= 404,
            detail= "wrong password and user name"
        )
    token = create_token({
        "sub": username
    })
    return {
        "token": token
    }'''

def verify_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code= 404,
            detail="wrong or expire token"
        )