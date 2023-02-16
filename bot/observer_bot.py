from typing import Iterable
import csv
from os import PathLike
from tqdm import tqdm
import pandas as pd

from sc2.observer_ai import ObserverAI
from sc2.unit import Unit

from bot.counter.counter import BotCounter
from bot.extension import BotExtension
from bot.ids.units import RACE_MAPPING
from collections import Counter

class ObserverBot(ObserverAI):
    def __init__(self, dataset_path: str | PathLike, progress_bar: tqdm):
        super().__init__()
        self._progress_bar = progress_bar
        self.path = dataset_path
        self.iteration = 0
        self.counter = BotCounter(self)
        self.dataframe: pd.DataFrame | None = None
        self.columns = []

    async def on_start(self):
        await self.counter.on_start()

        features_columns = self.counter.features_set().keys()
        self.columns = list(features_columns) + [f'ORDER_{key.name}' for key in RACE_MAPPING[self.race]]

        self.dataframe = pd.DataFrame(
            data={},
            columns=self.columns
        )

    async def on_unit_destroyed(self, unit_tag: int):
        await self.counter.on_unit_destroyed(unit_tag)

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        await self.counter.on_enemy_unit_entered_vision(unit)

    async def on_step(self, iteration):
        self.iteration = iteration
        self._progress_bar.update(self.state.game_loop // 16 - self._progress_bar.n)

        for order in self.new_orders():
            features = self.counter.features_set()
            features[f'ORDER_{order.name}'] = 1
            df = pd.DataFrame(features, index=[iteration])
            self.dataframe = pd.concat([self.dataframe, df]).fillna(0)

        await self.counter.after_step(iteration)

    def new_orders(self) -> Iterable:
        for key, val in self.counter.orders.new_creation_order().items():
            for _ in range(val):
                yield key

    def on_end(self, result):
        self._progress_bar.close()
        self.dataframe.to_csv(self.path)
        print("Game ended.")
