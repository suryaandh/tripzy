from sqlalchemy.orm import Session
from app.models.user_profiles import UserProfile

def create_profile(db: Session, user_id: int):
    profile = UserProfile(
        user_id=user_id,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile