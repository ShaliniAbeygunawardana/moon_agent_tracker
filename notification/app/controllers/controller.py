from app.services.sqs_service import SQSService
from fastapi import APIRouter
import time

router = APIRouter()

# SQS queue URL
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'

# Initialize SQS service
sqs_service = SQSService(queue_url=QUEUE_URL)

@router.get("/poll-sqs", summary="Poll SQS messages")
async def poll_sqs():
    """Endpoint to start polling SQS messages."""
    try:
        for message in sqs_service.poll_messages():
            print(f"Received message: {message['Body']}")
            sqs_service.delete_message(message['ReceiptHandle'])
            print("Message deleted")
            time.sleep(1)
        return {"message": "Polling completed"}
    except Exception as e:
        return {"error": str(e)}