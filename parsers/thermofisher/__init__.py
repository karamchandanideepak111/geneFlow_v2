import datetime
from datetime import datetime
import json


class Osmopro:
    def __init__(self, path):
        self.metadata = ''
        self.result = ''
        self.osmo = ''
        self.__read(path)

    def get_metadata(self):
        return json.dumps({'metadata': self.metadata})

    def get_result(self):
        data = {
            'Result': self.result,
            'Osmolality': self.osmo
        }
        return json.dumps({'result': data})

    def __read(self, path):
        with open(path) as f:
            lines = f.readlines()
        node = [x.split("|")[0][1] for x in lines]
        if (''.join(node)) != "HPORL":
            return "Error"
        else:
            data = [x.strip().split("|") for x in lines]
            for val in data:
                stat = val[0][1]
                if stat == 'H':
                    self.metadata = self.__readMetadata(val)
                elif stat == 'R':
                    self.result = self.__readOsmo(val)
                elif stat == 'O':
                    self.osmo = self.__readResult(val)

    def __readMetadata(self, metadata):
        clean_data = [s for s in metadata if s != '']
        metadata = {
            "Inst_Name": clean_data[2].split("^")[0],
            "Version": clean_data[2].split("^")[1],
            "Receiver": clean_data[5],
            "Inst_ID": ""
        }
        return metadata

    def __readOsmo(self, osmo):
        clean_osmo = [s for s in osmo if s != '']
        #print(clean_osmo)
        osmo = {
            "Test Time": (datetime.strptime(clean_osmo[8], '%Y%m%d%H%M%S')).strftime('%m/%d/%Y %H:%M:%S'),
            "Unit": clean_osmo[4],
            "Value": clean_osmo[3]
        }
        return osmo

    def __readResult(self, result):
        clean_result = [s for s in result if s != '']
        #print(clean_result)
        result = {
            "Sample ID": clean_result[2],
            "Date & Time": (datetime.strptime(clean_result[4], '%Y%m%d%H%M%S')).strftime('%m/%d/%Y %H:%M:%S')
        }
        return result
