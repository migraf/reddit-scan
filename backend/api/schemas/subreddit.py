import datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

from .fields import PyObjectId


class SubscriberCount(BaseModel):
    timestamp: datetime.datetime
    subscribers: int


class Subreddit(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    display_name: str = Field(...)
    subscribers: int = Field(...)
    public_description: str = Field(...)
    icon_img: Optional[str] = Field(...)
    over18: bool = Field(...)
    subscriber_counts: Optional[List[SubscriberCount]] = Field(...)
    _path: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
