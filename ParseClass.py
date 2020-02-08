import json
import logging
import datetime


def key_fix(key: str, split_sign='.'):
    return key.split(split_sign)[1].strip()


class SaveClass(object):
    expected_header = ['Interval', 'Last Refreshed']
    expected_info = ['high', 'low', 'open', 'close']
    export_header = {}
    export_info = []

    def __init__(self, parameter_input_file="data.json"):
        self.input_path = parameter_input_file
        self.opened_file = json.load(open(self.input_path))
        self.meta_shorter()
        self.info_parser(self.opened_file["Time Series (" + self.export_header['Interval'] + ")"])

    def export_json(self, export_path='test.json'):
        with open(export_path, 'w') as export:
            json.dump({'meta': self.export_header, 'data': self.export_info}, export)

    def meta_shorter(self):
        if "Meta Data" in self.opened_file.keys():
            self.tag_parser(self.opened_file["Meta Data"])
        else:
            logging.warning("Possibly wrong file format. Expected meta data header!")

    def tag_parser(self, meta_data_unparsed: dict):
        for tag, info in meta_data_unparsed.items():
            changed_tag = key_fix(tag)
            if changed_tag in self.expected_header:
                self.export_header[changed_tag] = info

    def info_parser(self, info: dict):
        for innerDict in info.values():
            log_point = {}
            for key, val in innerDict.items():
                parsed_key = key_fix(key)
                if parsed_key in self.expected_info:
                    log_point[parsed_key] = val
            self.export_info.append(log_point)


class LoadClass(object):
    def __init__(self, parameter_export_file="test.json"):
        self.opened_file = json.load(open(parameter_export_file))
        self.loaded_meta_header = self.opened_file['meta']
        self.data_information = self.opened_file['data']
        self.add_time_parameter(self.data_information, self.loaded_meta_header)

    # TODO add time when stock market is up. For now it sets next possible spots in given intervals.
    def add_time_parameter(self, info_to_modify: list, meta_header_data: dict):
        t_units = {'min': 60, 'hour': 60 * 60, 'day': 60 * 60 * 24}
        t_unit_in_header = ''.join([x for x in meta_header_data['Interval'] if x.isalpha()])
        interval_in_secs = int(meta_header_data['Interval']
                               [:len(meta_header_data['Interval']) - len(t_unit_in_header)]) * t_units[t_unit_in_header]
        starting_date = datetime.datetime.strptime(meta_header_data['Last Refreshed'], '%Y-%m-%d %H:%M:%S')
        for logIndex in info_to_modify:
            logIndex['date'] = starting_date.strftime('%Y-%m-%d %H:%M:%S')
            starting_date = starting_date - datetime.timedelta(0, interval_in_secs)

    def output_file(self):
        return {'meta': self.loaded_meta_header, 'data': self.data_information}
