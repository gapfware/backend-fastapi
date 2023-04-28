from fastapi import APIRouter

router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {"message": "No Encontrado"}}
    )

products = ["Product 1", "Product 2", "Product 3"]

@router.get('/')
async def products():
    return products

@router.get('/{id}')
async def product():
    return product[id]
