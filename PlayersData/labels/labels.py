from typing import Union
import enum

from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

from .alias import correct_alias, alias


class ProtossLabels(enum.IntEnum):
    # Units 16 - 35
    PROBE = 16
    ZEALOT = 17
    STALKER = 18
    SENTRY = 19
    ADEPT = 20
    HIGHTEMPLAR = 21
    DARKTEMPLAR = 22
    IMMORTAL = 23
    COLOSSUS = 24
    DISRUPTOR = 25
    ARCHON = 26
    OBSERVER = 27
    WARPPRISM = 28
    PHOENIX = 29
    VOIDRAY = 30
    ORACLE = 31
    CARRIER = 32
    TEMPEST = 33
    MOTHERSHIP = 34

    # Structures 36 - 55
    NEXUS = 36
    PYLON = 37
    ASSIMILATOR = 38
    GATEWAY = 39
    FORGE = 40
    CYBERNETICSCORE = 41
    PHOTONCANNON = 42
    SHIELDBATTERY = 43
    ROBOTICSFACILITY = 44
    STARGATE = 45
    TWILIGHTCOUNCIL = 46
    ROBOTICSBAY = 47
    FLEETBEACON = 48
    TEMPLARARCHIVE = 49
    DARKSHRINE = 50

    # Upgrades 56 - 79
    GROUNDATTACK = 56
    FLYERATTACK = 57
    GROUNDARMOR = 58
    FLYERARMOR = 59
    SHIELDARMOR = 60
    CHARGE = 61
    OBSERVERGRAVITICBOOSTER = 62
    GRAVITICDRIVE = 63
    VOIDRAYSPEEDUPGRADE = 64
    ADEPTPIERCINGATTACK = 65
    PHOENIXRANGEUPGRADE = 66
    EXTENDEDTHERMALLANCE = 67
    PSISTORMTECH = 68
    BLINKTECH = 69
    DARKTEMPLARBLINKUPGRADE = 70
    WARPGATERESEARCH = 71
    TEMPESTGROUNDATTACKUPGRADE = 72


class Labels(ProtossLabels):
    # 0 - 15 claimed for state
    MINERALS = 0
    VESPENE = 1
    FOOD_LEFT = 2
    FOOD_USED = 3
    UNIT_DISTANCE = 4
    STRUCTURE_DISTANCE = 5
    EXPANSIONS = 6
    # Units 16 - 35
    # Structures 36 - 55
    # Upgrades 56 - 79

    @staticmethod
    def get_value(u: Union[Unit, UnitTypeId, UpgradeId]) -> int:
        if isinstance(u, Unit):
            u = u.type_id
        _type = correct_alias.get(u, u)
        return alias[_type].value
