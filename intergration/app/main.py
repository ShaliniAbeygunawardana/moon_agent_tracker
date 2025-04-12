import sys
sys.path.append("/home/kosala/git-repos/moon_agent_tracker_test/")
from fastapi import FastAPI
from intergration.app.controllers.controller import router

app = FastAPI()
app.include_router(router)