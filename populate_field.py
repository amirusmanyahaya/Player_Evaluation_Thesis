from re import S
import database
import os
from orm_model import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from tqdm import tqdm


# returns the
def extract_season(season, session, season_type="All"):
    # extracting the specific season
    result = None
    if season_type == "Regular Season":
        result = (
            session.query(PlayByPlayEvents)
            .join(Game, PlayByPlayEvents.GameId == Game.GameId)
            .filter(Game.Season == season, Game.SeasonType == "Regular Season")
            .all()
        )
    elif season_type == "Playoffs":
        result = (
            session.query(PlayByPlayEvents)
            .join(Game, PlayByPlayEvents.GameId == Game.GameId)
            .filter(Game.Season == season, Game.SeasonType == "Playoffs")
            .all()
        )
    else:
        result = (
            session.query(PlayByPlayEvents)
            .join(Game, PlayByPlayEvents.GameId == Game.GameId)
            .filter(Game.Season == season)
            .all()
        )
    session.commit()
    return result


def perform_join(obj1, id1, id2, session):
    orm = session.query(obj1).filter(id1 == id2).all()
    return orm


def create_tables(engine, obj):
    Base.metadata.tables["new_play_by_play"].create(bind=engine, checkfirst=True)
    print(f"created table {obj.__tablename__}")


def populate_play_by_play(orms, session):
    for orm in tqdm(orms):
        result = None
        event = None
        if orm.EventType == "PERIOD START":
            result = perform_join(
                EventPeriodStart,
                EventPeriodStart.PeriodStartId,
                orm.ExternalEventId,
                session,
            )
            event = "PERIOD START"
        elif orm.EventType == "FACEOFF":
            result = perform_join(
                EventFaceoff, EventFaceoff.FaceoffId, orm.ExternalEventId, session
            )
            event = f"faceoff({'Home' if result.FaceoffWinningTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "MISSED SHOT":
            result = perform_join(
                EventMissedShot, EventMissedShot.MissId, orm.ExternalEventId, session
            )
            event = f"missed_shot({'Home' if result.MissTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "SHOT":
            result = perform_join(
                EventShot, EventShot.ShotId, orm.ExternalEventId, session
            )
            event = f"shot({'Home' if result.ShotByTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "HIT":
            result = perform_join(
                EventHit, EventHit.HitId, orm.ExternalEventId, session
            )
            event = f"hit({'Home' if result.HittingTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "BLOCKED SHOT":
            result = perform_join(
                EventBlockedShot, EventBlockedShot.BlockId, orm.ExternalEventId, session
            )
            event = f"blocked_shot({'Home' if result.BlockTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "STOPPAGE":
            result = perform_join(
                EventStoppage, EventStoppage.StoppageId, orm.ExternalEventId, session
            )
            event = "STOPPAGE"
        elif orm.EventType == "GIVEAWAY":
            result = perform_join(
                EventGiveaway, EventGiveaway.GiveawayId, orm.ExternalEventId, session
            )
            event = f"giveaway({'Home' if result.GiveawayTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "PENALTY":
            result = perform_join(
                EventPenalty, EventPenalty.PenaltyId, orm.ExternalEventId, session
            )
            event = f"penalty({'Home' if result.TeamPenaltyId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "GOAL":
            result = perform_join(
                EventGoal, EventGoal.GoalId, orm.ExternalEventId, session
            )
            event = f"goal({'Home' if result.ScoringTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "TAKEAWAY":
            result = perform_join(
                EventTakeaway, EventTakeaway.TakeawayId, orm.ExternalEventId, session
            )
            event = f"takeaway({'Home' if result.TakeawayTeamId == result.HomeTeamId else 'Away' },{result.Zone})"
        elif orm.EventType == "PERIOD END":
            result = perform_join(
                EventPeriodEnd, EventPeriodEnd.PeriodEndId, orm.ExternalEventId, session
            )
            event = "PERIOD END"
        elif orm.EventType == "GAME END":
            result = perform_join(
                EventGameEnd, EventGameEnd.GameEndId, orm.ExternalEventId, session
            )
            event = "GAME END"
        elif orm.EventType == "SHOOTOUT COMPLETED":
            result = perform_join(
                EventShootoutCompleted,
                EventShootoutCompleted.ShootoutCompletedId,
                orm.ExternalEventId,
                session,
            )
            event = "SHOOTOUT COMPLETED"
        elif orm.EventType == "EARLY INTERMISSION START":
            result = perform_join(
                EventEarlyIntermissionStart,
                EventEarlyIntermissionStart.EarlyIntermissionStartId,
                orm.ExternalEventId,
                session,
            )
            event = "EARLY INTERMISSION START"
        elif orm.EventType == "EARLY INTERMISSION END":
            result = perform_join(
                EventEarlyIntermissionEnd,
                EventEarlyIntermissionEnd.EarlyIntermissionEndId,
                orm.ExternalEventId,
                session,
            )
            event = "EARLY INTERMISSION END"
        elif orm.EventType == "GAME OFF":
            result = perform_join(
                EventGameOff, EventGameOff.GameOffId, orm.ExternalEventId, session
            )
            event = "GAME OFF"
        elif orm.EventType == "GOALIE":
            result = perform_join(
                EventGoaliePulled,
                EventGoaliePulled.GoaliePulledId,
                orm.ExternalEventId,
                session,
            )
            event = "GOALIE PULLED"

        if event is not None:
            # add the result to the database
            session.add(
                NewPlayByPlay(
                    GameId=orm.GameId,
                    Period=orm.PeriodNumber,
                    Sequence=orm.ActionSequence,
                    EventNumber=orm.EventNumber,
                    EventTime=orm.EventTime,
                    Event=event,
                )
            )
            session.commit()


if __name__ == "__main__":
    engine = database.create_connection(
        user=os.environ["db_user"],
        password=os.environ["db_pass"],
        host=os.environ["db_host"],
        database=os.environ["db_name"],
    )
    season = "2010-2011"
    session = sessionmaker(bind=engine)()
    orms = extract_season(season=season, session=session, season_type="Regular Season")
    create_tables(engine, NewPlayByPlay)
    populate_play_by_play(orms, session)
    session.close()
