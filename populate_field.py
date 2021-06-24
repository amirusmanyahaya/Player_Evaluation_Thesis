import database
import os
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = database.create_connection(user=os.environ["db_user"],
                                    password=os.environ["db_pass"],
                                    host=os.environ["db_host"],
                                    database=os.environ["db_name"])
session = sessionmaker(bind=engine)()
Base = declarative_base()


class Game(Base):
    __tablename__ = "game"
    GameId = Column(Integer, primary_key=True)
    Season = Column(Text)
    SeasonType = Column(Text)


class Player(Base):
    __tablename__ = "player"
    PlayerId = Column(Integer, primary_key=True)
    PlayerName = Column(Text)
    Position = Column(Text)
    BirthPlace = Column(Text)
    Country = Column(Text)
    Height = Column(Text)
    Weight = Column(Integer)
    Birthdate = Column(Text)
    BirthMonth = Column(Text)
    BirthYear = Column(Integer)
    Age = Column(Integer)
    DraftTeam = Column(Text)
    DraftYear = Column(Integer)
    DraftRound = Column(Integer)
    DraftNumber = Column(Integer)


class Team(Base):
    __tablename__ = "team"
    TeamId = Column(Integer, primary_key=True)
    TeamName = Column(Text)
    League = Column(Text)


class PlayByPlayEvents(Base):
    __tablename__ = "play_by_play_events"
    GameId = Column(Integer, ForeignKey(Game.GameId), primary_key=True)
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    ActionSequence = Column(Integer)
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventType = Column(Text)
    ExternalEventId = Column(Integer)
    AwayPlayer1 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer2 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer3 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer4 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer5 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer6 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer7 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer8 = Column(Integer, ForeignKey(Player.PlayerId))
    AwayPlayer9 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer1 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer2 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer3 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer4 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer5 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer6 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer7 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer8 = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayer9 = Column(Integer, ForeignKey(Player.PlayerId))


if __name__ == "__main__":
    # result = session.query(Game).filter(Game.Season == "2010-2011", Game.SeasonType != "Playoffs").all()
    # for row in result:
    #     print(f"{row.GameId}\t{row.Season}\t{row.SeasonType}")

    # result = session.query(Player).filter(Player.PlayerId == 8445176).all()
    # for row in result:
    #     print(f"{row.PlayerId}\t{row.PlayerName}")

    # result = session.query(Team).filter(Team.League == "NHL").all()
    # for row in result:
    #     print(f"{row.TeamId}\t{row.TeamName}")

    # result = session.query(PlayByPlayEvents).filter(PlayByPlayEvents.AwayPlayer1 == 8445176).all()
    # for row in result:
    #     print(f"{row.GameId}\t{row.EventTime}\t{row.EventType}")
    pass
