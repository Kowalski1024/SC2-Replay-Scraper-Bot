from typing import Iterable

from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.data import Result


class BotExtension:
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

    async def before_step(self, iteration: int):
        """
        You need to implement this function!
        Override this in your bot class.
        This function is called on every game step (looped in realtime mode).

        :param iteration:
        """

    async def after_step(self, iteration: int):
        """
        You need to implement this function!
        Override this in your bot class.
        This function is called on every game step (looped in realtime mode).

        :param iteration:
        """

    async def on_end(self, game_result: Result):
        """Override this in your bot class. This function is called at the end of a game.
        Unsure if this function will be called on the laddermanager client as the bot process may forcefully be terminated.

        :param game_result:"""