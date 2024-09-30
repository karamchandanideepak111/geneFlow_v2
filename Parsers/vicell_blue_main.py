import datetime
import os
import re
#import codecs
import sys 
import array
sys.path.append('.')
#from codecs import utf_8_encode
import logging
import config as config
from service_exception import ServiceException
from collections import OrderedDict
import datetime as dateTime
import constants as constants
import json
import csv
 
"""
    Global input, output data param. 
    set by python interpreter in Java code. 
"""
filename = "vicell_blue.py"
"""
    outPutData we send python success response to java
    errorOutPut we send error response
"""
sampleCount = ""
outPutData = ""
reducedoutPutData = ""
errorOutPut = ""
EXT_INPUT = ext_input
INSTRUMENT_NAME = ext_instrument_name
INSTRUMENT_VERSION = ext_instrument_version
INSTRUMENT_ID = ext_instrument_id
RECEIVER = ext_receiver
DEBUG_MODE = ext_debug_mode
LOG_FILE_NAME = ext_log_file_name

logging.getLogger("py4j").setLevel(logging.ERROR)
logging.raiseExceptions = False
# create logger
logger = logging.getLogger("vicell_blue")
logger.setLevel(logging.DEBUG)
# create formatter
message_format = '%(asctime)s  %(levelname)s  %(filename)s:%(lineno)d - %(message)s'
formatter = logging.Formatter(message_format)
if DEBUG_MODE.lower() == "true":
    fh = logging.FileHandler(config.LOG_PATH + LOG_FILE_NAME)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

# 'application' code
#logger.debug('debug message')

logger.info(config.LOG_PYTHON_STARTED_MESSAGE)

def prepare_reduced_output(resultDataDict, imageTotalDataDict):
    logger.info(constants.ENTERING_IN_PREPARE_REDUCED_OUTPUT)
    global errorOutPut
    try:
        updatedResDict = OrderedDict()
        updatedResDict[constants.SAMPLE_ID] = ""
        for key, value in resultDataDict.items():
            if constants.SAMPLE_ID in key:
                updatedResDict[constants.SAMPLE_ID] = resultDataDict[key]
        
        updatedResDict[constants.DATE_TIME] = resultDataDict[constants.DATE_TIME]
        updatedResDict[constants.CEL_TYPE] = resultDataDict[constants.CEL_TYPE]
        updatedResDict[constants.IMAGES] = {constants.UNIT : "", constants.VALUE : resultDataDict[constants.IMAGES]}

        #updatedResDict["Analysis by"] = resultDataDict["Analysis by"]
        
        resultListData = []
        for key , value in imageTotalDataDict.items():
            if key.lower() == constants.IMAGE_NUMBER:  
                del key  
            else:
                attr = OrderedDict()
                #key = str(key).decode('utf-8')
                if value.replace(".", "").isnumeric():
                    if value.isdigit() :
                        value = int(value)
                    else:
                        value = float(value)
                        
                attr[constants.VALUE] = value          
                if "(" in key:
                    start = key.find('(')
                    end = key.find(')')
                    keyUnit = key[start+1:end]
                    key = key[:start-1]+key[end+1:]
                    keyCode = keyUnit
                    attr[constants.UNIT] =  keyUnit                                                                                                        
                else:
                    attr[constants.UNIT] = ""
                
                updatedResDict[key] = attr 
                              
        resultListData.append(updatedResDict)
        
        logger.info(constants.EXISTING_FROM_PREPARE_REDUCED_OUTPUT)
        return resultListData
    except Exception as exception_message:
        logger.info("Exception occurred in vicell_blue_json_form: -%s")
        logger.info(exception_message)

        errorOutPut ={"code": 500,"message": constants.ERROR_INVALID_DATA}
        return errorOutPut
 
