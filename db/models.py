from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
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


class MatchRating(Base):
    __tablename__ = "match_ratings"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    source = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    minutes_played = Column(Integer, nullable=True)

    match_date = Column(Date, nullable=False)
    competition = Column(String, nullable=True)

    player = relationship("Player", back_populates="ratings")


class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    text = Column(String, nullable=False)
    source = Column(String, nullable=False)
    week = Column(Integer, nullable=False)

    vader_score = Column(Float, nullable=False)
    llm_score = Column(Float, nullable=True)

    player = relationship("Player", back_populates="sentiments")


class WeeklyScore(Base):
    __tablename__ = "weekly_scores"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    week = Column(Integer, nullable=False)

    performance_score = Column(Float, nullable=False)
    sentiment_score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=False)

    player = relationship("Player", back_populates="weekly_scores")
