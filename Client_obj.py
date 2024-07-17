import numbers
from typing import Callable, List
from Wellbeing_questionaire import Questionnaire as Quest
RANGES = [range(0, 6), range(40, 61), range(90, 121)]


class Client:
    def __init__(self, distinct_id: str, quests: List[Quest]):
        self.ui = ''
        self.distinct_id = distinct_id
        if not quests:
            self.quests = [None] * len(RANGES)
        else:
            self.quests = quests

    def get_num_key_at_i(self, key, i):
        if self.has_pa_i(i) and isinstance(self.quests[i].properties[key], numbers.Number):
            return self.quests[i].properties[key]

    def matches_predicate(self, predicate: Callable[['Client'], bool]):
        return predicate(self)

    def has_key_symptom_at_i(self, key, i):
        return (self.has_pa_i(i) and
                isinstance(self.quests[i].properties[key], numbers.Number) and
                self.quests[i].properties[key] != 0)

    def has_not_key_symptom_at_i(self, key, i):
        return (self.has_pa_i(i) and
                isinstance(self.quests[i].properties[key], numbers.Number) and
                self.quests[i].properties[key] == 0)

    def has_pa_i(self, i):
        return bool(self.quests[i])

    def has_dev_symptom(self, key, i):
        if self.has_pa_i(i):
            return self.quests[0].properties[key] == 0 and self.quests[i].properties[key] != 0
        else:
            return False

    def has_urge(self):
        return self.quests[0].properties['new_program_recommendation'] == 'Urgenturie'

    def has_stress(self):
        return self.quests[0].properties['new_program_recommendation'] == 'IncontinenceEffort'

    def has_mixed(self):
        return self.quests[0].properties['new_program_recommendation'] == 'MixedIncontinence'

    def delta_time_i(self, i):
        if self.has_pa_i(0) and self.has_pa_i(i):
            self.quests[i].properties['days_since_PA1'] = (self.quests[i].time - self.quests[0].time) / 86400000
            return self.quests[i].properties['days_since_PA1']

    def delta_pa_i(self, key, i):
        if self.has_pa_i(0) and self.has_pa_i(i):
            return self.quests[i].properties[key] - self.quests[0].properties[key]

    def got_better_at_i(self, key, i):
        return self.delta_pa_i(key, i) < 0 if isinstance(self.delta_pa_i(key, i), numbers.Number) else False

    def got_worse_at_i(self, key, i):
        return self.delta_pa_i(key, i) > 0 if isinstance(self.delta_pa_i(key, i), numbers.Number) else False

    def got_no_change_at_i(self, key, i):
        return self.delta_pa_i(key, i) == 0 if isinstance(self.delta_pa_i(key, i), numbers.Number) else False

    def got_cured_at_i(self, key, i):
        return self.has_key_symptom_at_i(key, i) and self.has_not_key_symptom_at_i(key, 0)
