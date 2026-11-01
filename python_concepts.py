"""Short Python explanations shown by the in-game Python Coach."""

PYTHON_LESSONS = {
    "strings": {
        "title": "STRING  |  Text inside quotes",
        "message": (
            "This message is a string: Python text is written inside quotes. "
            "The game can display strings in its menus and hints."
        ),
    },
    "lists": {
        "title": "LIST + LOOP  |  Many coins, one check",
        "message": (
            "The stage stores its coins in a list. A for loop checks each "
            "Coin object and collects the one touching the player."
        ),
    },
    "variables": {
        "title": "VARIABLE  |  Remembering a value",
        "message": (
            "The score is stored in a variable. Collecting an item changes "
            "that value, and the HUD reads it to show your current score."
        ),
    },
    "conditionals": {
        "title": "IF + BOOLEAN  |  Make a decision",
        "message": (
            "The power-up has a collected True/False state. An if condition "
            "checks it so the same power-up cannot activate twice."
        ),
    },
    "tuples": {
        "title": "TUPLE  |  A position pair",
        "message": (
            "The checkpoint position is an (x, y) tuple. It keeps the two "
            "coordinates together so the player can respawn there."
        ),
    },
    "classes": {
        "title": "CLASS + OBJECT  |  Blueprint and character",
        "message": (
            "Enemy is a class blueprint. Each cat in the level is an object "
            "with its own position, direction, and health."
        ),
    },
    "inheritance": {
        "title": "INHERITANCE  |  Reuse and extend code",
        "message": (
            "Boss inherits from Enemy, so it reuses enemy movement. The Boss "
            "class adds its own health and stronger attacks."
        ),
    },
    "dictionaries": {
        "title": "DICTIONARY  |  Values with named keys",
        "message": (
            "A stage dictionary stores groups under keys such as 'coins', "
            "'enemies', and 'info'. The key tells the game what data to read."
        ),
    },
    "modules": {
        "title": "MODULE  |  Split a project into files",
        "message": (
            "game.py imports Player, UI, and stage builders from other files. "
            "Modules keep a larger Python project organised and reusable."
        ),
    },
}