def raw_data_formation():
    global LOG_FILE_NAME, outPutData, errorOutPut, reducedoutPutData, sampleCount 
    #try:
    linecode_complete_data_array = []
    jsonArray = []
    vicellBlueRawDataArray = []
    resultRawDataArray = []
    regentRawDataArray = []
    imageRawDataArray = []
    imageTotalRawDataArray = []
    indexOfSampleId = 0;
    indexOfReagent = 0;
    indexOfImage = 0 ;
    indexOfTotal = 0 ;
    successOutput = OrderedDict()
    reducedOutput = OrderedDict()
    
    logger.info(constants.ENTER_IN_RAWDATA_FORMATION)
    byte_array = bytearray(ext_input)
    instrument_response = str(byte_array)
    logger.info(constants.INSTRUMENT_RESPONSE_PRINT);
    logger.info(instrument_response)
    instrument_response = instrument_response.replace("\r", "")
    dataArray = instrument_response.split("\n")
    dataArray=[response for response in dataArray if response.strip()]
    for i in range(len(dataArray)):
        line = dataArray[i] 
        if '\xef\xbb\xbf' in line:
            line = str(line).replace('\xef\xbb\xbf','')
        vicellBlueRawDataArray.append(line)
     
        if constants.SAMPLE_ID  in  line:
            indexOfSampleId =  i  
        if constants.REAGENT  in  line:
            indexOfReagent =  i  
        if constants.IMAGE_NUMBER  in  line:
            indexOfImage =  i  
        if constants.TOTAL  in  line:
            indexOfTotal =  i     
    print("indexOfReagent" + str(indexOfReagent) + " indexOfImage " + str(indexOfImage) +" indexOfTotal " + str(indexOfTotal))
    if indexOfReagent != 0 and  indexOfImage  != 0 and  indexOfTotal != 0:
        pass
    else:
        raise ServiceException(constants.ERROR_IN_JSON,constants.RESPONSE_CODE_500)
    #-----total list prepare
    imageTotalRawDataArray.append(vicellBlueRawDataArray[indexOfImage])
    imageTotalRawDataArray.append(vicellBlueRawDataArray[indexOfTotal])
    
    #---------------------------
    #-------sample data
    resultRawDataArray.append(vicellBlueRawDataArray[0])
    resultRawDataArray.append(vicellBlueRawDataArray[1])   
    for i in range(indexOfReagent, indexOfImage):
        regentRawDataArray.append(vicellBlueRawDataArray[i])
        
    for i in range(indexOfImage, indexOfTotal-1):
        imageRawDataArray.append(vicellBlueRawDataArray[i])
    
    #-----------preparing Dictonary
    #---------------total
    imageTotalDataArray = []
    for element in csv.DictReader(imageTotalRawDataArray):
        imageTotalDataArray.append(element)
    #--------------------results    
    #resultDataArray = []
    #for element in csv.DictReader(resultRawDataArray):
        #resultData = element
        #dateTimeObj = datetime.datetime.strptime(resultData["Analysis date/time"],"%m/%d/%Y %I:%M:%S %p").strftime("%m/%d/%Y %H:%M:%S")
        #resultData.update({"Analysis date/time":dateTimeObj})
        #resultDataArray.append(resultData)
    
    resultDataDict = OrderedDict()
    updatedResultData = OrderedDict()
    reader = csv.reader(resultRawDataArray)
    headers = next(reader)
    for row in reader:
       resultDataDict = OrderedDict(zip(headers, row))
    
    dateTimeObj = datetime.datetime.strptime(resultDataDict[constants.ANALYSIS_DATE_TIME],constants.RAW_DATA_DATE_FORMAT).strftime(constants.CONVERTED_DATA_DATE_FORMAT)
    del resultDataDict[constants.ANALYSIS_DATE_TIME]
    resultDataDict.update({constants.DATE_TIME:dateTimeObj})
    #--------------------------
    updatedResultData[constants.SAMPLE_ID] = resultDataDict[constants.SAMPLE_ID]
    updatedResultData[constants.DATE_TIME] = resultDataDict[constants.DATE_TIME]
    for key, value in resultDataDict.items():
        if key not in [constants.ANALYSIS_BY, constants.SAMPLE_ID]:
            updatedResultData[key] = value
            
    #-------------regents
    regentDataArray = []
    reader = csv.reader(regentRawDataArray)
    headers = next(reader)
    for row in reader:
       regentDataArray.append(OrderedDict(zip(headers, row)))
    expiradateTimeObj = datetime.datetime.strptime(regentDataArray[0][constants.EXPIRATION],constants.RAW_DATA_DATE_FORMAT).strftime(constants.CONVERTED_DATA_DATE_FORMAT)
    regentDataArray[0].update({constants.EXPIRATION:expiradateTimeObj})
    
    inServiceTimeObj = datetime.datetime.strptime(regentDataArray[0][constants.IN_SERVICE_DATE],constants.RAW_DATA_DATE_FORMAT).strftime(constants.CONVERTED_DATA_DATE_FORMAT)
    regentDataArray[0].update({constants.IN_SERVICE_DATE:inServiceTimeObj})
    
    effExpiraTimeObj = datetime.datetime.strptime(regentDataArray[0][constants.EFFECTIVE_EXPIRATION],constants.RAW_DATA_DATE_FORMAT).strftime(constants.CONVERTED_DATA_DATE_FORMAT)
    regentDataArray[0].update({constants.EFFECTIVE_EXPIRATION:effExpiraTimeObj})
    #-----------------------------image data
    imageDataArray = []
    reader = csv.reader(imageRawDataArray)
    headers = next(reader)
    for row in reader:
       imageDataArray.append(OrderedDict(zip(headers, row)))
    
                
    analysisBy = resultDataDict[constants.ANALYSIS_BY]
    metadata =  prePareMetaData(analysisBy)
    #--------------Result
    finalresultArray = prepare_reduced_output(resultDataDict,imageTotalDataArray[0] )
    #----------success result 
    sampleCount = len(finalresultArray)
    successOutput[constants.METADATA] = metadata
    successOutput[constants.RESULTS] = finalresultArray
    successOutput[constants.REAGENT] = regentDataArray
    successOutput[constants.IMAGEDATA] = imageDataArray
    #----------------reduced result
    reducedOutput[constants.METADATA] = metadata
    reducedOutput[constants.RESULTS] = finalresultArray
    reducedOutput[constants.REAGENT] = regentDataArray
    
    outPutData = json.dumps([successOutput],indent = 6)
    reducedoutPutData = json.dumps([reducedOutput], indent = 6)
    logger.info(constants.SUCCESS_OUTPUT)
    logger.info(outPutData)
    logger.info(constants.REDUCED_OUTPUT)
    logger.info(reducedoutPutData)
    
    logger.info(constants.EXIT_FROM_RAW_DATA_FORMATION)
    logger.info(config.LOG_PYTHON_END_MESSAGE)
    # except Exception as exception_message:
    #     logger.info("Error in Raw data formation method." + str( exception_message))
    #     errorOutPut ={"code": 500,"message": constants.ERROR_INVALID_DATA}
    #     return None

