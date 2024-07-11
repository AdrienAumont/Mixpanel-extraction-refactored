from dataclasses import dataclass
from typing import List
from Wellbeing_questionaire import Questionnaire as Quest
RANGES = [range(0, 6), range(40, 61), range(90, 121)]


class Client:
    def __init__(self, distinct_id: str, quests: List[Quest]):
        self.distinct_id = distinct_id
        if quests:
            self.quests = quests
        else:
            self.quests = [None]*len(RANGES)

