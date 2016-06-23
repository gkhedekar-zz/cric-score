from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .core import Base, scoped_session

class Ball(Base):
    __tablename__ = 'ball'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ball_num = Column(Integer)
    runs = Column(Integer)
    is_wide = Column(Integer)
    is_no_ball = Column(Integer)
    inning = Column(Integer)
    batsman_id = Column(Integer, ForeignKey('player.id'))
    bowler_id = Column(Integer, ForeignKey('player.id'))
    match_id = Column(Integer, ForeignKey('match.id'))

    @classmethod
    def create_ball(cls, match_id, user_input):
        with scoped_session() as session:
            ball = cls(match_id=match_id,
                       ball_num=int(user_input['ball_num']),
                       runs=int(user_input['runs']),
                       is_wide=int(user_input['is_wide']),
                       is_no_ball=int(user_input['is_no_ball']),
                       batsman_id=int(user_input['batsman_id']),
                       bowler_id=int(user_input['bowler_id'])
                    )
            session.add(ball)

    @classmethod
    def get_latest_ball(cls, session, match_id):
        query = session.query(func.max(cls.ball_num), cls.bowler_id, func.sum(cls.runs), cls.runs).filter_by(match_id=match_id)
        return query.one()

    @classmethod
    def get_player_stats(cls, session, player_id, match_id, type):
        if type == 'batting':
            query = session.query(func.sum(cls.runs), func.count(cls.ball_num)).filter_by(match_id=match_id, batsman_id=player_id)
        elif type == 'bowling':
            query = session.query(func.sum(cls.runs), func.count(cls.ball_num)).filter_by(match_id=match_id, bowler_id=player_id)
        return query.one()

