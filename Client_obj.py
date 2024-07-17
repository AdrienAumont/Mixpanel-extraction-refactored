import numbers
from typing import Callable, List
from Wellbeing_questionaire import Questionnaire as Quest
# this is the list of ranges that define the ranges of games played for PA1, PA2 ...
RANGES = [range(0, 6), range(40, 61), range(90, 121)]


class Client:
    """
    This is a class to represent a client/user

    Parameters:
    distinct_id (str): unique ID corresponding to the client.
    quests (list[Questionnaire]): All the Wellness assessment taken by the client,
        index indicates the number of the assessment, None if the assessment was not extracted
    """
    def __init__(self, distinct_id: str, quests: List[Quest]):
        self.ui = ''
        self.distinct_id = distinct_id
        if not quests:
            self.quests = [None] * len(RANGES)
        else:
            self.quests = quests

    def get_num_key_at_i(self, key, i):
        """
        Gets a numerical value in the indicated questionnaire.

        Parameters:
        key (str): The property to be accessed.
        i (int): The index where you want the property to be taken.

        :returns:
        number.Number :  the value found for the property.
        nothing : if the questionnaire does not exist or the value is not numerical
        """
        if self.has_pa_i(i) and isinstance(self.quests[i].properties[key], numbers.Number):
            return self.quests[i].properties[key]

    def matches_predicate(self, predicate: Callable[['Client'], bool]):
        """
        Check if the client matches the given predicate

        Parameters:
        predicate (<class 'function'>) : a function from client => bool

        :returns:
        bool :  does it match?
        """
        return predicate(self)

    def has_key_symptom_at_i(self, key, i):
        """
        checks if the value of the key in the ith questionnaire is none zero which usually indicates the presence
        of a symptom.
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions

        Parameters:
        key (str): The property to be accessed.
        i (int): The index where you want the property to be taken.

        :returns:
        bool: does the client present the symptom while having the requested property and questionnaire
        """
        return (self.has_pa_i(i) and
                isinstance(self.quests[i].properties[key], numbers.Number) and
                self.quests[i].properties[key] != 0)

    def has_not_key_symptom_at_i(self, key, i):
        """
        checks if the value of the key in the ith questionnaire is zero which usually indicates the absence
        of a symptom.
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions

        Parameters:
        key (str): The property to be accessed.
        i (int): The index where you want the property to be taken.

        :returns:
        bool: does the client not have the symptom while having the requested property and questionnaire
        """
        return (self.has_pa_i(i) and
                isinstance(self.quests[i].properties[key], numbers.Number) and
                self.quests[i].properties[key] == 0)

    def has_pa_i(self, i):
        """
        checks if the client has the requested questionnaire
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions

        Parameters:
        i (int): The index of the questionnaire to check.

        :returns:
        bool: does the client have the requested questionnaire
        """
        return bool(self.quests[i])

    def has_dev_symptom(self, key, i):
        """
        checks if the client has developped the asked symptom since his first wellness assessment
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions

        Parameters:
        key (str): The property to be accessed.
        i (int): The index where you want the property to be taken.

        :returns:
        bool: did he develop the symptom since his first assessment
        """
        if self.has_pa_i(i):
            return self.quests[0].properties[key] == 0 and self.quests[i].properties[key] != 0
        else:
            return False

    def has_urge(self):
        """
        does the client have urge type of UI symptom
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :return:
        bool : does the client have urge at the time of his first assessment
        """
        return self.quests[0].properties['new_program_recommendation'] == 'Urgenturie'

    def has_stress(self):
        """
        does the client have stress type of UI symptom
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :return:
        bool : does the client have stress at the time of his first assessment
        """
        return self.quests[0].properties['new_program_recommendation'] == 'IncontinenceEffort'

    def has_mixed(self):
        """
        does the client have both urge and stress type of UI symptom
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :return:
        bool : does the client have urge and stress at the time of his first assessment
        """
        return self.quests[0].properties['new_program_recommendation'] == 'MixedIncontinence'

    def delta_time_i(self, i):
        """
        finds the time since the first assessment in days
        This function is meant to be used as lambda for mean calculation or other client => Number requesting functions
        :param i: int : from what assessment
        :return: float : the time between assessment in days
        """
        if self.has_pa_i(0) and self.has_pa_i(i):
            self.quests[i].properties['days_since_PA1'] = (self.quests[i].time - self.quests[0].time) / 86400000
            return self.quests[i].properties['days_since_PA1']

    def delta_pa_i(self, key, i):
        """
        finds the difference (usually in symptoms) between the requested assessment and the first
        This function is meant to be used as lambda for mean calculation or other client => Number requesting functions
        :param key : str : The property to be accessed.
        :param i : int : The index where you want the property to be taken.
        :returns: Number: the difference in between requested assessment and first
        """
        if self.has_pa_i(0) and self.has_pa_i(i):
            return self.quests[i].properties[key] - self.quests[0].properties[key]

    def got_better_at_i(self, key, i):
        """
        determines whether a client has improved in a certain symptome/score since his first assessment
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :param key: : str : The property to be accessed.
        :param i:  int : The index where you want the property to be taken.
        :return: bool: did client get better or not
        """
        return self.delta_pa_i(key, i) < 0 if isinstance(self.delta_pa_i(key, i), numbers.Number) else False

    def got_worse_at_i(self, key, i):
        """
        determines whether a client has gotten worse in a certain symptome/score since his first assessment
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :param key: : str : The property to be accessed.
        :param i:  int : The index where you want the property to be taken.
        :return: bool: did client get worse or not
        """
        return self.delta_pa_i(key, i) > 0 if isinstance(self.delta_pa_i(key, i), numbers.Number) else False

    def got_no_change_at_i(self, key, i):
        """
        determines whether a client has seen no change in a certain symptome/score since his first assessment
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :param key: : str : The property to be accessed.
        :param i:  int : The index where you want the property to be taken.
        :return: bool: did client see no change or not
        """
        return self.delta_pa_i(key, i) == 0 if isinstance(self.delta_pa_i(key, i), numbers.Number) else False

    def got_cured_at_i(self, key, i):
        """
        determines whether a client has gotten cured of a certain symptome/score since his first assessment
        This function is meant to be used as lambda for matches predicate or other client => bool requesting functions
        :param key: : str : The property to be accessed.
        :param i:  int : The index where you want the property to be taken.
        :return: bool: did client get cured or not
        """
        return self.has_key_symptom_at_i(key, i) and self.has_not_key_symptom_at_i(key, 0)
