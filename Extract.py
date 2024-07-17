from mixpanel_utils import MixpanelUtils
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
API_SECRET = 'e0d9beac86a83795e8e7bd8608ae9e1b'
API = MixpanelUtils(API_SECRET)


def get_date_ranges(dates):
    """Given a sorted list of dates, find all continuous ranges."""
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
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    existing_dates = get_existing_dates(file_name)
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
    mputils = MixpanelUtils('e0d9beac86a83795e8e7bd8608ae9e1b', token="64dbf22bfc3728f730b4895b62573650")

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
    try:
        # Convert milliseconds to seconds (required by datetime.fromtimestamp)
        timestamp_sec = timestamp / 1000.0

        # Convert timestamp to datetime object
        dt_object = datetime.fromtimestamp(timestamp_sec)

        return dt_object
    except ValueError:
        return None  # Handle invalid timestamps gracefully if needed


def store_data_to_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f)


def get_existing_dates(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            existing_dates = [parse_mixpanel_time(item['time']).date() for item in data]
            return set(existing_dates)
    except FileNotFoundError:
        return set()


def get_missing_dates(start_date, end_date, existing_dates):
    requested_dates = pd.date_range(start=start_date, end=end_date).tolist()
    requested_dates = [date.date() for date in requested_dates]
    existing_dates_set = set(existing_dates)
    return [date for date in requested_dates if date not in existing_dates_set]


def append_data_to_file(new_data, file_name):
    try:
        with open(file_name, 'r+') as f:
            data = json.load(f)
            data.extend(new_data)
            f.seek(0)
            json.dump(data, f)
    except FileNotFoundError:
        store_data_to_file(new_data, file_name)


def get_data_from_file(file_name, start_date, end_date):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)

        # Convert string dates to datetime objects for comparison
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        filtered_data = [
            item for item in data
            if start_date_obj <= datetime.strptime(parse_mixpanel_time(item['time']).strftime('%Y-%m-%d'), '%Y-%m-%d') <= end_date_obj

        ]

        return filtered_data

    except FileNotFoundError:
        print("Data file not found.")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []



