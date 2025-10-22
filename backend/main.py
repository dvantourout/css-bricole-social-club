import logging

from adstrong.views import router as adstrong_router
from config import stdout_handler
from fastapi import FastAPI
from idealo.views import router as idealo_router

logging.basicConfig(level=logging.DEBUG, handlers=[stdout_handler])


app = FastAPI()

app.include_router(idealo_router, prefix="/idealo")
app.include_router(adstrong_router, prefix="/adstrong")


@app.get("/")
def hello_world():
    return {"hello": "world!"}
