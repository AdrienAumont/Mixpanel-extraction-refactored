import Extract
import pandas as pd
import Data_preProcessing as dapa
from Wellbeing_questionaire import KeyProperties


def main():
    Extract.fetch_and_store_data("Pelvic Assessment Passed", "2022-04-22", "2022-04-22", "raw_data")
    raw_data = Extract.get_data_from_file("raw_data", '2022-04-22', '2022-04-22')
    pre_processed_data = to_list_of_dict(raw_data)
    write_to_csv(pre_processed_data)


def to_list_of_dict(raw_data):
    client_dict = dapa.parse_data(raw_data)
    list_of_clients = client_dict.values()
    data = []
    for client in list_of_clients:
        single_row = {}
        for i in range(len(client.quests)):
            if client.quests[i]:
                flat = client.quests[i].flatten()
                new_dict = {f"{key}_PA{i + 1}": value for key, value in flat.items()}
            else:
                new_dict = {f"{key.value}_PA{i + 1}": '' for key in KeyProperties}
            single_row.update(new_dict)
        data.append(single_row)
    return data


def write_to_csv(pre_processed_data):
    df = pd.DataFrame(pre_processed_data)
    # Write DataFrame to CSV
    df.to_csv('output.csv', index=False)

    print("CSV file created successfully.")


if __name__ == "__main__":
    main()