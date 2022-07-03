import csv

from sc2.observer_ai import ObserverAI

from PlayersData.players_data import PlayersData


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
        if self.players_data.new_train_orders:
            self.writer.writerow(self.players_data.train_data)
        self.after_step()

    def on_end(self, result):
        self.file.close()
        print("Game ended.")
