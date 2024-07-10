
from enum import Enum


# this enumeration is used to select what properties to extract from mixpanel
class KeyProperties(Enum):
    DISTINCT_ID = "distinct_id"
    TOTAL_GAME_SESSIONS = "total_game_sessions"
    MEDICAL_BIRTH = "medical_birth"
    WELLBEING_QUESTIONNAIRE_SCORE = "wellbeing_questionnaire_score"
    SUBJECTIVE = "subjective"
    SUBJECTIVE_SCORE = "subjective_score"
    TOTAL_KEGEL_COACH_SESSIONS = "total_kegel_coach_sessions"
    TOTAL_KEGEL_COACH_SESSIONS_LENGTH = "total_kegel_coach_sessions_length"
    KEGEL_COACH_DONE = "kegel_coach_done"
    TOTAL_GAME_SESSIONS_LENGTH = "total_game_sessions_length"
    TOTAL_PRACTICE_SESSIONS_3D_LENGTH = "total_practice_sessions_3d_length"
    TOTAL_PRACTICE_SESSIONS_DOTS_LENGTH = "total_practice_sessions_dots_length"
    TRAINING_FREQUENCY = "training_frequency"
    TRAINING_FREQUENCY_LEVEL = "training_frequency_level"
    TRAINING_QUALITY = "training_quality"
    STRENGTH_GOAL = "strength_goal"
    KPI_AGILITY = "kpi_agility"
    KPI_ENDURANCE = "kpi_endurance"
    KPI_RELAXATION = "kpi_relaxation"
    KPI_STRENGTH = "kpi_strength"
    KPI_CONTRACTION_QUALITY = "kpi_contraction_quality"
    LAST_PROGRAM_RECOMMENDATION = "last_program_recommendation"
    NEW_PROGRAM_RECOMMENDATION = "new_program_recommendation"
    PROGRAM_SELECTED = "program_selected"
    MEDICAL_LIFE_1 = "medical_life_1"
    MEDICAL_LIFE_2 = "medical_life_2"
    MEDICAL_STRESS_1 = "medical_stress_1"
    MEDICAL_STRESS_2 = "medical_stress_2"
    MEDICAL_STRESS_3 = "medical_stress_3"
    MEDICAL_STRESS_4 = "medical_stress_4"
    MEDICAL_URGE_1 = "medical_urge_1"
    MEDICAL_URGE_2 = "medical_urge_2"
    MEDICAL_URGE_3 = "medical_urge_3"
    MEDICAL_URGE_4 = "medical_urge_4"
    MEDICAL_URGE_5 = "medical_urge_5"
    MEDICAL_URGE_6 = "medical_urge_6"
    MEDICAL_URGE_7 = "medical_urge_7"
    TOTAL_PRACTICE_SESSIONS = "total_practice_sessions"
    TOTAL_PRACTICE_SESSIONS_LENGTH = "total_practice_sessions_length"
    APP_VERSION = "app_version"
    TIME = "time"
    ACTIVITY_FREQUENCY = "activity_frequency"
    ACTIVITY_IMPACT = "activity_impact"
    ACTIVITY_INTENSITY = "activity_intensity"
    BODY_WEIGHT = "body_weight"
    CONTRACTION_QUALITY_7D_LEVEL = "contraction_quality_7D_level"
    CURRENT_GAME_SESSIONS_LENGTH = "current_game_sessions_length"
    GOALS_DAY = "goals_day"
    GOALS_WEEK = "goals_week"
    MEDICAL_OTHER = "medical_other"
    MEDICAL_OTHER_DESCRIPTION = "medical_other_description"
    MEDICAL_PROLAPSE_1 = "medical_prolapse_1"
    MEDICAL_PROLAPSE_2 = "medical_prolapse_2"
    MEDICAL_PROLAPSE_3 = "medical_prolapse_3"
    MEDICAL_PROLAPSE_4 = "medical_prolapse_4"
    MENSTRUAL_STATUS = "menstrual_status"
    SEXUALITY_1 = "sexuality_1"
    SEXUALITY_2 = "sexuality_2"
    SEXUALITY_3 = "sexuality_3"
    SEXUALITY_4 = "sexuality_4"
    YEAR_OF_BIRTH = "year_of_birth"
    STRESS_INCONTINENCE_B = "stress_incontinence_b"
    MEDICAL_STRESS_LIFE_1 = "medical_stress_life_1"
    MEDICAL_STRESS_LIFE_2 = "medical_stress_life_2"
    MEDICAL_STRESS_LIFE_3 = "medical_stress_life_3"
    MEDICAL_LIFE_SCORE = "medical_life_score"
    MEDICAL_STRESS_SCORE = "medical_stress_score"
    MEDICAL_URGE_SCORE = "medical_urge_score"
    MEDICAL_PROLAPSE_SCORE = "medical_prolapse_score"
    PROLAPSE_KNOWN = "prolapse_known"
    SCORE_MIXED_INCONTINENCE = "score_mixed_incontinence"
    SCORE_POSTPARTUM = "score_postpartum"
    SCORE_PREVENT_DISORDER = "score_prevent_disorder"
    SCORE_PROLAPSE = "score_prolapse"
    SCORE_SEXO = "score_sexo"
    SCORE_STRESS_INCONTINENCE = "score_stress_incontinence"
    SCORE_URGE_INCONTINENCE = "score_urge_incontinence"


