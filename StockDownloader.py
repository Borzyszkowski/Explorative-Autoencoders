import json
import csv
import requests
import time
import os

keys = ['UYC4Z4XMXL3ZYO9I', 'CYUKZA6K9HUGZ4IW', 'OGVN93OF72RN9K91', 'H6M076PAQE1TS55X']
symbols = json.load(open('symbols.json'))
url_format = ['https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=', '&apikey=']
directory_name = 'data'


def find_max(symbols: dict) -> int:
    return max([int(x) for x in symbols.keys()])


def url_creator(symbol: str, api_key: str, url_format: list) -> str:
    return url_format[0] + symbol.upper() + url_format[1] + api_key


def save_file(save_name: str, file: list, fields: list) -> int:
    try:
        with open(save_name, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for data in file:
                writer.writerow(data)
        return 0
    except IOError:
        print("I/O error")
        return 2


def simplify_dict(response: dict, fields: list) -> list:
    returned_list = []
    for date, info in response.items():
        variable_dict = {'date': date}
        for element in info.keys():
            modified_name = ''.join([x for x in element if x.isalpha()])
            if modified_name in fields:
                variable_dict[modified_name] = info[element]
        returned_list.append(variable_dict)
    return returned_list


def request_api(link: str, save_name: str) -> int:
    fields = ['date', 'open', 'high', 'low']
    response = requests.get(link)
    response = response.json()
    if not valid_file(response):
        return 1
    response = response["Time Series (Daily)"]
    return save_file(directory_name + "/" + save_name, simplify_dict(response, fields), fields)


def valid_file(json_file: dict) -> bool:
    if "Meta Data" in json_file.keys():
        return True
    else:
        return False


def check_if_data_folder_exists(dir_name='data'):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


# Error codes: 0: VALID, 1: API KEY OUT OF ORDER, 2: IO FAILURE
def download_all_data(keys: list, symbols: dict, url_format: list):
    actual_key = 0
    amount = find_max(symbols)
    check_if_data_folder_exists(directory_name)
    # Modify range of download
    range_of_download = [0, amount]
    for symbol_idx in range(range_of_download[0], range_of_download[1] + 1):
        symbol_id = symbols[str(symbol_idx)]
        if not os.path.isfile(directory_name + '/' + symbol_id + '.csv'):
            print(str(symbol_id) + ": " + str(symbol_idx) + "/" + str(amount))
            url = url_creator(symbol_id, keys[actual_key], url_format)
            error_code = request_api(url, symbol_id + '.csv')
            while error_code:
                if error_code == 2:
                    break
                if error_code == 1:
                    if actual_key < len(keys) - 1:
                        actual_key += 1
                    else:
                        actual_key = 0
                        print("Keys out of order! Waiting 60 s...")
                        time.sleep(60)
                url = url_creator(symbol_id, keys[actual_key], url_format)
                error_code = request_api(url, symbol_id + '.csv')
        else:
            print(symbol_id + " already downloaded!")


download_all_data(keys, symbols, url_format)
