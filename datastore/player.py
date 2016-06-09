from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .core import Base, scoped_session

class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))

    @classmethod
    def update_player(cls, id, name):
        with scoped_session() as session:
            player = session.query(cls).filter_by(id=id).all()[0]
            player.name = name