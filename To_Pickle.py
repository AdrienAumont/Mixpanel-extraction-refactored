import json
import pandas as pd


def process_json_entry(entry, all_keys):
    properties = entry.get('properties', {})
    flat_entry = {**entry, **properties}
    flat_entry.pop('properties', None)  # Ensure properties key is removed
    # Ensure all keys are present
    for key in all_keys:
        if key not in flat_entry:
            flat_entry[key] = 'undefined'
    return flat_entry

def load_json_data(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def transform_data(data):
    # Collect all possible keys
    all_keys = set()
    for entry in data:
        all_keys.update(entry.keys())
        if 'properties' in entry:
            all_keys.update(entry['properties'].keys())
    # Process entries ensuring all keys are present
    processed_data = [process_json_entry(entry, all_keys) for entry in data]
    df = pd.DataFrame(processed_data)
    return df


# # Assuming your JSON file is named 'data.json'
# json_file_path = 'raw_data.json'
# pickle_file_path = 'dataframe.pkl'
#
# # Load JSON data
# data = load_json_data(json_file_path)
#
# # Transform data to structured format
# dataframe = transform_data(data)
#
# # Save dataframe to pickle file
# dataframe.to_pickle(pickle_file_path)
