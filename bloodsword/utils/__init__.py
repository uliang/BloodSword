import re
import random


def roll_dice(string_form: str = '', *, n: int = 0,
              d: int = 0, modifier: int = 0) -> int:
    if not any((string_form, n, d, modifier)):
        raise ValueError("No dice specified.")

    if all((n > 0, d > 0, modifier >= 0)):
        dice_faces = [i for i in range(1, n+1)]
        dice_rolls = random.choices(dice_faces, k=d)
        dice_total = sum(dice_rolls) + modifier
        return dice_total

    if (matched := re.match(r'(?P<n>\d+)?d(?P<d>\d+)\+?(?P<modifier>\d+)?',
                            string_form) if string_form else None) is None:
        raise ValueError("Incorrect dice specification.")

    n = int(matched.group(1)) if matched.group(1) else 1
    d = int(matched.group(2))
    modifier = int(matched.group(3)) if matched.group(3) else 0

    return roll_dice(n=n, d=d, modifier=modifier)
