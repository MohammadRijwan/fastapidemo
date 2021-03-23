from fastapi import FastAPI

app=FastAPI()


@app.get('/')
def root():
    return{'Status':'Welcome to the fast API'}