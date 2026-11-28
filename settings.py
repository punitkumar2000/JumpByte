
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
WINDOW_TITLE = "JumpByte - Python Platform Adventure"

# EASY GAME SETTINGS
# Change these values to adjust lives, movement, quiz length, and score.
# If WORLD_WIDTH changes a lot, adjust the world layouts in levels.py too.
WORLD_WIDTH = 1600
TOTAL_STAGES = 10
PLAYER_START_POSITION = (60, 400)
MAX_LIVES = 3
QUIZ_QUESTIONS_PER_WORLD = 2
CHECKPOINT_X = WORLD_WIDTH // 2
QUIZ_GATE_X = WORLD_WIDTH - 110
EXIT_REACHED_X = WORLD_WIDTH - 60

SCORE_COIN = 100
SCORE_POWERUP = 50
SCORE_CHECKPOINT = 200
SCORE_ENEMY_STOMP = 200
SCORE_BOSS_STOMP = 250
SCORE_BOSS_HIT = 100
SCORE_BOSS_DEFEAT = 500
SCORE_ENEMY_SHOT = 150
SCORE_CHEESE = 25
SCORE_CORRECT_ANSWER = 200
SCORE_WORLD_CLEAR = 500
SCORE_GAME_COMPLETE = 1000

ENEMY_SPEED = 2
ENEMY_GRAVITY = 0.5
ENEMY_JUMP_SPEED = -10
ENEMY_JUMP_DELAY = 120
ENEMY_SHOOT_DELAY = 90
ENEMY_BULLET_SPEED = 7
BOSS_HEALTH = 3
BOSS_SPEED = 1
BOSS_JUMP_DELAY = 90
BOSS_SHOOT_DELAY = 110
BOSS_ENRAGED_SPEED = 2
BOSS_ENRAGED_DELAY = 75
PLAYER_SHOT_SPEED = 10
SPEED_BOOST_FRAMES = 300
FIRE_POWER_SECONDS = 5.0
SHOT_COOLDOWN_SECONDS = 0.3

SKY = (155, 215, 245)
GRASS = (70, 170, 85)
DIRT = (125, 82, 50)
COIN_COLOR = (250, 205, 55)
WHITE = (250, 250, 250)
DARK = (35, 45, 60)

PLAYER_SPEED = 5
JUMP_SPEED = -13
GRAVITY = 0.65

# Visual colors for the platforms in each world. These only affect drawing;
# change a world's colors here without touching its level layout or gameplay.
LEVEL_THEMES = {
    1: {
        "top": (82, 190, 102), "highlight": (174, 242, 156),
        "soil": (145, 96, 62), "shadow": (77, 55, 56),
        "detail": (195, 136, 83), "accent": (122, 245, 174),
        "moving": (92, 192, 190),
    },
    2: {
        "top": (105, 91, 164), "highlight": (184, 170, 255),
        "soil": (65, 58, 96), "shadow": (35, 34, 59),
        "detail": (132, 120, 180), "accent": (172, 155, 255),
        "moving": (99, 128, 210),
    },
    3: {
        "top": (194, 101, 100), "highlight": (255, 190, 143),
        "soil": (111, 61, 72), "shadow": (63, 43, 61),
        "detail": (205, 126, 92), "accent": (255, 166, 128),
        "moving": (207, 125, 143),
    },
    4: {
        "top": (136, 211, 235), "highlight": (238, 251, 255),
        "soil": (79, 137, 168), "shadow": (48, 73, 104),
        "detail": (147, 220, 238), "accent": (169, 236, 255),
        "moving": (106, 192, 226),
    },
    5: {
        "top": (119, 102, 195), "highlight": (248, 211, 125),
        "soil": (67, 64, 115), "shadow": (37, 38, 75),
        "detail": (166, 117, 207), "accent": (205, 165, 255),
        "moving": (96, 174, 219),
    },
    6: {
        "top": (223, 151, 66), "highlight": (255, 218, 142),
        "soil": (159, 83, 59), "shadow": (82, 51, 60),
        "detail": (231, 178, 91), "accent": (255, 200, 104),
        "moving": (212, 127, 81),
    },
    7: {
        "top": (60, 181, 168), "highlight": (164, 250, 220),
        "soil": (59, 107, 126), "shadow": (36, 62, 83),
        "detail": (230, 128, 163), "accent": (117, 240, 222),
        "moving": (87, 204, 215),
    },
    8: {
        "top": (94, 119, 145), "highlight": (241, 194, 96),
        "soil": (67, 76, 94), "shadow": (36, 44, 61),
        "detail": (194, 143, 76), "accent": (255, 199, 92),
        "moving": (105, 151, 183),
    },
    9: {
        "top": (186, 221, 245), "highlight": (255, 255, 255),
        "soil": (119, 164, 198), "shadow": (66, 95, 133),
        "detail": (158, 208, 227), "accent": (174, 237, 232),
        "moving": (125, 191, 224),
    },
    10: {
        "top": (130, 91, 211), "highlight": (172, 239, 255),
        "soil": (72, 59, 130), "shadow": (38, 36, 81),
        "detail": (134, 105, 205), "accent": (138, 230, 255),
        "moving": (90, 177, 236),
    },
}
