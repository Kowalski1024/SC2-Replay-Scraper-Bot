import enum


class Labels(enum.Enum):
    # 0 - 15 claimed for state

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

    # Upgrades 56 - 75
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