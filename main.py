from fastapi import FastAPI

app=FastAPI()


@app.get('/')
def root():
    return{'Status':'Welcome to the fast API'}


@app.post('/')
def post():
    return{'Status':'Welcome to the fast API'}

@app.put('/')
def put():
    return{'Status':'Welcome to the fast API'}

@app.delete('/')
def delete():
    return{'Status':'Welcome to the fast API'}