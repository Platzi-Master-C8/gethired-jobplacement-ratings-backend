import random
import functools
import operator

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

    def assign_weight(companion_evaluation_criteria: str) -> int:
        """Return the convertion of a string company evaluation in it's equivalent to a weight

        Args:
            companion_evaluation_criteria (str): Criteria of of the company evaluation to be evaluated

        Returns:
            int: Weight assigned
        """
        weight_assigned = 0

        if companion_evaluation_criteria == "Good":
            weight_assigned = 5
        elif companion_evaluation_criteria == "Regular":
            weight_assigned = 3
        elif companion_evaluation_criteria == "Bad":
            weight_assigned = 1

        return weight_assigned

    def round_values(amount, number_of_decimals=1):
        result = round(amount, number_of_decimals)
        return result

    def tranform_tuple_in_string(tuple: tuple) -> str:
        """Tansforma  tuple in a string

        Args:
            tuple (tuple): A tuple

        Returns:
            str: the tuple converted into string
        """
        return functools.reduce(operator.add, (tuple))
