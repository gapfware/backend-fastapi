from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "gapfware": {
        "username": "gapfware",
        "full_name": "Gabriel Perez",
        "email": "gapfware@gmail.com",
        "disabled": False,
        "password": "$2y$10$ncXEOPUBX2qNmDDjp3vXDu1xjEgJ7PE/YVhHdzQQ82o47hcDy1HCi" #awd12345
    },
    "gabrielpf_08": {
        "username": "gabrielpf_08",
        "full_name": "Gabriel Perez",
        "email": "gabrielpf086@gmail.com",
        "disabled": True,
        "password": "$2y$10$K1h3uzfHTBcjwOIB.va3jOpR9W5VCOfxH5.N9r8cgBnY0UDcx9K62" #12345awd
    },
}

def search_user_db(username: str = Depends(oauth2)):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Credenciales de autenticacion Invalidas',
            headers={'WWW-Authenticate': "Bearer"}
            )
    
    try:
        username = jwt.decode(token, SECRET, ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception 
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Usuario Inactivo')
    return user

@router.post('/loginjwt')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='EL usuario no es correcto')
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail='Contraseña Incorrecta')
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    access_token = {"sub": user.username, "exp": expire}
    
    return {"acces_token": jwt.encode(access_token, SECRET ,algorithm=ALGORITHM), "token_type": "bearer"}

@router.get('/usersjwt/me')
async def me(user: User = Depends(current_user)):
    return user