class Questionnaire:
    def __init__(self,
                 name: str = 'Pelvic Assessment Passed',
                 distinct_id: str = '',
                 labels: list = None,
                 time: int = 0,
                 sampling_factor: int = 1,
                 dataset: str = '$mixpanel',
                 properties: dict = None):

        self.name = name
        self.distinct_id = distinct_id
        self.labels = labels if labels is not None else []
        self.time = time
        self.sampling_factor = sampling_factor
        self.dataset = dataset
        self.properties = properties if properties else {}

        # Define default values for properties based on previous code
        self.properties.setdefault('total_kegel_coach_sessions', 0)
        self.properties.setdefault('total_kegel_coach_sessions_length', 0)
        self.properties.setdefault('total_practice_sessions_3d_length', 0)
        self.properties.setdefault('total_practice_sessions_dots_length', 0)
        self.properties.setdefault('medical_urge_score', '')
        self.properties.setdefault('medical_stress_score', '')
        self.properties.setdefault('stress_incontinence_b', '')
        self.properties.setdefault('medical_prolapse_score', '')
        self.properties.setdefault('medical_life_score', '')
        self.properties.setdefault('wellbeing_questionnaire_score', '')
        self.properties.setdefault('subjective', 0)
        self.properties.setdefault('subjective_score', '')
        self.properties.setdefault('training_frequency', '')
        self.properties.setdefault('training_frequency_level', '')
        self.properties.setdefault('training_quality', '')
        self.properties.setdefault('strength_goal', '')
        self.properties.setdefault('activity_frequency', '')
        self.properties.setdefault('activity_impact', '')
        self.properties.setdefault('activity_intensity', '')
        self.properties.setdefault('body_weight', '')
        self.properties.setdefault('contraction_quality_7D_level', '')
        self.properties.setdefault('medical_prolapse_1', 0)
        self.properties.setdefault('medical_prolapse_2', 0)
        self.properties.setdefault('medical_prolapse_3', 0)
        self.properties.setdefault('medical_prolapse_4', 0)
        self.properties.setdefault('menstrual_status', '')
        self.properties.setdefault('sexuality_1', 'undefined')
        self.properties.setdefault('sexuality_2', 'undefined')
        self.properties.setdefault('sexuality_3', 'undefined')
        self.properties.setdefault('sexuality_4', 'undefined')
        self.properties.setdefault('year_of_birth', '')
        self.properties.setdefault('medical_other', '')
        self.properties.setdefault('medical_other_description', '')
        self.properties.setdefault('current_game_sessions_length', '')
        self.properties.setdefault('medical_stress_1', 0)
        self.properties.setdefault('medical_stress_2', 0)
        self.properties.setdefault('medical_stress_3', 0)
        self.properties.setdefault('medical_stress_4', 0)
        self.properties.setdefault('medical_urge_1', 0)
        self.properties.setdefault('medical_urge_2', 0)
        self.properties.setdefault('medical_urge_3', 0)
        self.properties.setdefault('medical_urge_4', 0)
        self.properties.setdefault('medical_urge_5', 0)
        self.properties.setdefault('medical_urge_6', 0)
        self.properties.setdefault('medical_urge_7', 0)
        self.properties.setdefault('medical_life_1', '')
        self.properties.setdefault('medical_life_2', '')
        self.properties.setdefault('medical_stress_life_1', '')
        self.properties.setdefault('medical_stress_life_2', '')
        self.properties.setdefault('medical_stress_life_3', '')
        self.properties.setdefault('score_prolapse', '')
        self.properties.setdefault('goals_day', '')
        self.properties.setdefault('goals_week', '')
        self.properties.setdefault('score_mixed_incontinence', '')
        self.properties.setdefault('score_postpartum', '')
        self.properties.setdefault('score_prevent_disorder', '')
        self.properties.setdefault('score_prolapse', '')
        self.properties.setdefault('score_sexo', '')
        self.properties.setdefault('score_stress_incontinence', '')
        self.properties.setdefault('score_urge_incontinence', '')
        self.properties.setdefault('kpi_agility', '')
        self.properties.setdefault('kpi_endurance', '')
        self.properties.setdefault('kpi_agility', '')
        self.properties.setdefault('kpi_relaxation', '')
        self.properties.setdefault('kpi_strength', '')
        self.properties.setdefault('kpi_contraction_quality', '')

    def to_dict(self):
        return {
            'name': self.name,
            'distinct_id': self.distinct_id,
            'labels': self.labels,
            'time': self.time,
            'sampling_factor': self.sampling_factor,
            'dataset': self.dataset,
            'properties': self.properties
        }

    def undef_to_default(self):
        for key, value in self.properties.items():
            if value == 'undefined':
                self.properties[key] = 0

    def reduce_properties(self):
        self.undef_to_default()
        self.properties['medical_score'] = (
                self.properties['medical_urge_1'] + self.properties['medical_urge_2'] + self.properties['medical_urge_3']
                + self.properties['medical_urge_4'] + self.properties['medical_urge_5'] + self.properties[
                    'medical_urge_6']
                + self.properties['medical_urge_7'] + self.properties['medical_stress_1'] + self.properties[
                    'medical_stress_2']
                + self.properties['medical_stress_3'] + self.properties['medical_stress_4'])
        self.properties['medical_urge_result'] = (
                self.properties['medical_urge_1'] + self.properties['medical_urge_2'] + self.properties['medical_urge_3']
                + self.properties['medical_urge_4'] + self.properties['medical_urge_5']
                + self.properties['medical_urge_6'] + self.properties['medical_urge_7'])
        self.properties['medical_life_result'] = self.properties['medical_life_1'] + self.properties[
            'medical_life_2']
        self.properties['medical_prolapse_symptoms'] = (
                self.properties['medical_prolapse_1'] + self.properties['medical_prolapse_2']
                + self.properties['medical_prolapse_3'])
        self.properties['sex_result'] = self.calc_sex_result()

    def calc_sex_result(self):
        if self.properties['sexuality_1'] == 'undefined':
            sex_score = 'undefined'
        else:
            if self.properties['sexuality_2'] == 'undefined':
                sex_2_answer = 0
                sex_2_value = 0
            else:
                sex_2_answer = 1
                sex_2_value = self.properties['sexuality_2']
            if self.properties['sexuality_3'] == 'undefined':
                sex_3_answer = 0
                sex_3_value = 0
            else:
                sex_3_answer = 1
                sex_3_value = self.properties['sexuality_3']

            sex_score = (1 - (
                    self.properties['sexuality_1'] + sex_2_value + sex_3_value + self.properties['sexuality_4'])
                         / (6 + sex_2_answer * 3 + sex_3_answer * 3))
        return sex_score
