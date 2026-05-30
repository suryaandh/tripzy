from datetime import datetime

from sqlalchemy import String, Integer, DateTime, event, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )


@event.listens_for(User, "init")
def auto_create_profile(target, args, kwargs):
    from app.models.user_profiles import UserProfile
    target.profile = UserProfile()