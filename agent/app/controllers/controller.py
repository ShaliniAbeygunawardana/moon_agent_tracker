from fastapi import APIRouter
from agent.app.models.dtos import Agent, AgentUpdate, Product, ProductUpdate
from fastapi import Body
from pydantic import BaseModel
from typing import Annotated
from agent.app.db_repository.sql_repoitory import SQLRepository, DatabaseOperationException \
    , DataNotFoundException
from agent.configs import DB_STRING
from fastapi import HTTPException, status

router = APIRouter()
db_repository = SQLRepository(database_url=DB_STRING)  # Example URL, replace with actual

class AgentResponse(BaseModel):
    message: str
    agent: Agent|AgentUpdate

class ProductResponse(BaseModel):
    message: str
    product: Product | ProductUpdate

class ErrorResponse(BaseModel):
    detail: str

@router.post(
    "/agent/",
    response_model=AgentResponse,
    responses={
        200: {"description": "Agent created successfully", "model": AgentResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Create a new agent",
    description="This endpoint allows you to create a new agent by providing \
        the required agent details.",
    tags=["Agent"]
)
async def create_agent(agent: Agent):
    """Controller function to create an agent.
    
    Args:
        agent (Agent): Agent information received from the 
        HTTP client as POST request payload.

    Returns:
        JSON response: Success or error message.
    """
    try:
        # Call the repository function to save the agent
        success = db_repository.save_agen_info(agent)
        if success:
            return {
                "message": "Agent created successfully",
                "agent": agent
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create agent due to an unknown error."
            )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.put(
    "/agent/{agent_id}",
    response_model=AgentResponse,
    responses={
        200: {"description": "User updated successfully", "model": AgentResponse},
        404: {"description": "User not found", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Update an existing user",
    description="This endpoint allows you to update an existing user's details by \
        providing the user ID and updated information.",
        tags=["Agent"]
)
async def update_user(agent_id: str, agent: AgentUpdate):
    """Controller function to update a agent's information.
    
    Args:
        user_id (int): The ID of the agent to be updated.
        user (Agent): Updated agent information received from the HTTP client as a 
        PATCH request payload.

    Returns:
        JSON response: Success or error message.
    """
    try:
        # Call the repository function to update the user
        success = db_repository.update_agent_info(agent_id, agent)
        if success:
            return {
                "message": "Agent updated successfully",
                "agent": agent
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found."
            )
    except DataNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.delete(
    "/agent/{agent_id}",
    responses={
        200: {"description": "Agent deleted successfully", "model": AgentResponse},
        404: {"description": "Agent not found", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Delete an agent",
    description="This endpoint allows you to delete an agent by providing the agent ID.",
    tags=["Agent"]
)
async def delete_agent(agent_id: str):
    """Controller function to delete an agent.
    
    Args:
        agent_id (str): The ID of the agent to be deleted.

    Returns:
        JSON response: Success or error message.
    """
    try:
        # Call the repository function to delete the agent
        success = db_repository.delete_agent(agent_id)
        if success:
            return {
                "message": "Agent deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found."
            )
    except DataNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
        
        

@router.post(
    "/product/",
    response_model=ProductResponse,
    responses={
        200: {"description": "Product created successfully", "model": ProductResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Create a new product",
    description="This endpoint allows you to create a new product by providing \
        the required product details.",
    tags=["Product"]
)
async def create_product(product: Product):
    try:
        success = db_repository.save_product_info(product)
        if success:
            return {
                "message": "Product created successfully",
                "product": product
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create product due to an unknown error."
            )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.put(
    "/product/{product_id}",
    response_model=ProductResponse,
    responses={
        200: {"description": "Product updated successfully", "model": ProductResponse},
        404: {"description": "Product not found", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Update an existing product",
    description="This endpoint allows you to update an existing product's details by \
        providing the product ID and updated information.",
    tags=["Product"]
)
async def update_product(product_id: str, product: ProductUpdate):
    try:
        success = db_repository.update_product_info(product_id, product)
        if success:
            return {
                "message": "Product updated successfully",
                "product": product
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found."
            )
    except DataNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.delete(
    "/product/{product_id}",
    responses={
        200: {"description": "Product deleted successfully", "model": ProductResponse},
        404: {"description": "Product not found", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Delete a product",
    description="This endpoint allows you to delete a product by providing the product ID.",
    tags=["Product"]
)
async def delete_product(product_id: str):
    try:
        success = db_repository.delete_product(product_id)
        if success:
            return {
                "message": "Product deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found."
            )
    except DataNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseOperationException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )