from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .core import Base

class Ball(Base):
    __tablename__ = 'ball'

    id = Column(Integer, primary_key=True, autoincrement=True)
    batsman_name = Column(String, nullable=False)
    ball_num = Column(Integer)
    runs = Column(Integer)
    is_wide = Column(Integer)
    is_no_ball = Column(Integer)

    over_id = Column(Integer, ForeignKey('over.id'))