from mixpanel_utils import MixpanelUtils
from Client_obj import Client
from Wellbeing_questionaire import Questionnaire, KeyProperties
from Client_obj import RANGES
client_dict = {}


def parse_data(dataframe):
    """
    Transform raw data exported from Mixpanel into a list of unique Clients each with their own list of Questionnaires.
    :param dataframe: DataFrame containing the raw data
    :return: list of unique clients
    """
    print('processing rows')
    # Apply the process_row function to each row
    dataframe.apply(process_row, axis=1)
    print('done')
    client_list = list(filter(lambda user: user.has_pa_i(0), client_dict.values()))

    for client in client_list:
        client.ui = "UI" if client.has_key_symptom_at_i('medical_score', 0) else "NON UI"

    return client_list


def identify_quest_and_update_client(quest: Questionnaire, client: Client):
    """
    Identifies the number of the questionnaire and updates the client list of questionnaire if necessary
    :param quest: the questionnaire to analyse
    :param client: the client that took the questionnaire
    """
    game_sessions = quest.properties.get('total_game_sessions', 0)
    for i in range(len(RANGES)):
        needs_replace = client.quests[i] is None or client.quests[i].properties['total_game_sessions'] < quest.properties['total_game_sessions']
        if game_sessions in RANGES[i] and needs_replace:
            client.quests[i] = quest
            if i >= 1 and client.quests[0]:
                client.delta_time_i(i)


def process_row(row):
    """
    Process a single row to create or update a client with the questionnaire information.
    """
    distinct_id = row['distinct_id']
    if distinct_id not in client_dict:
        client = Client(distinct_id, [])
    else:
        client = client_dict[distinct_id]

    new_quest = parse_quest(row)
    new_quest.reduce_properties()
    identify_quest_and_update_client(new_quest, client)

    client_dict[client.distinct_id] = client


def parse_quest(one_line_data: dict):
    """
    Takes one line of raw data and creates a questionnaire from it using the enumeration given in
    "Wellbeing_questionnaire.py"
    :param one_line_data: one line of raw data
    :return: a parsed Questionnaire with all corresponding properties
    """
    new_properties = {}
    for key in KeyProperties:
        if key.value in one_line_data:
            new_properties[key.value] = one_line_data[key.value]
    return Questionnaire(one_line_data['distinct_id'], one_line_data['time'], new_properties)


