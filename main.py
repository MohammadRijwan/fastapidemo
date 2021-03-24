import databases, sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import model as modelUser
import uuid, datetime
from passlib.context import CryptContext    



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL="postgres://vjqsvelklqcndy:5e25599fc16cd8b098648874ad1cda31ffc754f45941461d42df4c4da5eccf4e@ec2-3-222-127-167.compute-1.amazonaws.com:5432/d17fc1gciajvb"
databases = databases.Database(DATABASE_URL)
metadata= sqlalchemy.MetaData()



users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id"        , sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username"  , sqlalchemy.String),
    sqlalchemy.Column("password"  , sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name" , sqlalchemy.String),
    sqlalchemy.Column("gender"    , sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at" , sqlalchemy.String),
    sqlalchemy.Column("status"    , sqlalchemy.CHAR  ),
)



engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)

#Model
  
app=FastAPI()

@app.on_event("startup")
async def startup():
    print('Connection Succefull...!!')
    await databases.connect()

@app.on_event("shutdown")
async def shutdown():
    await databases.disconnect()

@app.get("/users", response_model=List[modelUser.UserList], tags=["Users"])
async def find_all_users():
    query = users.select()
    return await databases.fetch_all(query)


@app.post("/users", response_model=modelUser.UserList, tags=["Users"])
async def register_user(user: modelUser.UserEntry):
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username   = user.username,
        password   = pwd_context.hash(user.password),
        first_name = user.first_name,
        last_name  = user.last_name,
        gender     = user.gender,
        create_at  = gDate,
        status     = "1"
    ) 

    await databases.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at":gDate,
        "status": "1"
    }