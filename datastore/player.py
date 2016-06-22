from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .core import Base, CricketBase, scoped_session

class Player(Base, CricketBase):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    team_name = Column(Integer, ForeignKey('team.name'))

    @classmethod
    def update_players(cls, players=[]):
        with scoped_session() as session:
            session.add_all(players)

    @classmethod
    def get_player(cls, **kwargs):
        with scoped_session() as session:
            query = session.query(cls).filter_by(**kwargs)
            player = query.all()[0]
            return player