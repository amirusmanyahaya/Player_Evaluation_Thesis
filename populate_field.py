import database
import os
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy import text
from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

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


class ExtractedPlayByPlay(Base):
    __tablename__ = "extracted_play_by_play"
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


# returns the
def extract_season(engine, season, season_type="All", session=sessionmaker):
    # adding the season to a new table new season
    text_query = text("DROP TABLE IF EXISTS extracted_play_by_play;")
    connection = engine.connect()
    connection.execute(text_query)
    print("I dropped extracted_play_by_play")
    Base.metadata.create_all(engine)

    # extracting the specific season
    print("I created the table extracted_play_by_play")
    result = None
    session1 = session(bind=engine)()
    if season_type == "Regular Season":
        result = (
            session1.query(PlayByPlayEvents)
            .join(Game, PlayByPlayEvents.GameId == Game.GameId)
            .filter(Game.Season == season, Game.SeasonType == "Regular Season")
            .all()
        )
    elif season_type == "Playoffs":
        result = (
            session1.query(PlayByPlayEvents)
            .join(Game, PlayByPlayEvents.GameId == Game.GameId)
            .filter(Game.Season == season, Game.SeasonType == "Playoffs")
            .all()
        )
    else:
        result = (
            session1.query(PlayByPlayEvents)
            .join(Game, PlayByPlayEvents.GameId == Game.GameId)
            .filter(Game.Season == season)
            .all()
        )

    # populates ExtractedEventPlayByPlay table
    for row in tqdm(result):
        session1.add(
            ExtractedPlayByPlay(
                GameId=row.GameId,
                AwayTeamId=row.AwayTeamId,
                HomeTeamId=row.HomeTeamId,
                ActionSequence=row.ActionSequence,
                EventNumber=row.EventNumber,
                PeriodNumber=row.PeriodNumber,
                EventTime=row.EventTime,
                ExternalEventId=row.ExternalEventId,
                AwayPlayer1=row.AwayPlayer1,
                AwayPlayer2=row.AwayPlayer2,
                AwayPlayer3=row.AwayPlayer3,
                AwayPlayer4=row.AwayPlayer4,
                AwayPlayer5=row.AwayPlayer5,
                AwayPlayer6=row.AwayPlayer6,
                AwayPlayer7=row.AwayPlayer7,
                AwayPlayer8=row.AwayPlayer8,
                AwayPlayer9=row.AwayPlayer9,
                HomePlayer1=row.HomePlayer1,
                HomePlayer2=row.HomePlayer2,
                HomePlayer3=row.HomePlayer3,
                HomePlayer4=row.HomePlayer4,
                HomePlayer5=row.HomePlayer5,
                HomePlayer6=row.HomePlayer6,
                HomePlayer7=row.HomePlayer7,
                HomePlayer8=row.HomePlayer8,
                HomePlayer9=row.HomePlayer9,
            )
        )
    session1.commit()


if __name__ == "__main__":
    engine = database.create_connection(
        user=os.environ["db_user"],
        password=os.environ["db_pass"],
        host=os.environ["db_host"],
        database=os.environ["db_name"],
    )
    season = "2010-2011"
    extract_season(engine, season=season, season_type="Regular Season")
