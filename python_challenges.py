"""Short Python questions asked at the end of each world."""

PYTHON_CHALLENGES = {
    1: {
        "topic": "Strings",
        "question": 'What does len("cat") return?',
        "choices": ["1", "3", "cat"],
        "answer": 2,
        "hint": "len() counts how many characters are in the text.",
        "explanation": '"cat" has three characters: c, a, and t.',
    },
    2: {
        "topic": "Lists",
        "question": 'What is ["red", "blue"][1]?',
        "choices": ["red", "blue", "1"],
        "answer": 2,
        "hint": "Python list positions start at 0.",
        "explanation": "Position 0 is red; position 1 is blue.",
    },
    3: {
        "topic": "Loops",
        "question": "What values does range(3) produce?",
        "choices": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3"],
        "answer": 2,
        "hint": "range(n) starts at 0 and stops before n.",
        "explanation": "range(3) produces 0, 1, and 2.",
    },
    4: {
        "topic": "Dictionaries",
        "question": 'What is {"coins": 5}["coins"]?',
        "choices": ["coins", "5", "coins: 5"],
        "answer": 2,
        "hint": "A dictionary key retrieves its matching value.",
        "explanation": "The key coins has the value 5.",
    },
    5: {
        "topic": "Inheritance",
        "question": "What does inheritance let a class do?",
        "choices": [
            "Reuse features from another class",
            "Turn a number into text",
            "Repeat a loop forever",
        ],
        "answer": 1,
        "hint": "In this game, Boss inherits from Enemy.",
        "explanation": "Boss reuses Enemy behavior and adds boss-specific features.",
    },
}