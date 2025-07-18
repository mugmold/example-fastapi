from pydantic import BaseModel


class VoteCreate(BaseModel):
    post_id: int


class VoteResponse(BaseModel):
    message: str
    post_id: int
    total_votes: int

    model_config = {
        "from_attributes": True
    }
