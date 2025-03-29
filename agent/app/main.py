import sys
sys.path.append(r"C:/Users/Shalini Imantha/moon_agent_tracker/")
from fastapi import FastAPI
from agent.app.controllers.controller import router

app = FastAPI()
app.include_router(router)