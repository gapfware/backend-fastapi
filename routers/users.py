from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix = '/user',
    tags=['users'],
    responses= {404: {"message": "No Encontrado"}}
)

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str = ''
    age: int

users_fake_db = [
    User(id=1, name='Gabriel', surname='Perez', url='gapfware.com', age=19), 
    User(id=2, name='Omar', surname='Perez', age=16),
    User(id=3, name='Valeria', surname='Chimienti', url='latematica.com', age=20)
    ]

@router.get('s/')
async def users():
    return users_fake_db

# Path
@router.get('/{id}')
async def get_user(id: int):
    return search_user(id)

#Query
@router.get('/')
async def user(id: int):
    return search_user(id)


def search_user(id: int):
    try:
        user = list(filter(lambda user: user.id == id, users_fake_db))
        return user[0]
    except:
        return {'error': "No se ha encontrado usuario"}

@router.post('/', response_model = User, status_code=201)
async def user(user: User):
    if type(search_user(user.id))  == User:
        raise HTTPException(400, detail="El usuario ya existe")

    users_fake_db.append(user)
    return user

@router.put('/')
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == user.id:
            users_fake_db[index] = user
            found = True
            return user
            
    if not found:
        return {"error": "No se ha encontrado el usuario"}

@router.delete('/{id}')
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_fake_db):
        if saved_user.id == id:
            del users_fake_db[index]
            found = True

    if not found:
        return {"error": "No se ha eliminado el usuario"}