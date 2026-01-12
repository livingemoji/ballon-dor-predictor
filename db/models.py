from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    position = Column(String, nullable=True)
    club = Column(String, nullable=True)

    ratings = relationship("MatchRating", back_populates="player")
    sentiments = relationship("Sentiment", back_populates="player")
    weekly_scores = relationship("WeeklyScore", back_populates="player")
