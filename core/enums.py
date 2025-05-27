import random
from enum import Enum


class GoodJobMessage(Enum):
    GREAT = "대단하다 삐!"
    AWESOME = "엄청나다 삐!"
    CRAZY = "미쳤다 삐!"
    REST = "이제 좀 쉬어라 삐!"
    LOVE = "반했다 삐!"
    WOW = "감탄했다 삐!"

    @classmethod
    def random(cls):
        return random.choice(list(cls)).value
