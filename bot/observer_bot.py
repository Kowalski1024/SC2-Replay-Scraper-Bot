import csv
import json
from os import PathLike
from tqdm import tqdm
from loguru import logger

from sc2.observer_ai import ObserverAI


class ObserverBot(ObserverAI):
    def __init__(self, dataset_path: str | PathLike, config_path: str | PathLike, progress_bar: tqdm):
        super().__init__()

        self._progress_bar = progress_bar
        self.file = open(dataset_path, 'w+', encoding='UTF8', newline='')
        self.writer = csv.writer(self.file)

        self.iteration = 0
    async def on_start(self):
        print("Game started")

    async def on_step(self, iteration):
        pass
        # self.before_step()
        self.iteration = iteration
        self._progress_bar.update(self.state.game_loop // 16 - self._progress_bar.n)
        # orders = {key: val for key, val in self.players_data.new_train_orders.items() if key not in EXCLUDE_ORDERS}
        # learning_data = [val for val in self.players_data.get_learning_data.values()]
        # for key, val in orders.items():
        #     actions = [0] * 40
        #     actions[Labels.get_value(key) - 16] = 1
        #     for _ in range(val):
        #         self.writer.writerow(learning_data + actions)
        # self.after_step()

    def on_end(self, result):
        self._progress_bar.close()
        self.file.close()
        print("Game ended.")
