from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class IngesionRequest(BaseModel):
    bucket_name: str
    file_path: str
    archive_path: Optional[str] = None
    
    
## models of the agent
class Agent(BaseModel):
    agent_id: str
    agent_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    branch_id: UUID

    
class AgentUpdate(BaseModel):
    agent_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    branch_id: UUID

    
class Product(BaseModel):
    product_id: str
    name: str
    description: str
    
class ProductUpdate(BaseModel):
    name: str
    description: str
