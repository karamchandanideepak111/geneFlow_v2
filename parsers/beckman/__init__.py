import json
from datetime import datetime
class Vicellxr:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.metadata = {}
        self.results = {}
        self.settings = {}
        self.run_date = None
        self.sample_id = None
        self.combined_data = None
        self.__read_text_file()
        self.__create_combined_data()

    def __read_text_file(self):
        # Read the text file and extract relevant data
        with open(self.input_file_path, 'r') as f:
            lines = f.readlines()

        in_results_section = False
        in_settings_section = False

        for line in lines:
            if line.strip() == 'Results:':
                in_results_section = True
                continue
            elif line.strip() == '':
                in_results_section = False
                continue
            elif line.strip() == 'Settings:':
                in_settings_section = True
                continue

            if in_results_section:
                key, value = map(str.strip, line.split(':', 1))

                if "(" in key and ")" in key:
                    key_parts = key.split("(")
                    try:

                        value = float(value)
                        numeric_value = int(value) if value.is_integer() else value
                        unit = key_parts[1].split(")")[0].strip()
                        self.results[key_parts[0].rstrip()] = {
                            "Value": numeric_value,
                            "Unit": unit,
                        }

                    except ValueError:
                        self.results[key] = {'Value': value, 'Unit': ''}

                else:
                    try:

                        value = float(value)
                        value = int(value) if value.is_integer() else value
                        self.results[key] = {'Value': value, 'Unit': ''}
                    except ValueError:
                        self.results[key] = {'Value': value, 'Unit': ''}

            elif in_settings_section:
                if "SizeData" in line:
                    break

                key, value = map(str.strip, line.split(':', 1))
                try:
                    value = float(value)
                    value = int(value) if value.is_integer() else value
                except ValueError:
                    pass
                self.settings[key] = value

            elif "RunDate" in line:
                run_date_str = line.split(':', 1)[1].strip()
                try:
                    self.run_date = datetime.strptime(run_date_str, "%d %b %Y %I:%M:%S %p")
                except ValueError:
                    pass

            elif "Sample ID" in line:
                self.sample_id = line.split(':', 1)[1].strip()

    def get_metadata(self):
        metadata = {
            'Inst_Name': 'ViCell-1',
            'INST_ID': 'EQ123456',
            'Instrument_Version': 'Vi-CELL XR 2.04',
            **self.metadata,
            'RECEIVER': self.input_file_path.split('/')[-1].split('.')[0],
            'User': ''
        }
        return json.dumps({'metadata': metadata})

    def get_results(self):

        """
        results_data = {
            'Results': [self.results]
        }
        """

        results_data = [self.results]
        """
        if self.run_date:
            results_data['Results'][0] = {
                'Date & Time': self.run_date.strftime("%m/%d/%Y %H:%M:%S"),
                'Sample ID': self.sample_id,
                **results_data['Results'][0]
            }
            """
        if self.run_date:
            results_data[0] = {
                'Date & Time': self.run_date.strftime("%m/%d/%Y %H:%M:%S"),
                'Sample ID': self.sample_id,
                **results_data[0]
            }

        return json.dumps({'result': results_data})

    def get_settings(self):
        return json.dumps({'settings': self.settings})

    def __create_combined_data(self):
        # Create the final combined JSON structure
        self.combined_data = {
            'metadata': {
                'Inst_Name': 'ViCell-1',
                'INST_ID': 'EQ123456',
                'Instrument_Version': 'Vi-CELL XR 2.04',
                **self.metadata,
                'RECEIVER': self.input_file_path.split('/')[-1].split('.')[0],
                'User': ''
            },
            'result': [self.results],
            'setting': self.settings
        }
        if self.run_date:
            self.combined_data['result'][0] = {
                'Date & Time': self.run_date.strftime("%m/%d/%Y %H:%M:%S"),
                'Sample ID': self.sample_id,
                **self.combined_data['result'][0]
            }

    def get_combined_data(self):
        return json.dumps({'combined-data': self.combined_data})
