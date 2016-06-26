from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .core import Base, scoped_session

class Ball(Base):
    __tablename__ = 'ball'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ball_num = Column(Integer, nullable=False)
    runs = Column(Integer, default=0)
    byes = Column(Integer, default=0)
    is_wide = Column(Integer, default=0)
    is_no_ball = Column(Integer, default=0)
    inning = Column(Integer)
    batsman_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    bowler_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    match_id = Column(Integer, ForeignKey('match.id'), nullable=False)

    @classmethod
    def create_ball(cls, match_id, user_input):
        with scoped_session() as session:
            ball = cls(match_id=match_id,
                       ball_num=int(user_input['ball_num']),
                       runs=int(user_input['runs']),
                       is_wide=int(user_input['is_wide']),
                       is_no_ball=int(user_input['is_no_ball']),
                       byes=int(user_input['byes']),
                       batsman_id=int(user_input['batsman_id']),
                       bowler_id=int(user_input['bowler_id'])
                    )
            session.add(ball)

    @classmethod
    def get_latest_ball(cls, session, match_id):
        query = session.query(func.max(cls.ball_num),
                              cls.bowler_id, func.sum(cls.runs),
                              cls.runs, cls.is_wide, cls.is_no_ball).filter_by(match_id=match_id)
        latest_ball, bowler_id, total_runs, runs, is_wide, is_no_ball = query.one()
        return {
            'latest_ball': latest_ball if latest_ball else 0,
            'bowler_id': bowler_id,
            'total_runs': total_runs if total_runs else 0,
            'runs': runs if runs else 0,
            'is_wide': is_wide,
            'is_no_ball': is_no_ball
        }

    @classmethod
    def get_total_wides(cls, session, match_id):
        query = session.query(cls).filter_by(match_id=match_id, is_wide=1)
        wides = query.count()
        return wides if wides else 0

    @classmethod
    def get_total_no_balls(cls, session, match_id):
        query = session.query(cls).filter_by(match_id=match_id, is_no_ball=1)
        no_balls = query.count()
        return no_balls if no_balls else 0

    @classmethod
    def get_total_byes(cls, session, match_id):
        query = session.query(func.sum(cls.byes)).filter_by(match_id=match_id)
        byes = query.one()[0]
        return byes if byes else 0

    @classmethod
    def get_batsman_stats(cls, session, player_id, match_id):
        query = session.query(func.sum(cls.runs), func.count(cls.ball_num)).filter_by(match_id=match_id,
                                                                                      batsman_id=player_id,
                                                                                      is_wide=0, is_no_ball=0)
        return query.one()

    @classmethod
    def get_bowler_stats(cls, session, player_id, match_id):
        query1 = session.query(func.sum(cls.runs), func.count(cls.ball_num)).filter_by(match_id=match_id,
                                                                                      bowler_id=player_id,
                                                                                      is_wide=0, is_no_ball=0)
        runs, num_balls = query1.one()
        wides = session.query(func.count(cls.ball_num)).filter_by(match_id=match_id, bowler_id=player_id, is_wide=1).one()[0]
        no_balls = session.query(func.count(cls.ball_num)).filter_by(match_id=match_id, bowler_id=player_id, is_no_ball=1).one()[0]
        return runs, num_balls, wides, no_balls

