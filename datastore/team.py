from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, contains_eager
from .core import Base, scoped_session
from .player import Player

class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    players = relationship('Player', backref='team', cascade='all, delete-orphan')
    # matches = relationship('Match', backref='team', cascade='all, delete-orphan')

    @classmethod
    def create_team(cls, team_name, players=None):
        with scoped_session() as session:
            team = cls()
            team.name = team_name
            if not players:
                players = []
                for i in range(8):
                    players.append(Player(name='Player{}'.format(i)))
            team.players = players
            session.add(team)

    @classmethod
    def get_team(cls, **kwargs):
        with scoped_session() as session:
            query = session.query(cls).filter_by(**kwargs)\
                           .outerjoin(cls.players).options(contains_eager('players'))
            team = query.all()
            if team:
                team = team[0].as_dict()
            return team

    def as_dict(self):
        result = {}
        result['team_name'] = self.name
        result['players'] = [player.name for player in self.players]
        return result


