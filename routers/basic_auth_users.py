from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

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
        "password": "awd12345"
    },
    "gabrielpf_08": {
        "username": "gabrielpf_08",
        "full_name": "Gabriel Perez",
        "email": "gabrielpf086@gmail.com",
        "disabled": True,
        "password": "12345awd"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Credenciales de autenticacion Invalidas',
            headers={'WWW-Authenticate': "Bearer"}
            )
        
    if user.disabled:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Usuario Inactivo')
    return user


@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='EL usuario no es correcto')
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail='Contraseña Incorrecta')
    return {"acces_token": user.username, "token_type": "bearer"}
    
@app.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user