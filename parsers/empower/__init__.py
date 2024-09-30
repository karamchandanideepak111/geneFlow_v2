from PyPDF2 import PdfReader
import fitz
from PIL import Image
import json
import re
import empower.imagecrop
import os

#Parser for Empower.Chromatography Instrument
class Chromatography:
    #Initializing path
    def __init__(self, path):
        """
        Initializes the DataExtractor with the specified path.
        :param path: Absolute path of the folder containing data files.
        """
        self.path = path

    #Fetching Images from Input File
    def __fetchImage(self, path, pageNo, sampleName):
        """
        This method is used to extract the images from the file and save it with the names.
        :param path: Absolute Path of the file.
        :param pageNo: the pageNo of the Pdf from where the image to be fetched ( datatype- int)
        :param sampleName: datatype- str
        :return: None ( the images will be saved ).
        """
        doc = fitz.open(path)

        page = doc.load_page(pageNo)

        image, lx0, ly0, rx1, ry1 = imagecrop.crop_image(path, pageNo, 'Processed:', 'Minutes')

        croppedImage = image.crop((lx0 - 51, ly0 + 22, rx1 + 270, ry1 + 10))

        croppedImage.save('SecEmpowerImages\\' + str(pageNo) + '_' + sampleName + '.jpg')


    #Return Number of Samples in File
    def numberOfSamples(self):
        try:
            fname = self.path

            info_list = []

            with fitz.open(fname) as doc:
                count = doc.page_count

            return count
        except Exception as e:
            return str(e)

    #Return Information of Sample
    def getSampleInfo(self):
        try:
            fname = self.path

            info_list = []

            with fitz.open(fname) as doc:
                count = doc.page_count

                for i in range(0, count):
                    text = ""
                    page = doc[i]
                    text += page.get_text()
                    l = text.split("\n")

                    mydict = {}

                    mydict['sample_name'] = l[l.index('Sample Name:') - 1].strip()

                    info_dict = {}

                    list1 = [
                        "sample_type",
                        "vial",
                        "injection#",
                        "injection_volume",
                        "run_time",
                        "acquired_by",
                        "sample_set_name",
                        "acq_method_set",
                        "processing_method",
                        "channel_name",
                        "proc_chnl_descr",
                        "data_acquired",
                        "data_processed"
                    ]

                    list2 = [
                        "Sample Type:",
                        "Vial:",
                        "Injection #:",
                        "Injection Volume:",
                        "Run Time:",
                        "Acquired By:",
                        "Sample Set Name:",
                        "Acq. Method Set:",
                        "Processing Method:",
                        "Channel Name:",
                        "Proc. Chnl. Descr.:",
                        "Date Acquired:",
                        "Date Processed:"
                    ]
                    info_dict["sample_name"] = l[l.index('Sample Name:') - 1].strip()

                    for k, v in zip(list1, list2):
                        if k == "proc_chnl_descr" or k == "processing_method":
                            for el in l:
                                if el.startswith(v):
                                    info_dict[k] = el.split(':')[1].strip()
                        elif k == "run_time" or k == "acq_method_set" or k == "data_processed" or k == "channel_name":
                            info_dict[k] = l[l.index(v) + 1].strip()
                        else:
                            if (l[l.index(v) - 1] not in list2) and (not l[l.index(v) - 1].strip() == ''):
                                info_dict[k] = l[l.index(v) - 1].strip()
                            else:
                                info_dict[k] = 'NIL'

                    info_list.append(info_dict)

            return json.dumps(info_list)
        except Exception as e:
            return str(e)

    #Return All Channel Information
    def getChannelInfo(self):
        try:
            fname = self.path

            final_list = []

            with fitz.open(fname) as doc:
                count = doc.page_count

                for i in range(0, count):
                    text = ""
                    page = doc[i]
                    text += page.get_text()
                    l = text.split("\n")

                    mydict = {}

                    mydict['sample_name'] = l[l.index('Sample Name:') - 1].strip()


                    channel_list = []

                    channel_dict = {}

                    list3 = [
                        "channel_name",
                        "rt",
                        "area",
                        "area%",
                        "height"
                    ]

                    list4 = [
                        'Channel Name',
                        'RT',
                        'Area',
                        '% Area',
                        'Height'
                    ]

                    diff = len(l) - l.index('Channel Name')

                    if diff <= 5:
                        for k in list3:
                            if k == "channel_name":
                                channel_dict[k] = l[l.index('Channel Name') + 1]
                            else:
                                channel_dict[k] = 'NIL'

                        channel_list.append(channel_dict)
                    else:
                        rows = int(l[l.index('Channel Name') - 1])

                        for i in range(0, rows):
                            channel_dict = {}

                            channel_dict["channel_name"] = l[l.index('Channel Name') + 5 + i]
                            channel_dict["rt"] = l[l.index('Channel Name') + 5 + rows + i]
                            channel_dict["area"] = l[l.index('Channel Name') + 5 + rows * 2 + i]
                            channel_dict["area%"] = l[l.index('Channel Name') + 5 + rows * 3 + i]
                            channel_dict["height"] = l[l.index('Channel Name') + 5 + rows * 4 + i]

                            channel_list.append(channel_dict)

                    mydict["channel_info"] = channel_list

                    final_list.append(mydict)

            return json.dumps(final_list)
        except Exception as e:
            return str(e)

    #Return All Informations from File
    def getAllData(self):
        try:
            fname = self.path

            final_list = []

            with fitz.open(fname) as doc:
                count = doc.page_count

                for i in range(0, count):
                    text = ""
                    page = doc[i]
                    text += page.get_text()
                    l = text.split("\n")

                    self.__fetchImage(fname, i, l[l.index('Sample Name:') - 1].strip())

                    mydict = {}

                    mydict['sample_name'] = l[l.index('Sample Name:') - 1].strip()

                    info_list = []
                    info_dict = {}

                    list1 = [
                        "sample_type",
                        "vial",
                        "injection#",
                        "injection_volume",
                        "run_time",
                        "acquired_by",
                        "sample_set_name",
                        "acq_method_set",
                        "processing_method",
                        "channel_name",
                        "proc_chnl_descr",
                        "data_acquired",
                        "data_processed",
                        "image_name",
                        "image_link"
                    ]

                    list2 = [
                        'Sample Type:',
                        'Vial:',
                        'Injection #:',
                        'Injection Volume:',
                        'Run Time:',
                        'Acquired By:',
                        'Sample Set Name:',
                        'Acq. Method Set:',
                        'Processing Method:',
                        'Channel Name:',
                        'Proc. Chnl. Descr.:',
                        'Date Acquired:',
                        'Date Processed:',
                        "image_name",
                        "image_link"
                    ]

                    for k, v in zip(list1, list2):
                        if k == "proc_chnl_descr" or k == "processing_method":
                            for el in l:
                                if el.startswith(v):
                                    info_dict[k] = el.split(':')[1].strip()
                        elif k == "run_time" or k == "acq_method_set" or k == "data_processed" or k == "channel_name":
                            info_dict[k] = l[l.index(v) + 1].strip()
                        elif k == "image_name":
                            info_dict[k] = str(i) + '_' + l[l.index('Sample Name:') - 1].strip()
                        elif k == "image_link":
                            info_dict[
                                k] = "SecEmpowerImages\\" + str(
                                i) + '_' + l[l.index('Sample Name:') - 1].strip() + ".jpg"
                        else:
                            if (l[l.index(v) - 1] not in list2) and (not l[l.index(v) - 1].strip() == ''):
                                info_dict[k] = l[l.index(v) - 1].strip()
                            else:
                                info_dict[k] = 'NIL'

                    info_list.append(info_dict)

                    mydict["sample_info"] = info_list

                    channel_list = []

                    channel_dict = {}

                    list3 = [
                        "channel_name",
                        "rt",
                        "area",
                        "area%",
                        "height"
                    ]

                    list4 = [
                        'Channel Name',
                        'RT',
                        'Area',
                        '% Area',
                        'Height'
                    ]

                    diff = len(l) - l.index('Channel Name')

                    if diff <= 5:
                        for k in list3:
                            if k == "channel_name":
                                channel_dict[k] = l[l.index('Channel Name') + 1]
                            else:
                                channel_dict[k] = 'NIL'

                        channel_list.append(channel_dict)
                    else:
                        rows = int(l[l.index('Channel Name') - 1])

                        for i in range(0, rows):
                            channel_dict = {}

                            channel_dict["channel_name"] = l[l.index('Channel Name') + 5 + i]
                            channel_dict["rt"] = l[l.index('Channel Name') + 5 + rows + i]
                            channel_dict["area"] = l[l.index('Channel Name') + 5 + rows * 2 + i]
                            channel_dict["area%"] = l[l.index('Channel Name') + 5 + rows * 3 + i]
                            channel_dict["height"] = l[l.index('Channel Name') + 5 + rows * 4 + i]

                            channel_list.append(channel_dict)

                    mydict["channel_info"] = channel_list

                    final_list.append(mydict)

            return json.dumps(final_list)
        except Exception as e:
            return str(e)

    #Return Images from the file
    def getImages(self):
        try:
            fname = self.path

            final_list = []

            with fitz.open(fname) as doc:
                count = doc.page_count

                for i in range(0, count):
                    text = ""
                    page = doc[i]
                    text += page.get_text()
                    l = text.split("\n")

                    self.__fetchImage(fname, i, l[l.index('Sample Name:') - 1].strip())

                    mydict = {}

                    mydict['sample_name'] = l[l.index('Sample Name:') - 1].strip()

                    info_list = []
                    info_dict = {}

                    list1 = [
                        "image_name",
                        "image_link"
                    ]

                    list2 = [
                        "image_name",
                        "image_link"
                    ]

                    for k, v in zip(list1, list2):
                        if k == "image_name":
                            info_dict[k] = str(i) + '_' + l[l.index('Sample Name:') - 1].strip()
                        if k == "image_link":
                            info_dict[
                                k] = "SecEmpowerImages\\" + str(
                                i) + '_' + l[l.index('Sample Name:') - 1].strip() + ".jpg"

                    info_list.append(info_dict)

                    mydict["image_info"] = info_list

                    final_list.append(mydict)

            return json.dumps(final_list)
        except Exception as e:
            return str(e)