def prePareMetaData(analysisBy):
    metaDict = OrderedDict()        
    metaDict[constants.INSTRUMENT_NAME] = INSTRUMENT_NAME
    metaDict[constants.INSTRUMENT_ID] = INSTRUMENT_ID
    metaDict[constants.INSTRUMENT_VERSION] = INSTRUMENT_VERSION        
    metaDict[constants.RECEIVER] = RECEIVER
    metaDict[constants.ANALYSIS_BY] = analysisBy
    
    return metaDict
 
def formatedTotalImageData(totalImageDataList):
    resultListData = []
    for key , value in totalImageDataList.items():
                
        attr = OrderedDict()
        #key = str(key).decode('utf-8')
        if value.replace(".", "").isnumeric():
            if value.isdigit() :
                value = int(value)
            else:
                value = float(value)
                
        attr[constants.VALUE] = value          
        if "(" in key:
            keyList = key.split(" (")
            keyUnit = keyList[1].replace(")", "")
            key = keyList[0]
            keyCode = keyUnit
            attr[constants.UNIT] =  keyUnit.decode('utf-8')                                                                                                        
        else:
            attr[constants.UNIT] = ""
        
        updatedResDict[key] = attr 
                          
        resultListData.append(updatedResDict) 
    return resultListData
     
if __name__ == "__main__":
    raw_data_formation()