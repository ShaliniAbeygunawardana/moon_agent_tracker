from fastapi import APIRouter
from agent.app.models.dtos import Agent
from fastapi import Body
from typing import Annotated

router = APIRouter()

@router.post("/agent/")
async def create_agent(agent: Agent):
    # Replace with actual logic
    print(agent.email)
    return {"message": "Agent created", "agent": agent}

@router.get("/agent/{user_id}")
async def get_user(user_id: int):
    # Replace with actual logic
    return {"message": "User fetched", "user_id": user_id}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # Replace with actual logic
    return {"message": "User deleted", "user_id": user_id}