from mixpanel_utils import MixpanelUtils
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
import To_Pickle
API_SECRET = 'e0d9beac86a83795e8e7bd8608ae9e1b'
API = "64dbf22bfc3728f730b4895b62573650"


def get_date_ranges(dates):
    """
    from a list of dates computes the largest ranges of dates possible to cover the whole list
    :param dates : list[dates] : list of missing dates
    :return: list of ranges of dates
    """
    if not dates:
        return []

    ranges = []
    start_date = dates[0]
    prev_date = dates[0]

    for date in dates[1:]:
        if date != prev_date + timedelta(days=1):
            ranges.append((start_date, prev_date))
            start_date = date
        prev_date = date

    ranges.append((start_date, prev_date))
    return ranges


def fetch_and_store_data(event_name, start_date_str, end_date_str, file_name):
    """
    imports from mixpanel the given event data from the given names into a file with the given name
    :param event_name : str: name of the mixpanel event
    :param start_date_str: str: import from this date
    :param end_date_str: str: import to this date
    :param file_name: str: where to save raw data
    """
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    print("getting dates")
    existing_dates = get_existing_dates(file_name)
    print("got dates")
    missing_dates = get_missing_dates(start_date, end_date, existing_dates)

    if not missing_dates:
        print("Data for the requested date range is already imported.")
        return

    # Sort the missing dates to find continuous ranges
    missing_dates = sorted(missing_dates)
    date_ranges = get_date_ranges(missing_dates)

    for start, end in date_ranges:
        new_data = get_mixpanel_data(event_name, start, end)
        append_data_to_file(new_data, file_name)
    print("Data has been fetched and stored successfully.")


def get_mixpanel_data(event_name, start_date, end_date):
    """
    uses mix panel api to export from the website
    :param event_name: the event to export
    :param start_date: export from this date
    :param end_date: export from this date
    :return: the imported data
    """
    mputils = MixpanelUtils(API_SECRET, token=API)

    query = '''function main() {
                            return Events({
                                from_date: '%s',
                                to_date: '%s',
                                event_selectors:[{event:'%s'}]})
                                .sortAsc('distinct_id');}''' % (start_date, end_date, event_name)
    # then pass it to the function
    data = mputils.query_jql(query)
    return data


def parse_mixpanel_time(timestamp):
    """
    transform a timestamp into a datetime object
    :param timestamp: int : timestamp
    :return: datetime object
    """
    try:
        # Convert milliseconds to seconds (required by datetime.fromtimestamp)
        timestamp_sec = timestamp / 1000.0

        # Convert timestamp to datetime object
        dt_object = datetime.fromtimestamp(timestamp_sec)

        return dt_object
    except ValueError:
        return None  # Handle invalid timestamps gracefully if needed


def store_data_to_file(data, file_name):
    """
    store given data in a file with given name
    :param data: data to store
    :param file_name: str: name of the created file
    """
    with open(file_name, 'w') as f:
        json.dump(data, f)


def get_existing_dates(file_name):
    """
    Get all already imported date from the raw data
    :param file_name: str: the name of the file containing the raw data
    :return: set of already imported dates
    """
    try:
        print("reading")
        dataframe = pd.read_pickle(file_name)
        print("read dates")
        date_list = dataframe['time'].apply(lambda x: parse_mixpanel_time(x).date()).tolist()
        return set(date_list)
    except FileNotFoundError:
        return set()


def get_missing_dates(start_date, end_date, existing_dates):
    """
    Get all dates that are still to be imported
    :param start_date: datetime obj: start of the date range
    :param end_date: datetime obj: end of the date range
    :param existing_dates: set(datetime obj): the set of already imported dates
    :return: a list of the dates that are yet to be imported
    """
    requested_dates = pd.date_range(start=start_date, end=end_date).tolist()
    requested_dates = [date.date() for date in requested_dates]
    existing_dates_set = set(existing_dates)
    return [date for date in requested_dates if date not in existing_dates_set]


def append_data_to_file(new_data, file_name):
    """
    appends data at the end of a file, used when adding data to raw data
    :param new_data: the raw data to append
    :param file_name: str: the name of the file
    """
    try:
        raw_dataframe = pd.read_pickle(file_name)
        new_dataframe = To_Pickle.transform_data(new_data)
        raw_dataframe.append(new_dataframe, ignore_index=True)
    except FileNotFoundError:
        store_data_to_file(new_data, file_name)


def get_data_from_file(file_name, start_date, end_date):
    """
    Gets data from the given file from a certain date to a certain date.
    :param file_name: str: the name of the file
    :param start_date: str: the start of the date range
    :param end_date: str: the end of the date range
    :return: DataFrame: the data obtained from the file within the date range
    """
    try:
        print("reading")
        # Load the DataFrame from the pickle file
        dataframe = pd.read_pickle(file_name)
        print("done")

        # Convert string dates to datetime objects for comparison
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # Convert 'time' column to datetime if it's not already in datetime format
        if not pd.api.types.is_datetime64_any_dtype(dataframe['time']):
            dataframe['time'] = pd.to_datetime(dataframe['time'], unit='ms')

        # Filter the DataFrame based on the date range
        filtered_data = dataframe[
            (dataframe['time'] >= start_date_obj) &
            (dataframe['time'] <= end_date_obj)
            ]

        print("data got gotten")
        return filtered_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



