from fastapi import FastAPI
from app.controllers.controller import router

app = FastAPI(
    title="Notification Service",
    description="API documentation for the Notification service",
    version="1.0.0",
    docs_url="/notification/docs",  # Custom path for Swagger UI
    redoc_url="/notification/redoc"  # Custom path for ReDoc
)

# Include the router
app.include_router(router, prefix="/notification", tags=["Notification"])