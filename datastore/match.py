from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .core import Base

class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ground = Column(String, nullable=False)
    time = Column(DateTime)
    num_overs = Column(Integer, nullable=False)
    toss_winner = Column(String, nullable=False)
    first_inning = Column(String, nullable=False)
    ground = Column(String, nullable=False)
    winner = Column(String, nullable=False)
    team1_id = Column(Integer, ForeignKey('team.id'))
    team2_id = Column(Integer, ForeignKey('team.id'))

    team1 = relationship('Team', foreign_keys=[team1_id])
    team2 = relationship('Team', foreign_keys=[team2_id])