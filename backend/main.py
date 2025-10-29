import logging

from config import stdout_handler
from core.views import router as core_api
from fastapi import FastAPI
from integrations.adstrong.views import router as adstrong_router
from integrations.external_db.views import router as external_db_router
from integrations.idealo.views import router as idealo_router
from integrations.ikom.views import router as ikom_router

logging.basicConfig(level=logging.DEBUG, handlers=[stdout_handler])


app = FastAPI()

app.include_router(idealo_router, prefix="/idealo")
app.include_router(adstrong_router, prefix="/adstrong")
app.include_router(ikom_router, prefix="/ikom")
app.include_router(core_api, prefix="/api/v1")
app.include_router(external_db_router, prefix="/external_db")


@app.get("/")
def hello_world():
    return {"hello": "world!"}
