from mixpanel_utils import MixpanelUtils
from Client_obj import Client
from Wellbeing_questionaire import Questionnaire, KeyProperties
from Client_obj import RANGES


# input : raw data from mixpanel
# output : dict of clients

def parse_data(data):
    client_dict = {}
    for i in range(len(data)):
        if not data[i].get('distinct_id') in client_dict:
            client = Client(data[i].get('distinct_id'), [])
        else:
            client = client_dict[data[i]['distinct_id']]
        new_quest = parse_quest(data[i])
        new_quest.reduce_properties()
        identify_quest_and_update_client(new_quest, client)
        client_dict[client.distinct_id] = client
    return client_dict


def identify_quest_and_update_client(quest: Questionnaire, client: Client):
    game_sessions = quest.properties.get('total_game_sessions', 0)
    for i in range(len(RANGES)):
        needs_replace = client.quests[i] is None or client.quests[i].properties['total_game_sessions'] < quest.properties['total_game_sessions']
        if game_sessions in RANGES[i] and needs_replace:
            client.quests[i] = quest
            if i > 1 and client.quests[0]:
                client.delta_time_i(i)


def parse_quest(one_line_data: dict):
    new_properties = {}
    for key in KeyProperties:
        if key.value in one_line_data['properties']:
            new_properties[key.value] = one_line_data['properties'][key.value]
    return Questionnaire(one_line_data['name'], one_line_data['distinct_id'], one_line_data['time'], new_properties)


