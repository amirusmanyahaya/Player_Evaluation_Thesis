import database
import os
from orm_model import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from tqdm import tqdm
from node import Node


# returns the
def extract_season(season, session, season_type="All"):
    # extracting the specific season
    result = None
    if season_type == "Regular Season":
        result = (
            session.query(
                PlayByPlayEvents.GameId,
                PlayByPlayEvents.PeriodNumber,
                PlayByPlayEvents.ActionSequence,
                PlayByPlayEvents.ExternalEventId,
                PlayByPlayEvents.EventNumber,
                PlayByPlayEvents.EventTime,
                PlayByPlayEvents.EventType,
            )
            .join(Game)
            .filter(Game.Season == season, Game.SeasonType == "Regular Season")
            .all()
        )
    elif season_type == "Playoffs":
        result = (
            session.query(
                PlayByPlayEvents.GameId,
                PlayByPlayEvents.PeriodNumber,
                PlayByPlayEvents.ActionSequence,
                PlayByPlayEvents.ExternalEventId,
                PlayByPlayEvents.EventNumber,
                PlayByPlayEvents.EventTime,
                PlayByPlayEvents.EventType,
            )
            .join(Game)
            .filter(Game.Season == season, Game.SeasonType == "Playoffs")
            .all()
        )
    else:
        result = (
            session.query(
                PlayByPlayEvents.GameId,
                PlayByPlayEvents.PeriodNumber,
                PlayByPlayEvents.ActionSequence,
                PlayByPlayEvents.ExternalEventId,
                PlayByPlayEvents.EventNumber,
                PlayByPlayEvents.EventTime,
                PlayByPlayEvents.EventType,
            )
            .join(Game)
            .filter(Game.Season == season)
            .all()
        )
    # session.commit()
    return result


def perform_join(obj1, id1, id2, session):
    orm = session.query(obj1).filter(id1 == id2).all()
    return orm


def create_tables(engine, obj, session):
    session.commit()
    Base.metadata.tables["new_play_by_play"].drop(bind=engine, checkfirst=True)
    print(f"dropped table {obj.__tablename__}")
    session.commit()
    Base.metadata.tables["new_play_by_play"].create(bind=engine, checkfirst=True)
    print(f"created table {obj.__tablename__}")
    session.commit()


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
            event = f"faceoff({'Home' if result[0].FaceoffWinningTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "MISSED SHOT":
            result = perform_join(
                EventMissedShot, EventMissedShot.MissId, orm.ExternalEventId, session
            )
            event = f"missed_shot({'Home' if result[0].MissTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "SHOT":
            result = perform_join(
                EventShot, EventShot.ShotId, orm.ExternalEventId, session
            )
            event = f"shot({'Home' if result[0].ShotbyTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "HIT":
            result = perform_join(
                EventHit, EventHit.HitId, orm.ExternalEventId, session
            )
            event = f"hit({'Home' if result[0].HittingTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "BLOCKED SHOT":
            result = perform_join(
                EventBlockedShot, EventBlockedShot.BlockId, orm.ExternalEventId, session
            )
            event = f"blocked_shot({'Home' if result[0].BlockTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "STOPPAGE":
            result = perform_join(
                EventStoppage, EventStoppage.StoppageId, orm.ExternalEventId, session
            )
            event = "STOPPAGE"
        elif orm.EventType == "GIVEAWAY":
            result = perform_join(
                EventGiveaway, EventGiveaway.GiveawayId, orm.ExternalEventId, session
            )
            event = f"giveaway({'Home' if result[0].GiveawayTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "PENALTY":
            result = perform_join(
                EventPenalty, EventPenalty.PenaltyId, orm.ExternalEventId, session
            )
            event = f"penalty({'Home' if result[0].TeamPenaltyId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "GOAL":
            result = perform_join(
                EventGoal, EventGoal.GoalId, orm.ExternalEventId, session
            )
            event = f"goal({'Home' if result[0].ScoringTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
        elif orm.EventType == "TAKEAWAY":
            result = perform_join(
                EventTakeaway, EventTakeaway.TakeawayId, orm.ExternalEventId, session
            )
            event = f"takeaway({'Home' if result[0].TakeawayTeamId == result[0].HomeTeamId else 'Away' },{result[0].Zone})"
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


def build_tree(session, results, time_array):
    # initialize a root node
    root = Node()
    root.set_type("Root Node")
    root.set_node_id(0)
    root.set_goal_away(None)
    root.set_goal_home(None)
    root.set_goal_diff(None)
    root.set_no_away_players(None)
    root.set_no_home_players(None)
    root.set_man_diff(None)
    root.set_zone(None)
    root.set_period(None)
    root.set_time_elapsed(None)
    root.set_count(1)

    current_node = root

    # for every row in the play_by_play_event
    #     get the type of event
    #     if event is a start marker
    #         create a context state
    #     else
    #         if the event is a normal event
    #             add the event to it's parent node
    #         if the event is an end event
    #             if the event is a goal
    #                 add a shot event before the goal to the parent node

    #             add the end event to the current node


if __name__ == "__main__":
    engine = database.create_connection(
        user=os.environ["db_user"],
        password=os.environ["db_pass"],
        host=os.environ["db_host"],
        database=os.environ["db_name"],
    )
    season = "2012-2013"
    session = sessionmaker(bind=engine)()
    orms = extract_season(season=season, session=session, season_type="Regular Season")
    # create_tables(engine, NewPlayByPlay, session)
    # populate_play_by_play(orms, session)
    time_array = []
    build_tree(session, orms, time_array)
