import random

from sc2.main import run_game
from sc2 import maps
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer, Difficulty
from sc2.units import Unit
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId


class AI(BotAI):
    def __init__(self):
        super().__init__()

    async def on_start(self):
        print("Game started")

    async def train_workers(self):
        if len(self.townhalls) * 22 > len(self.units(UnitTypeId.PROBE)):
            for nexus in self.townhalls.ready.idle:
                if (
                        self.can_afford(UnitTypeId.PROBE)
                ):
                    nexus.train(UnitTypeId.PROBE)

    async def build_gateway(self):
        if (
                self.can_afford(UnitTypeId.GATEWAY)
                and self.structures(UnitTypeId.PYLON).ready
                and self.structures({UnitTypeId.GATEWAY, UnitTypeId.WARPGATE}).amount < 4
        ):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.GATEWAY, near=pylon)

    async def build_gas(self):
        if self.structures({UnitTypeId.GATEWAY, UnitTypeId.WARPGATE}).exists:
            for nexus in self.townhalls.ready:
                vgs = self.vespene_geyser.closer_than(15, nexus)
                for vg in vgs:
                    if self.can_afford(UnitTypeId.ASSIMILATOR):
                        await self.build(UnitTypeId.ASSIMILATOR, vg)

    async def build_pylon(self):
        if self.supply_left < 5 and self.can_afford(UnitTypeId.PYLON) and not self.already_pending(UnitTypeId.PYLON):
            _main: Unit = self.townhalls.first
            pos = _main.position.towards(self.game_info.map_center, random.randint(4, 8))
            await self.build(UnitTypeId.PYLON, near=pos)

    async def build_cyber(self):
        if (
                self.can_afford(UnitTypeId.CYBERNETICSCORE)
                and self.structures({UnitTypeId.GATEWAY, UnitTypeId.WARPGATE}).ready
                and not self.structures(UnitTypeId.CYBERNETICSCORE)
                and not self.already_pending(UnitTypeId.CYBERNETICSCORE)
        ):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            await self.build(UnitTypeId.CYBERNETICSCORE, pylon)

    async def train_stalkers(self):
        if self.structures(UnitTypeId.CYBERNETICSCORE).ready:
            if self.warp_gate_count:
                pylon = self.structures(UnitTypeId.PYLON).closest_to(self.enemy_start_locations[0])
                for warp in self.structures(UnitTypeId.WARPGATE):
                    pos = pylon.position.random_on_distance(random.randint(2, 6))
                    warp.warp_in(UnitTypeId.STALKER, pos, can_afford_check=True)
            else:
                for gate in self.structures(UnitTypeId.GATEWAY).idle:
                    gate.train(UnitTypeId.STALKER, can_afford_check=True)

    async def attack_enemy(self):
        if self.units(UnitTypeId.STALKER).idle.amount > 8:
            for stalker in self.units(UnitTypeId.STALKER):
                enemy = self.enemy_units | self.enemy_structures
                if enemy:
                    stalker.attack(enemy.closest_to(stalker))
                else:
                    stalker.attack(self.enemy_start_locations[0])

    async def stalker_micro(self):
        enemy = (self.enemy_units | self.enemy_structures)
        if enemy:
            for stalker in self.units(UnitTypeId.STALKER):
                closest_enemy = enemy.closest_to(stalker)
                if closest_enemy and stalker.weapon_cooldown > 2:
                    if self.enemy_units.exclude_type(UnitTypeId.PROBE):
                        stalker.move(stalker.position.towards(closest_enemy, distance=-2))
                        stalker.attack(closest_enemy, queue=True)
                    else:
                        stalker.smart(stalker.position.towards(closest_enemy, distance=2))
                        stalker.attack(closest_enemy, queue=True)

    async def on_step(self, iteration):
        await self.distribute_workers()
        await self.train_workers()
        await self.build_pylon()
        await self.build_cyber()
        await self.build_gas()
        await self.build_gateway()
        await self.train_stalkers()
        await self.attack_enemy()
        await self.stalker_micro()
        self.research(UpgradeId.WARPGATERESEARCH)

    def on_end(self, result):
        print("Game ended.", result)


def main():
    # "DeathAura506"
    # VeryEasy, Easy, Medium, MediumHard, Hard, Harder, VeryHard, CheatVision, CheatMoney, CheatInsane
    run_game(maps.get("BlackburnAIE"), [
        Bot(Race.Protoss, AI()),
        # Bot(Race.Zerg, Enemy())
        Computer(Race.Protoss, Difficulty.VeryHard)
    ], realtime=False, disable_fog=False, save_replay_as='AIvsAI_2.SC2Replay')


if __name__ == '__main__':
    main()