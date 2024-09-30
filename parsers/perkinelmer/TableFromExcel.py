import os
import pandas as pd
import json
import xlrd
from openpyxl import load_workbook
import io
from xlwt import Workbook

## Python Version: Python 3.11.3 ##

########  Main Method : Start ##########
    
def fetch_data_from_excel(wbname, sheetname, start_row_index):
    """
    Input - 
    
    Passed Arguments are-
    1. The workbook path.
    2. The sheet name.
    3. The start row index in the excelsheet from which the table starts(the starting header row which
        will be considered as the key values)

    Output-
    The list which contains the dictionaries in which the keys are the header row of the table
    and each row of the table becomes each dictionary values.

    """
    output_list=[]
    fname=wbname
    if wbname.endswith('.xlsx') or wbname.endswith('.XLSX'):
        df=pd.read_excel(fname, engine='openpyxl', sheet_name=sheetname, skiprows=(start_row_index-1))
    if wbname.endswith('.xls') or wbname.endswith('.XLS'):
        df=pd.read_excel(fname, engine='xlrd', sheet_name=sheetname, skiprows=(start_row_index-1))
    row=0
    excel_row_dict_keys_list=df.columns.tolist()
    excel_row_dict_keys_list=[li for li in excel_row_dict_keys_list if not (li.startswith('Unnamed:'))]
    total_rows_in_df=df.shape[0]
    while row<total_rows_in_df and str(df.iloc[row][excel_row_dict_keys_list[0]]).strip()!='nan':
        row_val=df.iloc[row]
        excel_row_dict={}
        for excel_row_dict_key in excel_row_dict_keys_list:
            excel_row_dict[excel_row_dict_key.strip()]= str(row_val[excel_row_dict_key]).strip()
        output_list.append(excel_row_dict)
        row=row+1
    return output_list

########  Main Method : End ##########
