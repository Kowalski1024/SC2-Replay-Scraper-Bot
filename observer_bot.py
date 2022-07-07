import csv
import json

from sc2.observer_ai import ObserverAI

from PlayersData.players_data import PlayersData
from PlayersData.labels import Labels, alias


with open("settings.json") as f:
    data = json.load(f)


EXCLUDE_ORDERS = {alias[Labels[_id]] for _id in data["exclude_id"]}


class ObserverBot(ObserverAI):
    def __init__(self, file_name: str):
        super().__init__()
        self._file_name = file_name
        self.file = open('data/datasets/'+self._file_name+'.csv', 'a', encoding='UTF8', newline='')
        self.writer = csv.writer(self.file)
        self.iteration = 0
        self.players_data = PlayersData(self)

    async def on_unit_destroyed(self, unit_tag: int):
        await self.players_data.on_unit_destroyed(unit_tag)

    async def on_start(self):
        print("Game started")

    def before_step(self):
        self.players_data.on_prepare_step()

    def after_step(self):
        self.players_data.after_step()

    async def on_step(self, iteration):
        self.before_step()
        self.iteration = iteration
        orders = {key: val for key, val in self.players_data.new_train_orders.items() if key not in EXCLUDE_ORDERS}
        learning_data = [val for val in self.players_data.get_learning_data.values()]
        for key, val in orders.items():
            actions = [0] * 40
            actions[Labels.get_value(key) - 16] = 1
            for _ in range(val):
                self.writer.writerow(learning_data + actions)
        self.after_step()

    def on_end(self, result):
        self.file.close()
        print("Game ended.")
