from string import ascii_lowercase
from itertools import product as cartesian_product

def alpha_enum():
    letters = list(ascii_lowercase)
    digits = 1
    while True:
        for i in cartesian_product(*[letters for _ in range(digits)]):
            yield "".join(i)
        digits += 1
