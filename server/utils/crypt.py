import random

SYS_RANDOM = random.SystemRandom()


def gen_token(length: int):
    return "".join(
        SYS_RANDOM.choice(
            "abcdefghilkmnopqrstuvwxyzABCDEFGHILKMNOPQRSTUVWXYZ1234567890_-+"
        )
        for _ in range(length)
    )
