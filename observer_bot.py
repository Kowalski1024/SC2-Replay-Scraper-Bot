import csv
from sc2.observer_ai import ObserverAI
from collections import Counter
from PlayersData.players_data import PlayersData


class ObserverBot(ObserverAI):
    def __init__(self, file_name: str):
        super().__init__()
        self._file_name = file_name
        self.iteration = 0
        self._prev_abilities = Counter()
        self.players_data = PlayersData(self)

    async def on_unit_destroyed(self, unit_tag: int):
        await self.players_data.on_unit_destroyed(unit_tag)

    async def on_start(self):
        print("Game started")

    def on_prepare_step(self):
        self.players_data.on_prepare_step()

    def after_step(self):
        self.players_data.after_step()

    async def on_step(self, iteration):
        self.on_prepare_step()
        self.iteration = iteration
        if self.players_data.new_train_orders:
            with open('data/datasets/'+self._file_name+'.csv', 'a', encoding='UTF8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.players_data.train_data)
        self.after_step()

    def on_end(self, result):
        print("Game ended.")
