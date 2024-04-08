from sqlalchemy.orm import Session
from db import engine
from models import Match,Team, Player


with Session(bind=engine) as session:
    t1 = Team(name = "ABC")
    t2 = Team(name = "XYZ")
    t3 = Team(name = "IJK")

    session.add_all([t1,t2,t3])
    session.commit()

    m1 = Match(venue = "Wankhede" , team1_id = t1.team_id , team2_id = t2.team_id)
    m2 = Match(venue = "Chinaswamy" , team1_id = t2.team_id , team2_id = t3.team_id)

    session.add_all([m1,m2])
    session.commit()

    p1 = Player(name = "Nishith")
    p2 = Player(name = "Suchit")
    p3 = Player(name = "Dhruv")

    p1.teams = [t1,t2]
    p2.teams = [t3]
    p3.teams = [t1,t3]

    session.add_all([p1,p2,p3])
    session.commit()

