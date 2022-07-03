
from __future__ import annotations
from collections import Counter
from typing import Dict, List, Set, Union, TYPE_CHECKING

from sc2.cache import property_cache_once_per_frame
from sc2.data import Alert, Race, Result, ActionResult, race_townhalls
from sc2.game_data import GameData
from sc2.bot_ai_internal import BotAIInternal
from sc2.game_state import EffectData

from sc2.constants import (
    ALL_GAS,
    IS_PLACEHOLDER,
    TERRAN_STRUCTURES_REQUIRE_SCV,
    FakeEffectID,
    abilityid_to_unittypeid,
    geyser_ids,
    mineral_ids,
)

# Imports for mypy and pycharm autocomplete as well as sphinx autodocumentation
from sc2.game_state import Blip, GameState
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units

if TYPE_CHECKING:
    from sc2.game_info import GameInfo
    from sc2.client import Client
    from sc2.unit_command import UnitCommand


class ObserverAI(BotAIInternal):
    """Base class for bots."""

    @property
    def time(self) -> float:
        """ Returns time in seconds, assumes the game is played on 'faster' """
        return self.state.game_loop / 22.4  # / (1/1.4) * (1/16)

    @property
    def time_formatted(self) -> str:
        """ Returns time as string in min:sec format """
        t = self.time
        return f"{int(t // 60):02}:{int(t % 60):02}"

    def alert(self, alert_code: Alert) -> bool:
        """
        Check if alert is triggered in the current step.
        Possible alerts are listed here https://github.com/Blizzard/s2client-proto/blob/e38efed74c03bec90f74b330ea1adda9215e655f/s2clientprotocol/sc2api.proto#L679-L702
        Example use:
            from sc2.data import Alert
            if self.alert(Alert.AddOnComplete):
                print("Addon Complete")
        Alert codes::
            AlertError
            AddOnComplete
            BuildingComplete
            BuildingUnderAttack
            LarvaHatched
            MergeComplete
            MineralsExhausted
            MorphComplete
            MothershipComplete
            MULEExpired
            NuclearLaunchDetected
            NukeComplete
            NydusWormDetected
            ResearchComplete
            TrainError
            TrainUnitComplete
            TrainWorkerComplete
            TransformationComplete
            UnitUnderAttack
            UpgradeComplete
            VespeneExhausted
            WarpInComplete
        :param alert_code:
        """
        assert isinstance(alert_code, Alert), f"alert_code {alert_code} is no Alert"
        return alert_code.value in self.state.alerts

    @property
    def start_location(self) -> Point2:
        """
        Returns the spawn location of the bot, using the position of the first created townhall.
        This will be None if the bot is run on an arcade or custom map that does not feature townhalls at game start.
        """
        return self.game_info.player_start_location

    @property
    def enemy_start_locations(self) -> List[Point2]:
        """Possible start locations for enemies."""
        return self.game_info.start_locations

    async def get_available_abilities(
        self, units: Union[List[Unit], Units], ignore_resource_requirements: bool = False
    ) -> List[List[AbilityId]]:
        """Returns available abilities of one or more units. Right now only checks cooldown, energy cost, and whether the ability has been researched.
        Examples::
            units_abilities = await self.get_available_abilities(self.units)
        or::
            units_abilities = await self.get_available_abilities([self.units.random])
        :param units:
        :param ignore_resource_requirements:"""
        return await self.client.query_available_abilities(units, ignore_resource_requirements)

    async def on_unit_destroyed(self, unit_tag: int):
        """
        Override this in your bot class.
        Note that this function uses unit tags and not the unit objects
        because the unit does not exist any more.
        This will event will be called when a unit (or structure, friendly or enemy) dies.
        For enemy units, this only works if the enemy unit was in vision on death.

        :param unit_tag:
        """

    async def on_unit_created(self, unit: Unit):
        """Override this in your bot class. This function is called when a unit is created.

        :param unit:"""

    async def on_unit_type_changed(self, unit: Unit, previous_type: UnitTypeId):
        """Override this in your bot class. This function is called when a unit type has changed. To get the current UnitTypeId of the unit, use 'unit.type_id'

        This may happen when a larva morphed to an egg, siege tank sieged, a zerg unit burrowed, a hatchery morphed to lair,
        a corruptor morphed to broodlordcocoon, etc..

        Examples::

            print(f"My unit changed type: {unit} from {previous_type} to {unit.type_id}")

        :param unit:
        :param previous_type:
        """

    async def on_building_construction_started(self, unit: Unit):
        """
        Override this in your bot class.
        This function is called when a building construction has started.

        :param unit:
        """

    async def on_building_construction_complete(self, unit: Unit):
        """
        Override this in your bot class. This function is called when a building
        construction is completed.

        :param unit:
        """

    async def on_upgrade_complete(self, upgrade: UpgradeId):
        """
        Override this in your bot class. This function is called with the upgrade id of an upgrade that was not finished last step and is now.

        :param upgrade:
        """

    async def on_unit_took_damage(self, unit: Unit, amount_damage_taken: float):
        """
        Override this in your bot class. This function is called when your own unit (unit or structure) took damage.
        It will not be called if the unit died this frame.

        This may be called frequently for terran structures that are burning down, or zerg buildings that are off creep,
        or terran bio units that just used stimpack ability.
        TODO: If there is a demand for it, then I can add a similar event for when enemy units took damage

        Examples::

            print(f"My unit took damage: {unit} took {amount_damage_taken} damage")

        :param unit:
        """

    async def on_enemy_unit_entered_vision(self, unit: Unit):
        """
        Override this in your bot class. This function is called when an enemy unit (unit or structure) entered vision (which was not visible last frame).

        :param unit:
        """

    async def on_enemy_unit_left_vision(self, unit_tag: int):
        """
        Override this in your bot class. This function is called when an enemy unit (unit or structure) left vision (which was visible last frame).
        Same as the self.on_unit_destroyed event, this function is called with the unit's tag because the unit is no longer visible anymore.
        If you want to store a snapshot of the unit, use self._enemy_units_previous_map[unit_tag] for units or self._enemy_structures_previous_map[unit_tag] for structures.

        Examples::

            last_known_unit = self._enemy_units_previous_map.get(unit_tag, None) or self._enemy_structures_previous_map[unit_tag]
            print(f"Enemy unit left vision, last known location: {last_known_unit.position}")

        :param unit_tag:
        """

    async def on_before_start(self):
        """
        Override this in your bot class. This function is called before "on_start"
        and before "prepare_first_step" that calculates expansion locations.
        Not all data is available yet.
        This function is useful in realtime=True mode to split your workers or start producing the first worker.
        """

    async def on_start(self):
        """
        Override this in your bot class.
        At this point, game_data, game_info and the first iteration of game_state (self.state) are available.
        """

    async def on_step(self, iteration: int):
        """
        You need to implement this function!
        Override this in your bot class.
        This function is called on every game step (looped in realtime mode).

        :param iteration:
        """
        raise NotImplementedError

    async def on_end(self, game_result: Result):
        """Override this in your bot class. This function is called at the end of a game.
        Unsure if this function will be called on the laddermanager client as the bot process may forcefully be terminated.

        :param game_result:"""