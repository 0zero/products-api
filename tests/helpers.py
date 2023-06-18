import random
import string


def get_random_string(length: int = 10) -> str:
    """
    Generate a random string of fixed length

    Keyword arguments:
    length -- The length of the string to return (default 10)
    Return: random string of length
    """

    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))
