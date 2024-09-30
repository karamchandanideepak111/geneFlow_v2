import datetime
import json
import os
import re
import sys
import roche.constants
import roche.config

from roche.cedex_service_exception import CedexServiceException


class Cedex:
    def __init__(self, filename):
        '''
        # Define the folder path containing text files
        folder_path = os.path.join(os.getcwd(), "Data")


        # Initialize an empty string to store the combined content
        combined_content = ""

        # Iterate over each file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as file:
                    combined_content += file.read()

        # Save the combined content to a new file
        output_file_path = "raw_data_new.txt"
        with open(output_file_path, "w") as output_file:
            output_file.write(combined_content)
        '''
        self.data = self.__parse_data(filename)

    def get_data(self):
        return json.dumps({'data': self.data})

    def __orderid_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the order details and convert into a json
        :param elements: order details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        :return: None
        """
        orderid_list = []
        # fetch the start index for ordername
        ordernumber_start_index = elements.index(constants.SPACE)
        # fetch the regex condition for end index of ordername
        ordernumber_end_regex = re.search(r" \w{1,2}/", elements)
        # fetch the end index of ordername
        if ordernumber_end_regex:
            ordernumber_end_index = ordernumber_end_regex.start()
        # fetch the ordername
        order_number = elements[ordernumber_start_index + 1:ordernumber_end_index]
        # append the ordername to the list
        orderid_list.append(order_number.strip())
        # fetch the orderdate
        order_date = "".join(re.findall(
            r"(?:(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:18|19|20|21)\d{2}|00/00/0000)", elements
        ))
        if order_date == "00/00/0000":
            order_date = datetime.date.today().strftime("%d/%m/%Y")
        elif len(order_date) == 0:
            raise Exception(constants.DATE_NOT_CORRECT_FORMAT)
        # append the orderdate to the list
        orderid_list.append(order_date)

        # fetch the sample type if present
        sample_type = "".join(re.findall(r"\D{,3}$", elements)).strip()
        # sample type is not present-> assign  None to it
        if len(sample_type) == 0:
            sample_type = "None"
        # append the sampletype to the list
        orderid_list.append(sample_type)
        # create a dict with key of orderid and its value
        orderid_dict = dict(zip(linecode_descriptor[linecode], orderid_list))

        return orderid_dict

    def __samplename_validation_line_formation(self, elements):
        """
        Method to fetch the sample name from the line fields
        :param elements: sample name details
        :return: None
        """
        # fetch the start index of the field
        field_start_index = elements.index(constants.SPACE)
        # fetch the field detail
        field_name = elements[field_start_index + 1:]

        return field_name

    def __testid_testname_line_formation(self, elements):
        """
        Method to fetch the test id from the line fields and form test name
        :param elements: sample name details
        :return: None
        """
        # fetch the start index of the field
        field_start_index = elements.index(constants.SPACE)
        # fetch the field detail
        test_id = elements[field_start_index + 1:]
        # update the field detail in linecode_dict
        test_name = next((key for key, value in config.TEST_ID_MAPPING.items() if value == test_id), "")

        return test_id, test_name

    def __result_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the result data from the line fields and form dict
        :param elements:result details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        """
        resultdata_list = []

        # fetch the start index of result
        result_start_index = elements.index(constants.SPACE)
        # fetch the result
        result = elements[result_start_index + 1:result_start_index + 14]
        # append the result to resultdata_list
        resultdata_list.append(result.strip())

        # fetch the unit
        unit = re.findall(r"\s+([a-zA-Z/]{1,6})\s+", elements)[0]
        # append the unit to the list
        resultdata_list.append(unit)

        # fetch flag
        flag = re.findall(r"\s{1,2}[0-9]{1,3}\s", elements)
        flag = [items[:-1].strip() for items in flag]
        resultdata_list.extend(flag)

        # fetch range value to flag and range limit
        range_value = re.findall(r"\s(?:[0-9]{1}[.][0-9]+[E][+]?[-]?[0-9]+|\d+[.]\d+)", elements)
        range_value = range_value[1:]
        resultdata_list.extend(range_value)

        resultdata_dict = dict(zip(linecode_descriptor[linecode], resultdata_list))

        return resultdata_dict

    def __testexecution_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the test execution data from the line fields and form dict
        :param elements:test details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        """
        testexecution_list = []
        # fetch the date
        date = re.findall(r"(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}", elements)[0]
        testexecution_list.append(date)

        # fetch the time
        time = re.findall(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", elements)[0]
        testexecution_list.append(time)

        # fetch the dilution flag
        dilution_flag = re.findall(r"1:(?:[1-9]\s{3}|\d{2}\s{2}|\d{3}\s)", elements)[0].strip()
        testexecution_list.append(dilution_flag)

        # fetch the Sample flag
        sample_flag = re.findall(r"\w+", elements)[-1]
        # append the sample_flag in testexecution_list
        testexecution_list.append(sample_flag)

        testexecution_dict = dict(zip(linecode_descriptor[linecode], testexecution_list))
        return testexecution_dict

    def __cassette_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the cassette data from the line fields and form dict
        :param elements:cassette details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        """
        cassette_information_list = []

        # fetch the cassette lot number
        cassette_lot_number = (re.findall(r" \w+", elements)[0]).strip()
        # append the cassette_lot_number in list
        cassette_information_list.append(cassette_lot_number)

        # cassette serial number
        cassette_serial_number = (re.findall(r" \w+", elements)[1]).strip()
        # append the cassette_serial_number in list
        cassette_information_list.append(cassette_serial_number)

        # cassette expiration dates
        cassette_dates = re.findall(
            r"(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}", elements
        )
        # append the cassette expiration dates in list
        cassette_information_list.extend(cassette_dates)

        cassette_dict = dict(zip(linecode_descriptor[linecode], cassette_information_list))

        return cassette_dict

    def __calibration_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the calibration data from the line fields and form dict
        :param elements:calibration details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        """
        calibrationdata_list = []

        # fetch the calibration date
        calibration_date = re.findall(
            r"(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}", elements
        )[0]
        # append the cassette expiration dates in list
        calibrationdata_list.append(calibration_date)

        # fetch the calibration time
        calibration_time = re.findall(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", elements)[0]
        # append the cassette expiration dates in list
        calibrationdata_list.append(calibration_time)

        # fetch the calibration id
        calibration_id = re.findall(r" \w+-\w+-\w+", elements)[0].strip()
        # append the calibration id in list
        calibrationdata_list.append(calibration_id)

        # fetch the Calibration Lot Number
        calibration_lot_number = re.findall(r" \w+ ", elements)[0].strip()
        # append the calibration lot number in list
        calibrationdata_list.append(calibration_lot_number)

        # fetch the calibration date
        calibration_lot_expiration_date = \
            re.findall(r"(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}", elements)[1]
        # append the cassette expiration dates in list
        calibrationdata_list.append(calibration_lot_expiration_date)

        # fetch the Cassette Lot Number and Serial Number used for Calibration
        cassette_number_for_calibration = re.findall(r" \w+ ", elements)[1:3]
        cassette_number_for_calibration = [items.strip() for items in cassette_number_for_calibration]
        # append the calibration lot number in list
        calibrationdata_list.extend(cassette_number_for_calibration)

        # fetch the calibration ISE Solution 1 Lot Number
        calibration_ise_solution1_lot = re.findall(r" (?:[?]{10}|\w{1,10}) ", elements)[3].strip()
        # append the calibration ISE Solution 1 Lot number in list
        calibrationdata_list.append(calibration_ise_solution1_lot)

        # fetch the calibration ISE Solution 1 Expiration date
        calibration_ise_solution1_expiration = re.findall(
            r"(?:(?:3[01]|[12][0-9]|0[-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}|00/00/0000)", elements
        )[2]
        # append the cassette expiration dates in list
        calibrationdata_list.append(calibration_ise_solution1_expiration)

        # fetch the calibration ISE Solution 2 Lot Number
        calibration_ise_solution2_lot = re.findall(r" (?:[?]{10}|\w{1,10}) ", elements)[4].strip()
        # append the calibration ISE Solution 1 Lot number in list
        calibrationdata_list.append(calibration_ise_solution2_lot)

        # fetch the calibration ISE Solution 2 Expiration date
        calibration_ise_solution2_expiration = re.findall(
            r"(?:(?:3[01]|[12][0-9]|0[-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}|00/00/0000)", elements
        )[3]
        # append the cassette expiration dates in list
        calibrationdata_list.append(calibration_ise_solution2_expiration)

        # fetch the calibration ISE Solution 3 Lot Number
        calibration_ise_solution3_lot = re.findall(r" (?:[?]{10}|\w{1,10}) ", elements)[5].strip()
        # append the calibration ISE Solution 1 Lot number in list
        calibrationdata_list.append(calibration_ise_solution3_lot)

        # fetch the calibration ISE Solution 3 Expiration date
        calibration_ise_solution3_expiration = re.findall(
            r"(?:(?:3[01]|[12][0-9]|0[-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}|00/00/0000)", elements
        )[3]
        # append the cassette expiration dates in list
        calibrationdata_list.append(calibration_ise_solution3_expiration)

        # fetch the calibration result coefficient
        calibration_result_coefficient = re.findall(r" \S{1,10} ", elements)[8:]
        calibration_result_coefficient = [items.strip() for items in calibration_result_coefficient]
        # append the calibration result coefficient in list
        calibrationdata_list.extend(calibration_result_coefficient)

        # fetch the calibrator flag
        calibrator_flag = "".join(re.findall(r" \d{,3}$", elements)).strip()

        # append the calibrator flag in list
        calibrationdata_list.append(calibrator_flag)

        calibrationdata_dict = dict(zip(linecode_descriptor[linecode], calibrationdata_list))

        return calibrationdata_dict

    def __control_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the control data from the line fields and form dict
        :param elements:control details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        :return controldata_dict:control details
        """
        controldata_list = []
        # fetch the Control Date
        control_date = re.findall(
            r"(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}", elements
        )[0]
        # append the control date to the list
        controldata_list.append(control_date)

        # fetch the control time
        control_time = re.findall(r"(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d", elements)[0]
        # append the control time to the list
        controldata_list.append(control_time)

        # fetch the control ID
        control_id = re.findall(r" \w+-\w+-\w+", elements)[0].strip()
        # append the control id to the list
        controldata_list.append(control_id)

        # fetch the control lot number
        control_lot_number = re.findall(r" \w+ ", elements)[0].strip()
        # append the control lot number to the list
        controldata_list.append(control_lot_number)

        # fetch the control lot expiration date
        control_lot_expiration_date = re.findall(
            r"(?:3[01]|[12][0-9]|0[1-9])/(?:1[0-2]|0[1-9])/(?:19|20)\d{2}", elements
        )[1]
        # append the control lot expiration date to the list
        controldata_list.append(control_lot_expiration_date)

        # fetch the cassette lot  number and cassette serial number
        cassette_number = re.findall(r" \w+ ", elements)[1:]
        cassette_number = [items.strip() for items in cassette_number]
        # append the cassette lot number and cassette serial number to the list
        controldata_list.extend(cassette_number)

        # fetch the Control Result
        control_result = re.findall(
            r"\s(?:[0-9]{1}[.][0-9]+[E][+]?[-]?[0-9]+|\d+[.]\d+)", elements
        )[0].strip()
        # append the control result to the list
        controldata_list.append(control_result)

        # fetch the Control unit
        control_unit = re.findall(r"\s+([a-zA-Z/]{1,6})\s+", elements)[0].strip()
        # append the control unit to the list
        controldata_list.append(control_unit)

        # fetch the Control Flag
        control_flag = re.findall(r"\d{1,3}$", elements)[0]
        # append the control flag to the list
        controldata_list.append(control_flag)

        controldata_dict = dict(zip(linecode_descriptor[linecode], controldata_list))
        return controldata_dict

    def __absorbance_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the absorbance data from the line fields and form dict
        :param elements:absorbance details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        :return controldata_dict:absorbance details
        """
        absorbance_list = []
        # fetch the cycle and replicate number
        cycle_replicatenumber = re.findall(r" \d{1,3}", elements)[:2]
        cycle_replicatenumber = [items.strip() for items in cycle_replicatenumber]
        # append the cycle_replicatenumber to the list
        absorbance_list.extend(cycle_replicatenumber)

        # fetch the absorbance data
        absorbance_data = "".join(re.findall(r" [-]?\d+.\d+$", elements)).strip()
        # append the absorbance data to the list
        absorbance_list.append(absorbance_data)

        absorbance_dict = dict(zip(linecode_descriptor[linecode], absorbance_list))
        return absorbance_dict

    def __fp_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the fp raw data from the line fields and form dict
        :param elements:fp raw data details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        :return controldata_dict:fp raw data details
        """
        # fetch the dpraw_data
        fpraw_data = re.findall(r"\s?\d{1,9}\s?", elements)[1:]
        fpraw_data = [items.strip() for items in fpraw_data]
        # append the fpraw_data in the list
        fpraw_dict = dict(zip(linecode_descriptor[linecode], fpraw_data))
        return fpraw_dict

    def __rerun_line_formation(self, elements, linecode_descriptor, linecode):
        """
        Method to fetch the fp raw data from the line fields and form dict
        :param elements:rerun details
        :param linecode_descriptor: json containing linecode and its each field
        :param linecode: linecode of the particular line
        :return controldata_dict:rerun details
        """
        rerunstatus_list = []
        # fetch the Sample Concentration
        sample_concentration = "".join(
            re.findall(r"\s(?:[0-9]{1}[.][0-9]+[E][+]?[-]?[0-9]+|\d+[.]\d+)", elements)).strip()
        # append the sample concentration to the list
        rerunstatus_list.append(sample_concentration)

        # fetch the rerun order
        rerun_order = re.findall(r" \d{1,2} ", elements)[0].strip()
        # append the rerun order to the list
        rerunstatus_list.append(rerun_order)

        # fetch the dilution flag
        dilution_flag_rerun = re.findall(
            r"1:(?:[1-9]\s{3}$|\d{2}\s{2}$|\d{3}\s?$)", elements
        )[0].strip()
        # append the dilution flag to the list
        rerunstatus_list.append(dilution_flag_rerun)

        rerun_dict = dict(zip(linecode_descriptor[linecode], rerunstatus_list))
        return rerun_dict

    def __linecode_json_form(self, data: list, linecode_descriptor: dict):
        """
        Method to create a dict array from the instrument response
        :param data: data block of the response : str
        :param linecode_descriptor: dict
        :return: linecode_dict :dict
        """
        try:
            # print("Entering linecode_json_form method")

            absorbancerawdata_arraylist = []
            fprawdata_arraylist = []
            iserawdata_arraylist = []
            controlinformation_arraylist = []
            rerunresult_arraylist = []
            linecode_dict = {}
            # print(data)
            for elements in data:

                # fetch the line code
                linecode = elements.split(constants.SPACE)[0]

                if linecode in linecode_descriptor.keys():
                    # linecode is orderid
                    if linecode == constants.ORDERID_CODE:
                        orderid_dict = self.__orderid_line_formation(elements, linecode_descriptor, linecode)
                        # append the array to the linecode_dict
                        linecode_dict[constants.ORDERID] = orderid_dict

                    # linecode is sample name
                    elif linecode == constants.SAMPLENAME_CODE:
                        sample_name = self.__samplename_validation_line_formation(elements)
                        # update the field detail in linecode_dict
                        linecode_dict[constants.SAMPLENAME] = sample_name

                    # linecode is test id
                    elif linecode == constants.TESTID_CODE:
                        test_id, test_name = self.__testid_testname_line_formation(elements)
                        linecode_dict[constants.TESTID] = test_id
                        linecode_dict[constants.TESTNAME] = test_name

                    # linecode is result data
                    elif linecode == constants.RESULT_CODE:
                        resultdata_dict = self.__result_line_formation(elements, linecode_descriptor, linecode)
                        # append the array to the linecode_dict
                        linecode_dict[constants.RESULT_DATA] = resultdata_dict

                    # linecode is validation status
                    elif linecode == constants.VALIDATION_CODE:
                        validation = self.__samplename_validation_line_formation(elements)
                        # update the field detail in linecode_dict
                        linecode_dict[constants.VALIDATION_STATUS] = validation

                    # linecode is Test execution
                    elif linecode == constants.TESTEXECUTION_CODE:
                        testexecution_dict = self.__testexecution_line_formation(
                            elements, linecode_descriptor, linecode
                        )
                        # update the field detail in linecode_dict
                        linecode_dict[constants.TEST_EXECUTION] = testexecution_dict

                    # linecode is Cassette Information
                    elif linecode == constants.CASSETTE_CODE:
                        cassette_dict = self.__cassette_line_formation(elements, linecode_descriptor, linecode)
                        # append the array to the linecode_dict
                        linecode_dict[constants.CASSETTE] = cassette_dict

                    # linecode is calibration data
                    elif linecode == constants.CALIBRATION_CODE:
                        calibrationdata_dict = self.__calibration_line_formation(
                            elements, linecode_descriptor, linecode
                        )
                        # append the array to the linecode_dict
                        linecode_dict[constants.CALIBRATION] = calibrationdata_dict

                    # linecode is control data
                    elif linecode == constants.CONTROL_DATA:
                        controldata_dict = self.__control_line_formation(elements, linecode_descriptor, linecode)
                        controlinformation_arraylist.append(controldata_dict)
                        # append the array to the linecode_dict
                        linecode_dict[constants.CONTROL] = controlinformation_arraylist

                    # linecode is absorbance data
                    elif linecode == constants.ABSORBANCE_CODE:
                        absorbance_dict = self.__absorbance_line_formation(elements, linecode_descriptor, linecode)
                        # append the dict to a array
                        absorbancerawdata_arraylist.append(absorbance_dict.copy())
                        # append the array to the linecode_dict
                        linecode_dict[constants.ABSORBANCE_RAWDATA] = absorbancerawdata_arraylist

                    # linecode is FP Raw data
                    elif linecode == constants.FPRAWDATA_CODE:
                        fpraw_dict = self.__fp_line_formation(elements, linecode_descriptor, linecode)
                        # append the dict to a array
                        fprawdata_arraylist.append(fpraw_dict)
                        # append the array to the linecode_dict
                        linecode_dict[constants.FP_RAWDATA] = fprawdata_arraylist

                    # linecode is ISE Raw data
                    elif linecode == constants.ISERAWDATA_CODE:
                        # fetch the ise mean value
                        ise_mean_value = "".join(re.findall(r" \d+.\d+$", elements)).strip()
                        # append the validation_status in arraylist
                        iserawdata_arraylist.append(ise_mean_value)
                        # update the testid in linecode_dict
                        linecode_dict[constants.ISE_RAWDATA] = iserawdata_arraylist

                    # linecode is rerun status
                    elif linecode == constants.RERUN_CODE:
                        rerun_dict = self.__rerun_line_formation(elements, linecode_descriptor, linecode)

                        # append the dict to a array
                        rerunresult_arraylist.append(rerun_dict)
                        # append the array to the linecode_dict
                        linecode_dict[constants.RERUN] = rerunresult_arraylist

                else:
                    raise CedexServiceException(constants.LINECODE_DESCRIPTION_NOTFOUND, constants.RESPONSE_CODE_500)

            # print("Exiting linecode_json_form method")
            if constants.TESTNAME not in linecode_dict:
                linecode_dict[constants.TESTID] = ""
                linecode_dict[constants.TESTNAME] = ""

            return linecode_dict
        except CedexServiceException as exception_message:
            print("Exception occurred in linecode_json_form-%s", exception_message)
            return None

    def __parse_data(self, filename):
        try:
            linecode_complete_data_array = []
            with open("roche/linecode_description.json", "r", encoding="UTF-8") as linecode_description_file:
                linecode_description = json.load(linecode_description_file)
            try:
                with open(filename, "r", encoding="UTF-8") as file:
                    instrument_response = file.read()
                    response_list = instrument_response.split('\n\n')
                    response_list = [response for response in response_list if response.strip()]
            except FileNotFoundError as exception_message:
                sys.exit(1)

            for instrument_test_response in response_list:
                # fetch the starting index of block data
                datastarting_index = instrument_test_response.index(constants.STX + constants.LF)
                # fetch the end index of block data
                dataending_index = instrument_test_response.index(constants.ETX + constants.LF)
                # fetch the content of block data
                instrument_data = instrument_test_response[datastarting_index + 2:dataending_index - 1]

                # store the block data as list
                data_list = instrument_data.split(constants.LF)

                linecode_dictionary = self.__linecode_json_form(data_list, linecode_description)
                if linecode_dictionary is None:
                    raise CedexServiceException(constants.ERROR_IN_JSON, constants.RESPONSE_CODE_500)
                linecode_complete_data_array.append(linecode_dictionary)
            # print(linecode_complete_data_array)
            return linecode_complete_data_array
            """
            base_name = os.path.basename(config.RESPONSE_FILE).split('.')[0]

            current_date = datetime.datetime.now().strftime(constants.TIME_FORMAT)

            output_file_path = os.path.join(
                os.path.dirname(os.path.abspath(sys.argv[0])), "Output"
            )
            if not os.path.exists(output_file_path):
                os.mkdir(output_file_path)
            response_json_file_path = os.path.join(
                output_file_path, f"{base_name}_{current_date}{config.JSON_EXTENSION}"
            )

            with open(response_json_file_path, "w+", encoding=constants.UTF8) as file:
                json.dump(linecode_complete_data_array, file)
                print(constants.OUTPUT_FILE_CREATED)
            """
        except Exception as exception_message:
            print("Exception occurred in linecode connector-%s", exception_message)
            return None
