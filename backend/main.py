from fastapi import FastAPI
from idealo.views import router as idealo_router

app = FastAPI()

app.include_router(idealo_router, prefix="/idealo")


@app.get("/")
def hello_world():
    return {"hello": "world!"}
