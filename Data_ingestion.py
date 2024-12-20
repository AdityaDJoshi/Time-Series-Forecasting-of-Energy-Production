import requests
import json
import csv
import time
import datetime
import os
import Constants

# FILENAME = "latestdata"
API_KEY = Constants.API_KEY_1  # Replace with your actual API key
API_URL = "https://api.eia.gov/v2/electricity/rto/region-sub-ba-data/data/"


def get_formatted_date(date):
    return date.strftime("%Y-%m-%d")


def get_file_prefix(date, train_test="train"):
    return f"datastore2/{train_test}/{date}"


def write_to_csv(data, csv_file_path):
    records = data['response']['data']

    with open(csv_file_path, 'w', newline='') as csv_file:
        if records:
            fieldnames = records[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)


def fetch_data(date):
    params = {
        "frequency": "hourly",
        "data[0]": "value",
        "start": get_formatted_date(date) + "T00",
        "end": get_formatted_date(date + datetime.timedelta(days=1)) + "T00",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        # "length": 5000,
        "api_key": API_KEY
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {get_formatted_date(date)}. HTTP Status code: {response.status_code}")
        # print(response.json())
        return None


def main():
    writeJSON = False
    last_x_days = 365
    start_date = datetime.datetime(2022, 10, 1)
    end_date = datetime.datetime(2023, 9, 30)

    while start_date <= end_date:
        data = fetch_data(start_date)
        if data:
            csv_file_path = get_file_prefix(get_formatted_date(start_date), train_test="train") + ".csv"
            write_to_csv(data, csv_file_path)
            print(f"Data written for {get_formatted_date(start_date)}")
        # time.sleep(5)
        start_date += datetime.timedelta(days=1)

    # start_date = datetime.datetime(2024, 11, 1)
    # end_date = datetime.datetime(2024, 11, 30)

    # while start_date <= end_date:
    #     data = fetch_data(start_date)
    #     if data:
    #         csv_file_path = get_file_prefix(get_formatted_date(start_date), train_test="test") + ".csv"
    #         write_to_csv(data, csv_file_path)
    #         print(f"Data written for {get_formatted_date(start_date)}")
    #     time.sleep(5)
    #     start_date += datetime.timedelta(days=1)


if __name__ == "__main__":
    main()
