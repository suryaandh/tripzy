from fastapi import FastAPI

from app.core.exceptions import global_exception_handler

from app.api.auth import router as auth_router


app = FastAPI(
    title="Tripzy Backend API",
    version="1.0.0",
)

app.include_router(auth_router)

app.add_exception_handler(Exception, global_exception_handler)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Tripzy Backend API!"}