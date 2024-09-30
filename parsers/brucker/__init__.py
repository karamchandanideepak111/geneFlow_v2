import pandas as pd
import json
class Iconnmr:
    def __init__(self, set_file):
        self.set_file = set_file
        self.data_dict = self.__parse_set_files()

    def get_data(self):
        return json.dumps({'data':self.data_dict})

    def __remove_braces(self, input_string):
        output_string = input_string
        if '{' in input_string:
            output_string = output_string.replace('{', '')
        if '}' in input_string:
            output_string = output_string.replace('}', '')
        return output_string

    def __fetch_comment(self, title_list, first_index, last_index):
        comment = ""
        for comt in title_list[first_index + 1:last_index]:
            comment += comt + "\n"
        return comment

    def __parse_set_files(self):
        with open(self.set_file, 'r') as fh:
            fd = fh.read()

        set_file_list = fd.split('\n')
        holder_list = [value for value in set_file_list if 'Holder' in value]
        last_title_ind = max(idx for idx, val in enumerate(set_file_list) if 'Title' in val)

        output_parsed_list = []

        for each_holder in holder_list:
            each_row_dict = {}
            holder = each_holder.split(' ')[1].strip()
            each_row_dict['Holder'] = holder

            experiment_id = each_holder.split(' ')[3].strip()
            if '{' in experiment_id:
                experiment_id = self.__remove_braces(each_holder.split(' ')[3] + each_holder.split(' ')[4]).strip()
            each_row_dict['Experiment ID'] = experiment_id

            pulse_sequence = ""
            if '{N' in each_holder.split(' '):
                pulse_sequence_index = each_holder.split(' ').index('{N')
                pulse_sequence = self.__remove_braces(each_holder.split(' ')[pulse_sequence_index + 1]).strip()
                each_row_dict['Pulse Sequence'] = pulse_sequence

            data_folder = ''
            for data in each_holder.split(' '):
                if 'nmr' in data:
                    data_folder = self.__remove_braces(data).strip()
            each_row_dict['Data folder'] = data_folder

            comments = ""
            start_comment_index = set_file_list.index(each_holder) + 1
            if holder_list.index(each_holder) != (len(holder_list) - 1):
                end_comment_index = set_file_list.index(holder_list[holder_list.index(each_holder) + 1]) - 1
            else:
                end_comment_index = last_title_ind

            comments = self.__fetch_comment(set_file_list, start_comment_index, end_comment_index)
            each_row_dict['Comments'] = comments

            output_parsed_list.append(each_row_dict)

        return pd.DataFrame(output_parsed_list).to_dict()

