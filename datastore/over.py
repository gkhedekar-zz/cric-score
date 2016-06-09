from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .core import Base

class Over(Base):
    __tablename__ = 'over'

    id = Column(Integer, primary_key=True, autoincrement=True)
    inning = Column(Integer, nullable=False)
    bowler_name = Column(String, nullable=False)
    over_num = Column(Integer, nullable=False)
    runs = Column(Integer)
    wides = Column(Integer)
    no_balls = Column(Integer)

    balls = relationship('Ball', backref='over', cascade='all, delete-orphan')
    match_id = Column(Integer, ForeignKey('match.id'))