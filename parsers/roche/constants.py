"""
constants file for cedex instrument
"""
SOH = "\x01"
STX = "\x02"
ETX = "\x03"
EOT = "\x04"
LF = "\x0A"

INSTRUMENT_CODE = "14"
INSTRUMENT_IDENTIFIER = "COBAS_INTEGRA   "
SPACE = " "
IDLE_BLOCK_CODE = "00"  # sync block code
BLOCK_CODE = "09"  # generic block code
RESULT_REQUEST_BLOCK_CODE = "09"
RESULT_REQUEST_LINE_CODE = "10"
RESULT_REQUEST_RESULTTYPESELECTOR = "07"
HOST_IDENTIFIER = "CEDEX BIO HT   "
ERROR_BLOCK_CODE = "99"

UTF8 = "UTF-8"
JSON = "Json"

ORDERID_CODE = "53"
SAMPLENAME_CODE = "56"
TESTID_CODE = "55"
RESULT_CODE = "00"
VALIDATION_CODE = "14"
TESTEXECUTION_CODE = "17"
CASSETTE_CODE = "18"
CALIBRATION_CODE = "19"
CONTROL_DATA = "21"
ABSORBANCE_CODE = "06"
FPRAWDATA_CODE = "08"
ISERAWDATA_CODE = "09"
RERUN_CODE = "27"

ORDERID = "Order ID"
SAMPLENAME = "Sample Name"
TESTID = "Test ID"
TESTNAME = "Test Name"
VALIDATION_STATUS = "Validation Status"
RESULT_DATA = "Result Data"
TEST_EXECUTION = "Test Execution"
CASSETTE = "Cassette Information"
CALIBRATION = "Calibration Information"
CONTROL = "Control Information"
ABSORBANCE_RAWDATA = "Absorbance Rawdata"
FP_RAWDATA = "FP Raw Data"
ISE_RAWDATA = "ISE Raw Data"
RERUN = "Rerun Status"

RAW_DATA = "Raw data"

# LOG Message
RESPONSE_FILE_READ = "Response file read"
OUTPUT_FILE_CREATED = 'Output file created'
NO_RESPONSE = "Exception occurred-No response obtained from instrument"
ERROR_IN_JSON = "Exception occurred-Error forming json-Check the field values"
CANNOT_OBTAIN_FULL_RESPONSE = "Cannot obtain full response"
RESPONSE_FILE_CREATED = "Response file created"
OPEN_SERIALPORT = "Opening the serial port"
ERROR_OPENING_SERIALPORT = "Error opening port"
IDLEBLOCK_ENCOUNTERED = "Idle block encountered"
ERROR_BLOCK_RESPONSE = "Exception getting error block"
DATE_NOT_CORRECT_FORMAT = "Date is not in correct format"
LINECODE_DESCRIPTION_NOTFOUND = "Linecode description not found"
INSTRUMENT_RESPONSE_READ = "Instrument Response read"
INTERNAL_SERVER_ERROR = 'Internal Server Error'
SYNC_REQUEST_ERROR="Error in Sync block request"

BYTES_EOT = b'\x04\n'
BYTES_EXTRA_CHARACTERS = b'\xff\xfd\x03\xff\xfb\x03\xff\xfb\x01'

RESPONSE_CODE_500 = "500"
RESPONSE_CODE_200 = "200"

TIME_FORMAT = "%d-%m-%y-%H-%M-%S"
