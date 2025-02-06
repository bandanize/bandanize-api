from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class BandSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        from_attributes = True

class Request(BaseModel, Generic[T]):
    parameter: T = Field(...)

class RequestBand(BaseModel):
    parameter: BandSchema = Field(...)

class Update(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

class RequestUpdate(BaseModel):
    parameter: Update = Field(...)

class Delete(BaseModel):
    id: int

class RequestDelete(BaseModel):
    parameter: Delete = Field(...)

class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T] = None