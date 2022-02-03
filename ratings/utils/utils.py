import random
from typing import List


class Util:
    def create_tracking_code() -> str:
        MAYUS = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "X",
            "Y",
            "Z",
        ]

        NUMS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        characters = MAYUS + NUMS

        tracking_code: List = []

        for i in range(8):
            random_character = random.choice(characters)
            tracking_code.append(random_character)

        tracking_code = "".join(tracking_code)

        return tracking_code
