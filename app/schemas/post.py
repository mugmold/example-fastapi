from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator
from app.schemas.user import UserResponse


class PostBase(BaseModel):
    is_public: Optional[bool] = True


class PostCreate(PostBase):
    title: str
    content: str


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if not (self.title or self.content or self.is_public is not None):
            raise ValueError("At least one field must be updated")
        return self


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    total_votes: int
    is_public: bool
    created_at: datetime
    owner: UserResponse

    model_config = {
        "from_attributes": True
    }
