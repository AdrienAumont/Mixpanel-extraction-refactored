import Extract
import pandas as pd
import Data_preProcessing as dapa
import copy
from Wellbeing_questionaire import KeyProperties
from Analysis import calc_stats


def main():
    """
    1. extracts and stores the requested event in the given date range if necessary
    2. parses the raw data in a list of clients
    3. writes the list of clients to a csv file with all their assessments
    4. analyses the values to give meaningful statistics on the requested time period
    5. writes the analysis to a csv file
    """
    Extract.fetch_and_store_data("Pelvic Assessment Passed", "2022-04-22", "2022-05-24", "raw_data")
    raw_data = Extract.get_data_from_file("raw_data", '2022-04-22', '2022-05-24')
    list_of_clients = dapa.parse_data(raw_data)
    pre_processed_data = to_list_of_dict(list_of_clients.copy())
    write_to_csv(pre_processed_data, 'output.csv')
    analysis = calc_stats(list_of_clients)
    analysis_list = dict_to_list_of_tuples(analysis)
    write_to_csv(analysis_list, 'analysis.csv')


def to_list_of_dict(original_list):
    """
    Transforms a list of clients into a list of dictionary for export to csv file
    :param original_list: list of clients
    :return: list of dict
    """
    list_of_clients = original_list.copy()
    data = []
    for client in list_of_clients:
        client_cpy = copy.deepcopy(client)
        single_row = {"UI/NON UI": client.ui}
        for i in range(len(client_cpy.quests)):
            if client_cpy.quests[i]:
                flat = client_cpy.quests[i].flatten()
                new_dict = {f"{key}_PA{i + 1}": value for key, value in flat.items()}
            else:
                new_dict = {f"{key.value}_PA{i + 1}": '' for key in KeyProperties}
            single_row.update(new_dict)
        data.append(single_row)
    return data


def dict_to_list_of_tuples(data):
    """
    Transforms a simple dict into a list of tuples for export to csv file
    :param data: dict of the analysis
    :return: list of tuples
    """
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")

    # Convert the dictionary to a list of tuples
    list_of_tuples = list(data.items())
    return list_of_tuples


def write_to_csv(pre_processed_data, name):
    """
    Uses panda to export the processed data to csv file
    :param pre_processed_data: list of dict or list of tuples...
    :param name: name of the file to export to
    """
    df = pd.DataFrame(pre_processed_data)
    # Write DataFrame to CSV
    df.to_csv(name, index=False)

    print("CSV file created successfully.", flush = True)


if __name__ == "__main__":
    main()