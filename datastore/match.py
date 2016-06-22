from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, contains_eager, aliased
from .core import Base, CricketBase, scoped_session
from .team import Team
from datetime import datetime

class Match(Base, CricketBase):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ground = Column(String, nullable=False)
    time = Column(DateTime)
    num_overs = Column(Integer, nullable=False)
    toss_winner = Column(String, nullable=False)
    first_inning = Column(String, nullable=False)
    winner_name = Column(Integer, ForeignKey('team.name'))
    team1_name = Column(Integer, ForeignKey('team.name'))
    team2_name = Column(Integer, ForeignKey('team.name'))

    team1 = relationship('Team', foreign_keys=[team1_name])
    team2 = relationship('Team', foreign_keys=[team2_name])
    winner = relationship('Team', foreign_keys=[winner_name])

    @classmethod
    def create_match(cls, user_input):
        with scoped_session() as session:
            match = cls()
            match.time = datetime.strptime(user_input['time'], '%Y-%m-%d')
            match.ground = user_input['ground']
            match.num_overs = user_input['num_overs']
            match.team1_name = user_input['team1']
            match.team2_name = user_input['team2']
            match.toss_winner = user_input['toss_winner']
            match.first_inning = user_input['first_inning']
            session.add(match)
            session.flush()
            return match.id

    @classmethod
    def get_match(cls, **kwargs):
        with scoped_session() as session:
            team1 = aliased(Team)
            team2 = aliased(Team)
            query = session.query(cls).filter_by(**kwargs)\
                           .outerjoin(team1, cls.team1_name == team1.name)\
                           .outerjoin(team2, cls.team1_name == team2.name)
            match = query.all()[0]
            return match.as_dict()

    def as_dict(self):
        match_dict = super(self.__class__, self).as_dict()
        match_dict['team1'] = self.team1.as_dict()
        match_dict['team2'] = self.team2.as_dict()
        return match_dict
