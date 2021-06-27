from typing import Type
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base

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


class EventPeriodStart:
    __tablename__ = "event_period_start"
    PeriodStartId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventLocalTime = Column(Time)
    TimeZone = Column(Text)


class EventFaceoff:
    __tablename__ = "event_faceoff"
    FaceoffId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    FaceoffWinningTeam = Column(Text)
    FaceoffWinningTeamId = Column(Integer)
    Zone = Column(Text)
    AwayPlayerNumber = Column(Integer)
    AwayPlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    HomePlayerNumber = Column(Integer)
    HomePlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    WinningTeamDisposition = Column(Text)


class EventMissedShot:
    __tablename__ = "event_missed_shot"
    MissId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    MissTeam = Column(Text)
    MissTeamId = Column(Integer)
    Disposition = Column(Text)
    PlayerNumber = Column(Integer)
    PlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    ShotType = Column(Text)
    Reason = Column(Text)
    Zone = Column(Text)
    Distance = Column(Float)


class EventShot:
    __tablename__ = "event_shot"
    ShotId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    ShotByTeam = Column(Text)
    ShotbyTeamId = Column(Integer, ForeignKey(Team.TeamId))
    TeamDisposition = Column(Text)
    ShootingPlayerNumber = Column(Integer)
    ShootingPlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    ShotType = Column(Text)
    Zone = Column(Text)
    Distance = Column(Float)


class EventHit:
    __tablename__ = "event_hit"
    HitId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    HittingTeam = Column(Text)
    HittingTeamId = Column(Integer)
    Disposition = Column(Text)
    PlayerNumber = Column(Integer)
    PlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    HitPlayerNumber = Column(Integer)
    HitPlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    Zone = Column(Text)


class EventBlockedShot:
    __tablename__ = "event_blocked_shot"
    BlockId = Column(Integer, primary_key=True)
    GameId = Column(Integer, ForeignKey(Game.GameId), primary_key=True)
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    BlockTeam = Column(Text)
    BlockTeamId = Column(Integer, ForeignKey(Team.TeamId))
    Dispositon = Column(Text)
    PlayerNumber = Column(Integer)
    PlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    BlockedTeam = Column(Text)
    BlockedTeamId = Column(Integer, ForeignKey(Team.TeamId))
    BlockedPlayerNumber = Column(Integer)
    BlockedPlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    ShotType = Column(Text)
    Zone = Column(Text)


class EventStoppage:
    __tablename__ = "event_stoppage"
    StoppageId = Column(Integer, primary_key=True)
    GameId = Column(Integer, ForeignKey(Game.GameId), primary_key=True)
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    Reason = Column(Text)


class EventGiveaway:
    __tablename__ = "event_giveaway"
    GiveawayId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    GiveawayTeam = Column(Text)
    GiveawayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    Disposition = Column(Text)
    PlayerNumber = Column(Integer)
    PlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    Zone = Column(Text)


class EventPenalty:
    __tablename__ = "event_penalty"
    PenaltyId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    TeamPenalty = Column(Text)
    TeamPenaltyId = Column(Integer, ForeignKey(Team.TeamId))
    PlayerNumber = Column(Integer)
    PlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    PenaltyType = Column(Text)
    PenaltyDuration = Column(Integer)
    Zone = Column(Text)
    DrawnByPlayerNumber = Column(Integer)
    DrawnByPlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    PenalizedTeamDisposition = Column(Text)


class EventGoal:
    __tablename__ = "event_goal"
    GoalId = Column(Integer, primary_key=True)
    GameId = Column(Integer, ForeignKey(Game.GameId), primary_key=True)
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    ScoringTeam = Column(Text)
    ScoringTeamId = Column(Integer, ForeignKey(Team.TeamId))
    Disposition = Column(Text)
    GoalScorerNumber = Column(Integer)
    GoalScorerId = Column(Integer, ForeignKey(Player.PlayerId))
    NumGoals = Column(Integer)
    FirstAssistNumber = Column(Integer)
    FirstAssistId = Column(Integer, ForeignKey(Player.PlayerId))
    NumAssistsFirstPlayer = Column(Integer)
    SecondAssistNumber = Column(Integer)
    SecondAssistId = Column(Integer, ForeignKey(Player.PlayerId))
    NumberAssistsSecondPlayer = Column(Integer)
    ShotType = Column(Text)
    Zone = Column(Text)
    ShotDistance = Column(Float)


class EventTakeaway:
    __tablename__ = "event_takeaway"
    TakeawayId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    TakeawayTeam = Column(Text)
    TakeawayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    Disposition = Column(Text)
    PlayerNumber = Column(Integer)
    PlayerId = Column(Integer, ForeignKey(Player.PlayerId))
    Zone = Column(Text)


class EventPeriodEnd:
    __tablename__ = "event_period_end"
    PeriodEndId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventLocalTime = Column(Time)
    TimeZone = Column(Text)


class EventGameEnd:
    __tablename__ = "event_game_end"
    GameEndId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventLocalTime = Column(Time)
    TimeZone = Column(Text)


class EventShootoutCompleted:
    __tablename__ = "event_shootout_completed"
    ShootoutCompletedId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventLocalTime = Column(Time)
    TimeZone = Column(Text)


class EventEarlyIntermissionStart:
    __tablename__ = "event_early_intermission_start"
    EarlyIntermissionStartId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventLocalTime = Column(Time)
    TimeZone = Column(Text)


class EventEarlyIntermissionEnd:
    __tablename__ = "event_early_intermission_end"
    EarlyIntermissionEndId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    EventLocalTime = Column(Time)
    TimeZone = Column(Text)


class EventGameOff:
    __tablename__ = "event_game_off"
    GameOffId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)


class EventGoaliePulled:
    GoaliePulledId = Column(Integer)
    GameId = Column(Integer, ForeignKey(Game.GameId))
    AwayTeamId = Column(Integer, ForeignKey(Team.TeamId))
    HomeTeamId = Column(Integer, ForeignKey(Team.TeamId))
    EventNumber = Column(Integer)
    PeriodNumber = Column(Integer)
    EventTime = Column(Time)
    TeamPullingGoalie = Column(Text)
    TeamPullingGoalieId = Column(Integer, ForeignKey(Team.TeamId))
    GoalieNumber = Column(Integer)
    GoalieId = Column(Integer, ForeignKey(Player.PlayerId))
