import database
import os
from orm_model import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm


# returns the
def extract_season(engine, season, season_type="All", session=sessionmaker):
    # extracting the specific season
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

    return result


def perform_join(obj1, obj2, id1, id2, session):
    orm = session.query(
        obj1,
    )


if __name__ == "__main__":
    engine = database.create_connection(
        user=os.environ["db_user"],
        password=os.environ["db_pass"],
        host=os.environ["db_host"],
        database=os.environ["db_name"],
    )
    season = "2010-2011"
    a = extract_season(engine, season=season, season_type="Regular Season")
    print(a)
