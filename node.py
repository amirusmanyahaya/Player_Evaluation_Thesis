class Node:
    number_of_node = 0

    def __init__(self) -> None:
        self.type = None
        self.node_id = Node.number_of_node + 1
        self.goal_home = 0
        self.goal_away = 0
        self.goal_diff = 0
        self.no_home_players = 0
        self.no_away_players = 0
        self.man_diff = 0
        self.zone = None
        self.period = 0
        self.time_elapsed = 0
        self.count = 0
        self.reward = 0
        self.parent = None
        self.childeren = dict()
        self.visited = False

    def set_type(self, type: str) -> None:
        self.type = type

    def set_node_id(self, node_id: int) -> None:
        self.node_id = node_id

    def set_goal_home(self, goals: int) -> None:
        self.goal_home = goals

    def set_goal_away(self, goals: int) -> None:
        self.goal_away = goals

    def set_goal_diff(self, goals: int) -> None:
        self.goal_diff = goals

    def set_no_home_players(self, players: int) -> None:
        self.no_home_players = players

    def set_no_away_players(self, players: int) -> None:
        self.no_away_players = players

    def set_man_diff(self, players: int) -> None:
        self.man_diff = players

    def set_zone(self, zone: str) -> None:
        self.zone = zone

    def set_period(self, period: int) -> None:
        self.period = period

    def set_parent(self, parent_node) -> None:
        self.parent = parent_node

    def set_time_elapsed(self, time_elapsed: int) -> None:
        self.time_elapsed = time_elapsed

    def set_count(self, count: int) -> None:
        self.count = count

    def set_reward(self, reward: int) -> None:
        self.reward = reward

    def increment_count(self):
        self.count += 1

    def add_child(self, key: str, new_node) -> None:
        self.childeren.update({key: [1, new_node]})

    def mark_as_visited(self) -> None:
        self.visited = True

    def get_type(self) -> str:
        return self.type

    def get_node_id(self) -> int:
        return self.node_id

    def get_goal_home(self) -> int:
        return self.goal_home

    def get_goal_away(self) -> int:
        return self.goal_away

    def get_goal_diff(self) -> int:
        return self.goal_home - self.goal_away

    def get_no_home_players(self) -> int:
        return self.no_home_players

    def get_no_away_players(self) -> int:
        return self.no_away_players

    def get_man_diff(self) -> int:
        return self.no_home_players - self.no_away_players

    def get_zone(self) -> str:
        return self.zone

    def get_period(self) -> int:
        return self.period

    def get_time_elapsed(self) -> int:
        return self.time_elapsed

    def get_count(self) -> int:
        return self.count

    def get_reward(self) -> int:
        return self.reward

    def get_childeren(self) -> dict:
        return self.childeren

    def get_child(self, key) -> list:
        return self.childeren.get(key)

    def is_visited(self) -> bool:
        return self.visited
