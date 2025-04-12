import sys
sys.path.append('/home/kosala/git-repos/moon_agent_tracker_test/')
from fastapi import APIRouter
from intergration.app.models.dtos import IngesionRequest
from fastapi import Body
from pydantic import BaseModel
from typing import Annotated
from intergration.app.db_repository.sql_repository import SQLRepository, DatabaseOperationException \
    , DataNotFoundException
from intergration.app.services.service import IntergrationService
from intergration.app.s3_repository.s3_service import S3Service, S3ServiceException
from intergration.configs import DB_STRING
from fastapi import HTTPException, status

router = APIRouter()
db_repository = SQLRepository(database_url=DB_STRING)
s3_repository = S3Service()
# injecting the db and s3 repository into the service
intergration_service = IntergrationService(
    db_adapter=db_repository,
    s3_adapter=s3_repository
)
    
class IngetionResponse(BaseModel):
    message: str
    ingestion: str

class ErrorResponse(BaseModel):
    detail: str

@router.post(
    "/intergration/trigger_ingesion",
    response_model=IngetionResponse,
    responses={
        201: {"description": "ingesion process triggered successfully", "model": IngetionResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Ingestion process trigger",
    description="This endpoint allows you to trigger the ingestion process by \
        providing the required details.",
    tags=["Ingesion"]
)
async def ingest_data(ingest_request: IngesionRequest):
    """Controller function to create an agent.
    
    Args:
        agent (Agent): Agent information received from the 
        HTTP client as POST request payload.

    Returns:
        JSON response: Success or error message.
    """
    try:
        # Call the repository function to save the agent
        success = intergration_service.fetch_data(ingest_request.model_dump())
        if success:
            return {
                "message": "Sales data ingested successfully.",
                "ingestion": "success"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to trigger sales ingestion process."
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

