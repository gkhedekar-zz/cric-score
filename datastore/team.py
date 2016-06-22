from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, contains_eager
from .core import Base, CricketBase, scoped_session
from .player import Player

class Team(Base, CricketBase):
    __tablename__ = 'team'

    name = Column(String, primary_key=True)
    players = relationship('Player', backref='team', cascade='all, delete-orphan')

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
    def get_teams(cls, *args, **kwargs):
        with scoped_session() as session:
            teams_dict = []
            query = session.query(cls).filter_by(**kwargs)\
                           .outerjoin(cls.players).options(contains_eager('players'))
            teams = query.all()
            for team in teams:
                teams_dict.append(team.as_dict())
            return teams_dict

    @classmethod
    def get_team(cls, *args, **kwargs):
        with scoped_session() as session:
            return cls.get_teams(cls, **kwargs)[0]

    def as_dict(self):
        team_dict = super(self.__class__, self).as_dict()
        team_dict['players'] = [player.as_dict() for player in self.players]
        return team_dict

