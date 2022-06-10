import enum

from sc2.data import Race


class MetaData(enum.Enum):
    Player_1 = 0
    Player_2 = 1
    Map = 3


class PlayerDetails:
    def __init__(self, player_details):
        self._player_details = player_details
        self.race = self.get_race()
        self.team = player_details['m_teamId']
        self.result = player_details['m_result']

    def get_race(self):
        race_str = self._player_details['m_race'].decode('ascii')
        if race_str == 'Terran':
            return Race.Terran
        elif race_str == 'Zerg':
            return Race.Zerg
        else:
            return Race.Protoss

    @property
    def get_info(self):
        return [self.team, self.race.value, self.result]

    def __repr__(self):
        return f'[Team={self.team}, Race={self.race}, Result={self.result}]'