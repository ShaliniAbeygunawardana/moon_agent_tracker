import sys
sys.path.append("/app/")
from fastapi import FastAPI
from agent.app.controllers.controller import router

app = FastAPI()
app.include_router(router)