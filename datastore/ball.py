from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .core import Base, scoped_session

class Ball(Base):
    __tablename__ = 'ball'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ball_num = Column(Integer)
    runs = Column(Integer)
    is_wide = Column(Integer)
    is_no_ball = Column(Integer)

    batsman_name = Column(Integer, ForeignKey('player.id'))
    bowler_name = Column(Integer, ForeignKey('player.id'))
    match_id = Column(Integer, ForeignKey('match.id'))

    @classmethod
    def create_ball(cls, match_id, user_input):
        with scoped_session() as session:
            ball = cls(match_id=match_id,
                       ball_num=int(user_input['ball_num']),
                       runs=int(user_input['runs']),
                       is_wide=int(user_input['is_wide']),
                       is_no_ball=int(user_input['is_no_ball']),
                       batsman_name=int(user_input['batsman_id']),
                       bowler_name=int(user_input['bowler_id'])
                    )
            session.add(ball)
