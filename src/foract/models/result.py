from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Result[T](BaseModel):
    success: bool
    data: T | None = None
    message: str = ""
