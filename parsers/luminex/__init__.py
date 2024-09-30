import csv
import json


class xponent:
    def __init__(self, path):
        self.info, self.cal_info, self.protocol, self.data = self.__read_data(path)

    def get_data(self):
        return self.data

    def get_protocol(self):
        return self.protocol

    def get_cal_info(self):
        return self.cal_info

    def get_info(self):
        return self.info

    def __read_data(self, path):
        data = self.__read_csv_file(path)
        print(data)
        info_temp = []
        protocol = []
        for line in data[:19]:
            if line:
                if "Protocol" in line[0]:
                    protocol.append(line)
                else:
                    info_temp.append(line)
        proto_data = {}
        for row in data[19:21]:
            proto_data[row[0]] = {row[i]: row[i + 1] for i in range(1, len(row), 2) if row[i] and row[i + 1]}
        for line in data[21:26]:
            if line:
                if "Protocol" in line[0]:
                    protocol.append(line)
                else:
                    info_temp.append(line)
        info_data = {}
        for line in info_temp:
            if line:
                info_data[line[0]] = ' '.join(line[1:])
        if data[37][1]:
            info_data["Sample"] = data[37][1]
        if data[37][4] and data[37][3]:
            info_data["Min Events"] = {
                "unit": data[37][4],
                "value": data[37][3]
            }
        for line in protocol:
            if line:
                proto_data[line[0]] = ' '.join(line[1:])
        cal_info = []
        temp_cal = {}
        for line in range(len(data[33])):
            if data[33][line] and data[34][line]:
                temp_cal[data[33][line]] = data[34][line]
        if temp_cal:
            cal_info.append({"Calibrator": temp_cal})
        result = {}
        temp_data = []
        key = ''
        for line in data[41:]:

            if line and line[0] != '':
                #print("int cond 1")
                if line[0] == "DataType:":
                    key = line[1]
                else:
                    temp_data.append(line)
            elif temp_data and key:
                #print("int cond 2")
                table_data = self.__get_table_data(temp_data)
                if table_data:
                    result[key] = table_data
                temp_data = []
                key = ''
        return info_data, cal_info, proto_data, result

    def __equalize_sublist_sizes(self, lst):
        max_len = max(len(sublist) for sublist in lst)
        for sublist in lst:
            sublist.extend([''] * (max_len - len(sublist)))
        return lst

    def __get_table_data(self, data):
        data = self.__equalize_sublist_sizes(data)
        #print(data)
        final_data = []
        keys = []
        units = []
        for key in data[0]:
            unit = ''
            if '(' in key:
                start = key.find('(')
                end = key.find(')')
                unit = key[start + 1:end]
                key = key[:start - 1] + key[end + 1:]
            keys.append(key)
            units.append(unit)
        if len(data) > 1:
            for line in data[1:]:
                #print(line)
                result = {}
                for i, key in enumerate(keys):
                    #print(i)
                    result[key] = {'unit': units[i], 'value': str(line[i])}
                final_data.append(result)
        else:
            final_data.append(dict.fromkeys(keys))
        return final_data

    def __read_csv_file(self, file_path):
        output_file = "Data/cleaned.csv"
        with open(file_path, 'r') as inp, open(output_file, 'w', newline='') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if any(field.strip() for field in row):
                    # If row is not completely empty, remove empty fields
                    writer.writerow(field for field in row if field.strip())
                else:
                    # If row is completely empty, write it as is
                    writer.writerow(row)

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data
