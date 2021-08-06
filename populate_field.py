import database
import os
from orm_model import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from tqdm import tqdm
from node import Node


# returns a list of play by play objects for a game
def extract_game(season, session, game_id, season_type="All"):
    # extracting the specific season
    result = None
    if season_type == "Regular Season":
        result = (
            session.query(
                PlayByPlayEvents
                # PlayByPlayEvents.GameId,
                # PlayByPlayEvents.PeriodNumber,
                # PlayByPlayEvents.ActionSequence,
                # PlayByPlayEvents.ExternalEventId,
                # PlayByPlayEvents.EventNumber,
                # PlayByPlayEvents.EventTime,
                # PlayByPlayEvents.EventType,
            )
            .join(Game)
            .filter(
                Game.Season == season,
                Game.SeasonType == "Regular Season",
                Game.GameId == game_id,
            )
            .all()
        )
    elif season_type == "Playoffs":
        result = (
            session.query(
                PlayByPlayEvents
                # PlayByPlayEvents.GameId,
                # PlayByPlayEvents.PeriodNumber,
                # PlayByPlayEvents.ActionSequence,
                # PlayByPlayEvents.ExternalEventId,
                # PlayByPlayEvents.EventNumber,
                # PlayByPlayEvents.EventTime,
                # PlayByPlayEvents.EventType,
            )
            .join(Game)
            .filter(
                Game.Season == season,
                Game.SeasonType == "Playoffs",
                Game.GameId == game_id,
            )
            .all()
        )
    else:
        result = (
            session.query(
                PlayByPlayEvents
                # PlayByPlayEvents.GameId,
                # PlayByPlayEvents.PeriodNumber,
                # PlayByPlayEvents.ActionSequence,
                # PlayByPlayEvents.ExternalEventId,
                # PlayByPlayEvents.EventNumber,
                # PlayByPlayEvents.EventTime,
                # PlayByPlayEvents.EventType,
            )
            .join(Game)
            .filter(Game.Season == season, Game.GameId == game_id)
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


def get_game_ids(session, season, season_type):
    results = (
        session.query(Game.GameId)
        .filter(Game.Season == season, Game.SeasonType == season_type)
        .all()
    )
    return results


def is_leaf_node(event):
    end_markers = ["GAME END","STOPPAGE","PENALTY","GOAL","PERIOD END"]
    if event in end_markers:
        return True
    else:
        return False

def is_home_team(event):
    return event[0].ScoringTeamId == event[0].HomeTeamId


def generate_node(orm, session):
    node = Node()


def build_tree(session, season, season_type, time_array):
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

    # get game_ids
    games = get_game_ids(session, season, season_type)


    for game_id in games:
        current_node = root

        # for every event in the game
        # expanding my current_node
        for event in extract_game(season,session,game_id,season_type):
            if is_leaf_node(event.EventType):
                new_node = Node()
                key = None
                if event.EventType == "GOAL":
                    goal_event = session.query(EventGoal).filter(EventGoal.GoalId == event.ExternalEventId).all()

                    # adding shot event before the goal
                    new_node.set_type("Event Node")
                    new_node.set_goal_home(current_node.get_goal_home())
                    new_node.set_goal_away(current_node.get_goal_away())
                    new_node.set_goal_diff(current_node.get_goal_diff())
                    new_node.set_no_home_players(current_node.get_no_home_players())
                    new_node.set_no_away_players(current_node.get_no_away_players())
                    new_node.set_man_diff(current_node.get_man_diff())
                    new_node.set_period(current_node.get_period())
                    # set the zone and the team that scores the goal
                    new_node.set_zone(goal_event.get_zone())
                    new_node.set_time_elapsed(goal_event.EventTime)
                    
                    # if the home team scores
                    if is_home_team(goal_event):
                        key = f"shot(Home,{goal_event.Zone}):"
                    else:
                        key = f"shot(away,{goal_event.zone}):"
                    # key of the form shot(home,offensive) or shot(away,offensive)
                    key += str(goal_event.EventTime.minute)

                    child_node = current_node.get_childeren().get(key)
                    # child node is not a child of the current node
                    if(child_node == None):
                        new_node.increment_count()
                        new_node.parent
                        current_node.add_child(key,new_node)
                    else:
                        child_node.increment_count()







                    # create a shot event as a child of the current_node
                    # before adding a goal event

                    

                root.increment_count()


if __name__ == "__main__":
    engine = database.create_connection(
        user=os.environ["db_user"],
        password=os.environ["db_pass"],
        host=os.environ["db_host"],
        database=os.environ["db_name"],
    )
    season = "2013-2014"
    session = sessionmaker(bind=engine)()
    season_type = "Regular Season"
    # orms = extract_season(season=season, session=session, season_type=season_type)
    # build_tree(session, season, season_type, time_array=[])

    game_ids = get_game_ids(session, season, season_type=season_type)
    results = extract_game(season,session,game_ids[0][0],season_type)
    print(results[3].EventType)
