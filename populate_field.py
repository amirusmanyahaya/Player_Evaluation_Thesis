import database
import os
from orm_model import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import func
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


def is_start_marker(event):
    start_markers = ["Period Start", "Early Intermission Start"]
    if event in start_markers:
        return True
    else:
        return False


def is_leaf_node(event):
    end_markers = ["GAME END", "STOPPAGE", "PENALTY", "GOAL", "PERIOD END"]
    if event in end_markers:
        return True
    else:
        return False


def is_home_team(event):
    return event[0].ScoringTeamId == event[0].HomeTeamId


# def generate_context_key(parent_gd,parent_md,event,):
#     # generates a context node of the form GD:MD:P:T
#     return f"{parent_gd}:{parent_md}:{event.PeriodNumber}:{0 if event.EventTime.minute < 10 else''}"

# def generate_non_context_key(parent_gd,parent_md,event):
#     return f"{}"


def generate_node(
    event, session, home_goal, away_goal, home_players, away_players, context=False
):
    result = None
    zone = None
    event_type = None
    performed_by = None
    new_node = Node()

    # setting the values of the new node
    new_node.set_goal_home(home_goal)
    new_node.set_goal_away(away_goal)
    new_node.set_no_away_players(away_players)
    new_node.set_no_home_players(home_players)

    if event.EventType == "PERIOD START":
        result = session.query(EventPeriodStart).filter(
            event.ExternalEventId == EventPeriodStart.PeriodStartId
        )
        event_type = "period_start"
    elif event.EventType == "FACEOFF":
        result = session.query(EventFaceoff).filter(
            event.ExternalEventId == EventFaceoff.FaceoffId
        )
        zone = result[0].Zone
        event_type = "faceoff"
        performed_by = (
            "Home" if result[0].FaceoffWinningTeamId == result[0].HomeTeamId else "Away"
        )
    elif event.EventType == "MISSED SHOT":
        result = session.query(EventMissedShot).filter(
            event.ExternalEventId == EventMissedShot.MissId
        )
        zone = result[0].Zone
        event_type = "missed_shot"
        performed_by = (
            "Home" if result[0].MissTeamId == result[0].HomeTeamId else "Away"
        )
    elif event.EventType == "SHOT":
        result = session.query(EventShot).filter(
            event.ExternalEventId == EventShot.ShotId
        )
        zone = result[0].Zone
        event_type = "shot"
        performed_by = (
            "Home" if result[0].ShotByTeamId == result[0].HomeTeamId else "Away"
        )
    elif event.EventType == "HIT":
        result = session.query(EventHit).filter(event.ExternalEventId == EventHit.HitId)
        zone = result[0].Zone
        event_type = "hit"
        performed_by = (
            "Home" if result[0].HittingTeamId == result[0].HomeTeamId else "Away"
        )
    elif event.EventType == "BLOCKED SHOT":
        result = session.query(EventBlockedShot).filter(
            event.ExternalEventId == EventBlockedShot.BlockId
        )
        zone = result[0].Zone
        event_type = "blocked_shot"
        performed_by = (
            "Home" if result[0].BlockTeamId == result[0].HomeTeamId else "Away"
        )

    elif event.EventType == "GIVEAWAY":
        result = session.query(EventGiveaway).filter(
            event.ExternalEventId == EventGiveaway.GiveawayId
        )
        zone = result[0].Zone
        event_type = "giveaway"
        performed_by = (
            "Home" if result[0].GiveawayTeamId == result[0].HomeTeamId else "Away"
        )
    elif event.EventType == "PENALTY":
        result = session.query(EventPenalty).filter(
            event.ExternalEventId == EventPenalty.PenaltyId
        )
        zone = result[0].Zone
        event_type = "penalty"
        performed_by = (
            "Home" if result[0].TeamPenaltyId == result[0].HomeTeamId else "Away"
        )
    elif event.EventType == "GOAL":
        result = session.query(EventGoal).filter(
            event.ExternalEventId == EventGoal.GoalId
        )
        zone = result[0].Zone
        event_type = "goal"
        performed_by = (
            "Home" if result[0].ScoringTeamId == result[0].HomeTeamId else "Away"
        )

    new_node.set_time_elapsed(event.EventTime.minute)
    new_node.set_period(event.PeriodNumber)
    key = None

    if context == True:
        if event_type == "goal":
            if performed_by == "home":
                new_node.set_goal_home(new_node.get_goal_home + 1)
                new_node.set_goal_away(new_node.get_goal_away - 1)
            else:
                new_node.set_goal_home(new_node.get_goal_home - 1)
                new_node.set_goal_away(new_node.get_goal_away + 1)
        elif event_type == "penalty":
            if performed_by == "home":
                new_node.set_no_away_players(new_node.get_no_away_players() - 1)
            else:
                new_node.set_no_home_players(new_node.get_no_home_players() - 1)

    if zone == None and performed_by == None:
        if context == True:
            key = f"{new_node.get_goal_diff()}:{new_node.get_man_diff()}:{event.Period}:{event.EventTime.minute}"
        else:
            # creates a key of the form "period_start:0:0:1:0"
            key = f"{event_type}:{new_node.get_goal_diff()}:{new_node.get_man_diff()}:{event.Period}:{event.EventTime.minute}"
    else:
        new_node.set_zone(zone)
        # creates a key of the form "faceoff(home,neutral):0:0:1:0"
        key = f"{event_type}({performed_by},{zone}):{new_node.get_goal_diff()}:{new_node.get_man_diff()}:{event.Period}:{event.EventTime.minute}"

    return key, new_node


def build_tree(session, season, season_type, time_array):
    # initialize a root node
    root = Node()
    root.set_type("Root Node")
    root.set_goal_away(0)
    root.set_goal_home(0)
    root.set_goal_diff(0)
    root.set_no_away_players(0)
    root.set_no_home_players(0)
    root.set_man_diff(0)
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
        for event in extract_game(season, session, game_id, season_type):
            # if event is a start or end marker
            # generate context key for the event
            # if current node is not the root node
            # if key is a child of the root node
            # if key is not a child of our current node
            # add the context node to the list of cildren of the current node
            # else
            # increment the transiton context node to the current node
            # else if the key is not a child of the root node
            # add the context node to the root node
            # add the context node to the leaf node
            #  else if the current node is the root node
            # add the context node to the root node
            # incrment the occurance of the child node
            # set current to be equal to the context
            # generate non context key for the event
            # if non context key is a child of current key
            # increment the transiton count for the current node to the non-context node
            # else if non context key is not a child of current node
            # add the the non context key to current node
            # incrment the count of the non context node
            # set the current node to be the non context node

            pass


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
    results = extract_game(season, session, game_ids[0][0], season_type)
    results_2 = (
        session.query(
            PlayByPlayEvents.AwayPlayer1,
            PlayByPlayEvents.AwayPlayer2,
            PlayByPlayEvents.AwayPlayer3,
            PlayByPlayEvents.AwayPlayer4,
            PlayByPlayEvents.AwayPlayer5,
            PlayByPlayEvents.AwayPlayer6,
            PlayByPlayEvents.AwayPlayer7,
            PlayByPlayEvents.AwayPlayer8,
            PlayByPlayEvents.AwayPlayer9,
        )
        .filter(
            PlayByPlayEvents.EventNumber == results[0].EventNumber,
            PlayByPlayEvents.GameId == results[0].GameId,
        )
        .all()
    )
    # generate_node(session,event,goal_home=0,goal_away=0,no_home_ply=6,no_away_ply=6,context=True) #("0:0:1:0",context_node)
    print(sum(x != None for x in results_2[0]))
