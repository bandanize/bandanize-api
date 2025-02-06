from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    email: Optional[str] = None
    image: Optional[str] = None
    hashed_password: Optional[str] = None
    disabled: Optional[bool] = False

    class Config:
        from_attributes = True

class Request(BaseModel, Generic[T]):
    parameter: T = Field(...)

class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)

class CreateUser(UserSchema):
    password: str

class Update(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    image: Optional[str] = None
    hashed_password: Optional[str] = None
    disabled: Optional[bool] = False

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

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(UserSchema):
    hashed_password: str