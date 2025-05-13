import motor.motor_asyncio
from dotenv import load_dotenv
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_core import core_schema
from typing import Any
from pathlib import Path
import os

# from bson import ObjectId


# Chemin absolu vers le fichier .env
env_path = Path(__file__).parent / ".env"  # __file__ = emplacement de main.py
load_dotenv(env_path)

# Vérification du chargement
MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    raise ValueError("La variable MONGODB_URL n'est pas définie dans .env")

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.blogapi

# BSON and fastapi JSON
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: core_schema.CoreSchema, _handler: Any) -> dict[str, Any]:
        return {"type": "string"}

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,  # Remplace allowed_population_by_field_name
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "David Dem",
                "email": "daoudadembele215@gmail.com",
                "password": "secret_code"
            }
        }
    )

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,  # Remplace allowed_population_by_field_name
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "David Dem",
                "email": "daoudadembele215@gmail.com"
            }
        }
    )


class BlogContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    body: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Blog Title",
                "body": "Blog Content"
            }
        }
    )

class BlogContentResponse(BlogContent):  # Hérite de BlogContent
    author_name: str = Field(...)  # Correction orthographique: "author" au lieu de "auther"
    author_id: str = Field(...)    # Idem
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "title": "Blog Title",
                "body": "Blog Content",
                "author_name": "Name of the author",
                "author_id": "ID of the author",
                "created_at": "2023-01-01T00:00:00Z"
            }
        }
    )

# class BlogContent(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     title: str = Field(...)
#     body: str = Field(...)

#     class Config:
#         populate_by_name=True,  # Remplace allowed_population_by_field_name
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str},
#         json_schema_extra={
#             "example": {
#                 "title": "Blog Title",
#                 "body": "Blog Content"
#             }
#         }


# class BlogContentResponse(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     title: str = Field(...)
#     body: str = Field(...)
#     auther_name: str = Field(...)
#     auther_id: str = Field(...)
#     created_at: str = Field(...)

#     class Config:
#         populate_by_name=True,  # Remplace allowed_population_by_field_name
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str},
#         json_schema_extra={
#             "example": {
#                 "title": "Blog Title",
#                 "body": "Blog Content",
#                 "auther_name": "Name of the auther",
#                 "auther_id": "ID of the auther",
#                 "created_at": "Date create"
#             }
#         }



class TokenData(BaseModel):
    id: str


class PasswordRest(BaseModel):
    email: EmailStr

class NewPassword(BaseModel):
    password: str