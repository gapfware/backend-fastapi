from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount('/statico', StaticFiles(directory='static'), name='statico')

@app.get('/', response_class=HTMLResponse)
async def root():
    return """<h1>Hola FastAPI</h1>"""