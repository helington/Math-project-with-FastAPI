from fastapi import FastAPI

app = FastAPI()

app.get('/')
def hello_word():
    return {'message': 'hello world'}