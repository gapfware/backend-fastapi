from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def hello_world():
    return "Hola FastAPI!"

@app.get('/documentation')
async def url():
    return { 'url_doc': 'http://127.0.0.1:8000/docs' }