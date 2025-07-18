from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer
from app.models.base import Base


class Vote(Base):
    __tablename__ = "votes"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
