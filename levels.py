"""Layouts for all five JumpByte worlds."""

from enemy import Boss, Enemy
from objects import Coin, Hazard, Platform, PowerUp


def build_stage_one():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(210, 405, 150),
        Platform(440, 335, 150),
        Platform(700, 405, 170),
        Platform(920, 380, 150),
        Platform(1170, 410, 170),
    ]
    coins = [
        Coin(x, y)
        for x, y in [
            (260, 370), (490, 300), (750, 370),
            (1060, 315), (1320, 375),
        ]
    ]
    powerups = [PowerUp(740, 370)]
    hazards = [Hazard(885, 490, color=(95, 155, 75))]
    enemies = [Enemy(560, 460, 520, 650)]
    info = {
        "name": "Green Meadow",
        "number": 1,
        "background": (155, 215, 245),
    }
    return {
        "platforms": platforms,
        "coins": coins,
        "powerups": powerups,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }


def build_stage_two():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(170, 410, 130),
        Platform(370, 345, 140),
        Platform(610, 405, 150),
        Platform(850, 325, 140),
        Platform(1090, 395, 150),
        Platform(1360, 335, 170),
    ]
    coins = [
        Coin(x, y)
        for x, y in [
            (205, 375), (415, 310), (660, 370),
            (895, 290), (1135, 360), (1415, 300),
        ]
    ]
    enemies = [
        Enemy(520, 460, 470, 590),
        Enemy(1030, 460, 970, 1080),
    ]
    hazards = [
        Hazard(770, 490, color=(90, 220, 235)),
        Hazard(1260, 490, color=(165, 130, 255)),
    ]
    info = {
        "name": "Moonlit Cave",
        "number": 2,
        "background": (45, 35, 75),
    }
    return {
        "platforms": platforms,
        "coins": coins,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }


def build_stage_three():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(170, 410, 140),
        Platform(400, 340, 150),
        Platform(660, 405, 150),
        Platform(900, 330, 150),
        Platform(1160, 400, 150),
        Platform(1390, 335, 170),
    ]
    coins = [
        Coin(x, y)
        for x, y in [
            (210, 375), (445, 305), (705, 370),
            (945, 295), (1205, 365), (1440, 300),
        ]
    ]
    enemies = [
        Enemy(520, 460, 470, 620),
        Enemy(850, 460, 820, 1080),
    ]
    hazards = [
        Hazard(760, 490, color=(245, 105, 90)),
        Hazard(1265, 490, color=(255, 165, 85)),
    ]
    info = {
        "name": "Sunset Castle",
        "number": 3,
        "background": (112, 84, 126),
    }
    return {
        "platforms": platforms,
        "coins": coins,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }


def build_stage_four():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(170, 410, 130),
        Platform(380, 340, 140),
        Platform(610, 400, 150),
        Platform(840, 325, 140),
        Platform(1080, 390, 150),
        Platform(1340, 335, 170),
    ]
    coins = [
        Coin(x, y)
        for x, y in [
            (210, 375), (425, 305), (660, 365),
            (880, 290), (1130, 355), (1400, 300),
        ]
    ]
    powerups = [PowerUp(660, 365)]
    enemies = [
        Enemy(500, 460, 450, 590),
        Enemy(1020, 460, 960, 1080),
    ]
    hazards = [
        Hazard(760, 490, color=(135, 225, 255)),
        Hazard(1260, 490, color=(195, 245, 255)),
    ]
    info = {
        "name": "Frostfall Peaks",
        "number": 4,
        "background": (175, 220, 240),
    }
    return {
        "platforms": platforms,
        "coins": coins,
        "powerups": powerups,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }


def build_stage_five():
    platforms = [
        Platform(0, 490, 1600, 50),
        Platform(150, 410, 140),
        Platform(350, 345, 150),
        Platform(590, 405, 150),
        Platform(830, 335, 150),
        Platform(1080, 400, 160),
        Platform(1340, 330, 180),
    ]
    coins = [
        Coin(x, y)
        for x, y in [
            (195, 375), (395, 310), (640, 370),
            (875, 300), (1130, 365), (1400, 295),
        ]
    ]
    powerups = [PowerUp(1130, 365)]
    enemies = [
        Enemy(520, 460, 470, 650),
        Boss(960, 442, 900, 1220),
    ]
    hazards = [
        Hazard(760, 490, color=(165, 115, 255)),
        Hazard(1260, 490, color=(245, 205, 105)),
    ]
    info = {
        "name": "Skyforge Citadel",
        "number": 5,
        "background": (45, 55, 105),
    }
    return {
        "platforms": platforms,
        "coins": coins,
        "powerups": powerups,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }
