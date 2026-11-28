"""Layouts for all ten JumpByte worlds."""

from enemy import Boss, Enemy
from objects import Coin, Hazard, MovingPlatform, Platform, PowerUp
from settings import WORLD_WIDTH


def build_stage_one():
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
        Platform(210, 405, 150),
        Platform(440, 335, 150),
        Platform(700, 405, 170),
        Platform(920, 380, 150),
        Platform(1170, 410, 170),
    ]
    moving_platforms = [
        MovingPlatform(
            x=1080,
            y=340,
            width=90,
            height=18,
            top_y=285,
            bottom_y=395,
            speed=1,
        )
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
        "moving_platforms": moving_platforms,
        "coins": coins,
        "powerups": powerups,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }


def build_stage_two():
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
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
    powerups = [PowerUp(660, 370, kind="bullet")]
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
        "powerups": powerups,
        "coins": coins,
        "hazards": hazards,
        "enemies": enemies,
        "info": info,
    }


def build_stage_three():
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
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
        Platform(0, 490, WORLD_WIDTH, 50),
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
        Platform(0, 490, WORLD_WIDTH, 50),
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


def build_stage_six():
    """Ember Dunes: warm desert platforms with spaced hazards."""
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
        Platform(160, 410, 135), Platform(360, 345, 145),
        Platform(590, 405, 145), Platform(820, 325, 140),
        Platform(1050, 390, 150), Platform(1320, 330, 160),
    ]
    coins = [Coin(x, y) for x, y in [
        (205, 375), (405, 310), (640, 370),
        (865, 290), (1100, 355), (1370, 295),
    ]]
    enemies = [Enemy(500, 460, 450, 600), Enemy(1120, 460, 1080, 1230)]
    hazards = [Hazard(760, 490, color=(235, 115, 55)), Hazard(1260, 490, color=(245, 175, 65))]
    powerups = [PowerUp(640, 370)]
    info = {"name": "Ember Dunes", "number": 6, "background": (235, 165, 115)}
    return {"platforms": platforms, "coins": coins, "powerups": powerups,
            "hazards": hazards, "enemies": enemies, "info": info}


def build_stage_seven():
    """Coral Reef: a bright underwater route with a moving lift."""
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
        Platform(145, 415, 135), Platform(360, 350, 145),
        Platform(600, 405, 150), Platform(850, 320, 145),
        Platform(1100, 395, 150), Platform(1370, 330, 160),
    ]
    moving_platforms = [MovingPlatform(760, 370, 95, 18, 290, 420, 1)]
    coins = [Coin(x, y) for x, y in [
        (190, 380), (405, 315), (645, 370),
        (895, 285), (1145, 360), (1410, 295),
    ]]
    enemies = [Enemy(470, 460, 420, 590), Enemy(1010, 460, 960, 1090)]
    hazards = [Hazard(300, 490, color=(255, 105, 145)), Hazard(1250, 490, color=(255, 135, 170))]
    info = {"name": "Coral Reef", "number": 7, "background": (65, 165, 195)}
    return {"platforms": platforms, "moving_platforms": moving_platforms,
            "coins": coins, "hazards": hazards, "enemies": enemies, "info": info}


def build_stage_eight():
    """Clockwork Factory: narrow raised routes guarded by fast cats."""
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
        Platform(185, 405, 125), Platform(395, 330, 125),
        Platform(620, 395, 130), Platform(850, 315, 130),
        Platform(1080, 390, 135), Platform(1370, 325, 155),
    ]
    coins = [Coin(x, y) for x, y in [
        (225, 370), (435, 295), (660, 360),
        (885, 280), (1120, 355), (1410, 290),
    ]]
    enemies = [Enemy(500, 460, 455, 610), Enemy(1040, 460, 980, 1140)]
    hazards = [Hazard(330, 490, color=(245, 190, 70)), Hazard(780, 490, color=(220, 115, 65)), Hazard(1270, 490, color=(245, 190, 70))]
    powerups = [PowerUp(1120, 355, kind="bullet")]
    info = {"name": "Clockwork Factory", "number": 8, "background": (105, 125, 150)}
    return {"platforms": platforms, "coins": coins, "powerups": powerups,
            "hazards": hazards, "enemies": enemies, "info": info}


def build_stage_nine():
    """Cloud Kingdom: floating platforms connected by moving lifts."""
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
        Platform(150, 420, 125), Platform(370, 350, 135),
        Platform(610, 410, 135), Platform(850, 325, 135),
        Platform(1090, 395, 140), Platform(1370, 330, 160),
    ]
    moving_platforms = [MovingPlatform(720, 365, 95, 18, 285, 430, 1)]
    coins = [Coin(x, y) for x, y in [
        (190, 385), (410, 315), (650, 375),
        (890, 290), (1135, 360), (1410, 295),
    ]]
    enemies = [Enemy(470, 460, 420, 590), Enemy(1010, 460, 960, 1120)]
    hazards = [Hazard(300, 490, color=(145, 215, 255)), Hazard(790, 490, color=(180, 230, 255))]
    info = {"name": "Cloud Kingdom", "number": 9, "background": (145, 195, 235)}
    return {"platforms": platforms, "moving_platforms": moving_platforms,
            "coins": coins, "hazards": hazards, "enemies": enemies, "info": info}


def build_stage_ten():
    """Python Core: the final world and the last boss encounter."""
    platforms = [
        Platform(0, 490, WORLD_WIDTH, 50),
        Platform(150, 410, 135), Platform(365, 345, 145),
        Platform(600, 405, 145), Platform(835, 325, 140),
        Platform(1070, 390, 150), Platform(1350, 325, 175),
    ]
    coins = [Coin(x, y) for x, y in [
        (195, 375), (410, 310), (645, 370),
        (880, 290), (1115, 355), (1400, 290),
    ]]
    enemies = [Enemy(500, 460, 450, 610), Boss(960, 442, 900, 1240)]
    hazards = [Hazard(310, 490, color=(180, 105, 245)), Hazard(760, 490, color=(120, 190, 255)), Hazard(1280, 490, color=(255, 190, 80))]
    powerups = [PowerUp(645, 370, kind="bullet")]
    info = {"name": "Python Core", "number": 10, "background": (55, 55, 115)}
    return {"platforms": platforms, "coins": coins, "powerups": powerups,
            "hazards": hazards, "enemies": enemies, "info": info}
