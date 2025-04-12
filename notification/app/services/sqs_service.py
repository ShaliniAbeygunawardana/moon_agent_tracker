import boto3
import time

class SQSService:
    def __init__(self, queue_url: str):
        self.sqs = boto3.client('sqs')
        self.queue_url = queue_url

    def poll_messages(self):
        while True:
            # Receive messages from SQS queue
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All'],
                WaitTimeSeconds=20  # Enable long polling
            )

            messages = response.get('Messages', [])
            for message in messages:
                yield message

    def delete_message(self, receipt_handle: str):
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )