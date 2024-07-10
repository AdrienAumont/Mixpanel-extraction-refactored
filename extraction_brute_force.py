from mixpanel_utils import MixpanelUtils
from Client_obj import Client
from Wellbeing_questionaire import Questionnaire, KeyProperties
from Client_obj import RANGES


def load_period(from_date, to_date):
    mputils = MixpanelUtils('e0d9beac86a83795e8e7bd8608ae9e1b', token="64dbf22bfc3728f730b4895b62573650")
    selector = 'defined (properties["$firmware"])'
    parameters = {'selector': selector}

    query = '''function main() {
                        return Events({
                            from_date: '%s',
                            to_date: '%s',
                            event_selectors:[{event:'Pelvic Assessment Passed'}]})
                            .sortAsc('distinct_id');}''' % (from_date, to_date)
    # then pass it to the function
    results = mputils.query_jql(query)
    return results


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
    game_sessions = quest.properties['total_game_sessions']
    for i in range(len(RANGES)):
        needs_replace = client.quests[i] is None or client.quests[i].properties['total_game_sessions'] < quest.properties['total_game_sessions']
        if game_sessions in RANGES[i] and needs_replace:
            client.quests[i] = quest
            if i > 1 and client.quests[0]:
                client.quests[i].properties['days_since_PA1'] = (client.quests[i].time - client.quests[0].time) / 86400


def parse_quest(one_line_data: dict):
    new_properties = {}
    for key in KeyProperties:
        if key.value in one_line_data['properties']:
            new_properties[key.value] = one_line_data['properties'][key.value]
    return Questionnaire(one_line_data['name'], one_line_data['distinct_id'],
                         one_line_data['labels'], one_line_data['time'],
                         one_line_data['sampling_factor'], one_line_data['dataset'], new_properties)


# print(load_period("2022-07-22", "2022-07-22")[0])
raw_data = load_period("2024-07-09", "2024-07-09")
client_dict = parse_data(raw_data)
print(len(client_dict))
