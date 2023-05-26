from fastapi import FastAPI
from router import menu, authentication
from database import engine
import models
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(menu.router)
