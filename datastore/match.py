from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, contains_eager, aliased
from .core import Base, CricketBase, scoped_session
from .team import Team
from .ball import Ball
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
            match = cls(time=datetime.strptime(user_input['time'], '%Y-%m-%d'),
                        ground=user_input['ground'],
                        num_overs=user_input['num_overs'],
                        team1_name=user_input['team1'],
                        team2_name=user_input['team2'],
                        toss_winner=user_input['toss_winner'],
                        first_inning=user_input['first_inning']
                    )
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
            match_dict = match.as_dict()

            latest_ball_res = Ball.get_latest_ball(session, match.id)
            latest_ball = latest_ball_res['latest_ball']
            bowler_id = latest_ball_res['bowler_id']
            total_runs = latest_ball_res['total_runs']
            runs = latest_ball_res['runs']
            is_wide = latest_ball_res['is_wide']
            is_no_ball = latest_ball_res['is_no_ball']

            # import pdb; pdb.set_trace()
            total_wides = Ball.get_total_wides(session, match.id)
            total_no_balls = Ball.get_total_no_balls(session, match.id)
            total_byes = Ball.get_total_byes(session, match.id)

            match_dict['current_bowler'] = bowler_id if latest_ball%6 < 6 else ''
            match_dict['over'] = get_over(latest_ball, is_wide, is_no_ball)
            match_dict['total_runs'] = total_runs + total_wides + total_no_balls + total_byes
            match_dict['wides'] = total_wides
            match_dict['no_balls'] = total_no_balls
            match_dict['byes'] = total_byes
            match_dict['last_ball'] = runs
            match_dict['next_ball'] = next_ball(latest_ball, is_wide, is_no_ball)
            match_dict['batting_score'] = get_batting_score(session, match)
            match_dict['bowling_score'] = get_bowling_score(session, match)
            return match_dict

    @classmethod
    def get_matches(cls, **kwargs):
        with scoped_session() as session:
            query = session.query(cls).filter_by(**kwargs)
            matches = query.all()
            matches_dict = []
            for match in matches:
                matches_dict.append(match.as_dict())
            return matches_dict

    def as_dict(self):
        match_dict = super(self.__class__, self).as_dict()
        match_dict['team1'] = self.team1.as_dict()
        match_dict['team2'] = self.team2.as_dict()
        return match_dict

def get_batting_score(session, match):
    batting_score = {}
    batting_team = match.team1 if match.first_inning == match.team1_name else match.team2
    for player in batting_team.players:
        player_runs, balls_played = Ball.get_batsman_stats(session, player.id, match.id)
        batting_score[player.id] = {'runs': player_runs, 'balls': balls_played}
    return batting_score

def get_bowling_score(session, match):
    bowling_score = {}
    bowling_team = match.team2 if match.first_inning == match.team1_name else match.team1
    for player in bowling_team.players:
        num_runs, num_balls, wides, no_balls = Ball.get_bowler_stats(session, player.id, match.id)
        overs = str(num_balls/6) +"."+ str(num_balls%6)
        bowling_score[player.id] = {'runs': num_runs, 'overs': overs, 'wides': wides, 'no_balls': no_balls}
    return bowling_score

def get_over(latest_ball, is_wide, is_no_ball):
    if is_wide or is_no_ball:
        ball_num = latest_ball - 1
    else:
        ball_num = latest_ball
    return str(ball_num/6) +"."+ str(ball_num%6)

def next_ball(latest_ball, is_wide, is_no_ball):
    if is_wide or is_no_ball:
        return latest_ball
    else:
        return latest_ball + 1

