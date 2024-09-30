import fitz
import json

class endotoxin:
    def __init__(self,path):
        self.data = self.__extract_data(path)

    def __extract_data(self,path):
        fname = path
        extracted_data_dict_list = []
        with fitz.open(fname) as doc:
            for page in doc:

                text = page.get_text()
                reviewer_index = text.find("Reviewer:")
                l = text[:reviewer_index].split("\n")
                extracted_data_dict = {}
                if "Assay Name:" in l:
                    assay_name_index = l.index("Assay Name:")
                    extracted_data_dict["Assay Name"] = l[assay_name_index + 1]
                extracted_data_dict["Analyst"] = l[3].split(": ")[1]
                extracted_data_dict["Assay Date/Time"] = l[4].split(": ")[1]
                extracted_data_dict["Lab Name"] = l[5].split(": ")[1]
                extracted_data_dict["Instrument Type"] = l[6].split(": ")[1]
                extracted_data_dict["Instrument Serial Number"] = l[7].split(": ")[1]
                if "Serial Number/Bay:" in l:
                    serial_no_index = l.index("Serial Number/Bay:")
                    extracted_data_dict["Serial Number/Bay"] = l[serial_no_index + 1]
                if "Start/End Temp (°C):" in l:
                    start_end_temp_index = l.index("Start/End Temp (°C):")
                    extracted_data_dict["Start/End Temp (°C)"] = l[start_end_temp_index + 1]
                if "Sample Name:" in l:
                    sample_name_index = l.index("Sample Name:")
                extracted_data_dict["Sample Name"] = l[sample_name_index + 1]
                if "Sample ID:" in l:
                    sample_id_index = l.index("Sample ID:")
                    extracted_data_dict["Sample ID"] = l[sample_id_index + 1]
                if "Sample Lot:" in l:
                    sample_lot_index = l.index("Sample Lot:")
                    extracted_data_dict["Sample Lot"] = l[sample_lot_index + 1]
                if "Dil./Conc.:" in l:
                    dil_conc_index = l.index("Dil./Conc.:")
                    extracted_data_dict["Dil./Conc."] = l[dil_conc_index + 1]
                if "Sample Comments:" in l:
                    sample_comment_index = l.index("Sample Comments:")
                    extracted_data_dict["Sample Comments"] = l[sample_comment_index + 1]
                if "Cartridge Lot Number:" in l:
                    catridge_lot_no_index = l.index("Cartridge Lot Number:")
                    extracted_data_dict["Cartridge Lot Number"] = l[catridge_lot_no_index + 1]
                if "Cartridge Range:" in l:
                    catridge_range_index = l.index("Cartridge Range:")
                    extracted_data_dict["Cartridge Range"] = l[catridge_range_index + 1]
                if "Calibration Code:" in l:
                    calibration_code_index = l.index("Calibration Code:")
                    extracted_data_dict["Calibration Code"] = l[calibration_code_index + 1]
                if "Archived Spike Concentration:" in l:
                    archieve_spike_conc_index = l.index("Archived Spike Concentration:")
                    extracted_data_dict["Archived Spike Concentration"] = l[archieve_spike_conc_index + 1]
                if "Range" in l:
                    range_index = l.index("Range")
                    extracted_data_dict["Range"] = l[range_index + 1]
                if "Y-Intercept:" in l:
                    y_intercept_index = l.index("Y-Intercept:")
                    extracted_data_dict["Y-Intercept"] = l[y_intercept_index + 1]
                if "Slope:" in l:
                    slope_index = l.index("Slope:")
                    extracted_data_dict["Slope"] = l[slope_index + 1]
                if "Endotoxin Value:" in l:
                    endotoxin_index = l.index("Endotoxin Value:")
                    extracted_data_dict["Endotoxin Value"] = l[endotoxin_index + 1]
                if "Sample CV Limit:" in l:
                    sample_cv_limit_index = l.index("Sample CV Limit:")
                    extracted_data_dict["Sample CV Limit"] = l[sample_cv_limit_index + 1]
                    extracted_data_dict["Sample CV Limit Status"] = l[sample_cv_limit_index + 3]
                if "Endotoxin Limit:" in l:
                    endotoxin_limit_index = l.index("Endotoxin Limit:")
                    extracted_data_dict["Endotoxin Limit"] = l[endotoxin_limit_index + 1]
                    extracted_data_dict["Endotoxin Limit Status"] = l[endotoxin_limit_index + 3]
                if "Spike CV Limit:" in l:
                    spike_cv_limit_index = l.index("Spike CV Limit:")
                    extracted_data_dict["Spike CV Limit"] = l[spike_cv_limit_index + 1]
                    extracted_data_dict["Spike CV Limit Status"] = l[spike_cv_limit_index + 3]
                if "Alert Limit:" in l:
                    alert_limit_index = l.index("Alert Limit:")
                    extracted_data_dict["Alert Limit"] = l[alert_limit_index + 1]
                if "Spike Recovery Range:" in l:
                    spike_recovery_range_index = l.index("Spike Recovery Range:")
                    extracted_data_dict["Spike Recovery Range"] = l[spike_recovery_range_index + 1] + l[
                        spike_recovery_range_index + 2]
                    extracted_data_dict["Spike Recovery Range Status"] = l[spike_recovery_range_index + 4]
                if "Detailed Endotoxin Cartridge Report:" in l:
                    report_comments_index = l.index("Detailed Endotoxin Cartridge Report:") - 1
                    extracted_data_dict["Report Comments"] = l[report_comments_index].split(": ")[1]
                else:
                    continue

                if "SAMPLE DATA" in l:
                    sample_data_index = l.index("SAMPLE DATA")
                    sample_data_info_list = []
                    spike_data_info_list = []
                    sample_spike_data_list = l[sample_data_index + 16:report_comments_index]
                    sample_spike_data_len = (len(sample_spike_data_list) - 5) // 4
                    sample_data_dict = {}
                    spike_data_dict = {}
                    sample_data_dict["CV%"] = sample_spike_data_list[2]
                    sample_data_dict["Sample Value"] = sample_spike_data_list[3]
                    spike_data_dict["CV%"] = sample_spike_data_list[6]
                    spike_data_dict["Spike Value"] = sample_spike_data_list[7] + " " + sample_spike_data_list[8]
                    spike_data_dict["Spike Recovery %"] = sample_spike_data_list[9]
                    sample_channel_dict = {"Channel": sample_spike_data_list[0], "Reaction Time": sample_spike_data_list[1]}
                    spike_channel_dict = {"Channel": sample_spike_data_list[4], "Reaction Time": sample_spike_data_list[5]}
                    sample_channel_data_list = [sample_channel_dict]
                    spike_channel_data_list = [spike_channel_dict]
                    sample_spike_remaining_records_index = 10
                    for i in range(sample_spike_data_len - 1):
                        sample_channel_dict = {"Channel": sample_spike_data_list[sample_spike_remaining_records_index],
                                               "Reaction Time": sample_spike_data_list[
                                                   sample_spike_remaining_records_index + 1]}
                        spike_channel_dict = {"Channel": sample_spike_data_list[sample_spike_remaining_records_index + 2],
                                              "Reaction Time": sample_spike_data_list[
                                                  sample_spike_remaining_records_index + 3]}
                        sample_channel_data_list.append(sample_channel_dict)
                        spike_channel_data_list.append(spike_channel_dict)
                        sample_spike_remaining_records_index += 4
                    sample_data_dict["Channel Data"] = sample_channel_data_list
                    spike_data_dict["Channel Data"] = spike_channel_data_list
                    sample_data_info_list.append(sample_data_dict)
                    spike_data_info_list.append(spike_data_dict)
                    extracted_data_dict["Sample Data Info"] = sample_data_info_list
                    extracted_data_dict["Spike Data Info"] = spike_data_info_list
                extracted_data_dict_list.append(extracted_data_dict)
            return extracted_data_dict_list

    def get_data(self):
        Endotoxin_LR_json = json.dumps(self.data)
        return Endotoxin_LR_json
