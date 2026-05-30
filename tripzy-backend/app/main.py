from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

import app.models  # noqa: F401 — ensures all models are registered with SQLAlchemy mapper

from app.core.exceptions import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

from app.api.auth import router as auth_router


app = FastAPI(
    title="Tripzy Backend API",
    version="1.0.0",
)

app.include_router(auth_router, prefix="/api/v1")

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Tripzy Backend API!"}