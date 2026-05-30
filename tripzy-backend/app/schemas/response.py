from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None


def success_response(message: str, data: Any = None) -> dict:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str, data: Any = None) -> dict:
    return {
        "success": False,
        "message": message,
        "data": data,
    }