"""
pip install pandas
pip install xlrd
pip install xlsxwriter
"""

import sys
import os
import re
import time
import json
import requests
import argparse
import pandas as pd
import xlsxwriter
from collections import defaultdict
from utils import datetime_serial
from settings import *
from get_aws_ri import *


def load_xlsx(file_xlsx, sheet_name, flag, lst_title):
    lst_ret = []
    is_detail = True if flag is None else False
    df = pd.read_excel(file_xlsx, sheet_name=sheet_name)
    for i in df.index.values:
        lst_row = df.loc[i].to_list()
        if lst_row[0] == flag:
            is_detail = True
            continue
        if not is_detail:
            continue
        if lst_row == lst_title:
            continue
        if pd.isnull(lst_row[0]):
            break
        lst_ret.append(dict(zip(lst_title, lst_row)))
    return lst_ret

def get_dic(lst_in, key_flag, set_keys):
    """
    key_flag:
        Series: Get SumWeight
        Series.Type: Get Count
    """
    dic_ret = {}
    for d in lst_in:
        if "Series" == key_flag:
            k = "{}".format(d["Series"])
            dic_ret[k] = d["SumWeight"]
        else:
            k = "{}.{}".format(d["Series"], d["Type"])
            dic_ret[k] = d["Count"]
        set_keys.add(k)
    return dic_ret

def compare(lst_it, lst_ri, key_flag):
    lst_ret = []
    set_keys = set([])
    d_it = get_dic(lst_it, key_flag, set_keys)
    d_ri = get_dic(lst_ri, key_flag, set_keys)
    set_keys.remove(key_flag)
    lst_keys = sorted(list(set_keys))
    for key in lst_keys:
        val_inst = int(d_it.get(key, 0))
        val_ir = int(d_ri.get(key, 0))
        s_memo = g_dic_memo.get(key, "")
        lst_ret.append([key, val_inst, val_ir, val_inst-val_ir, s_memo])
    return lst_ret

def dump_table(file_in, sepa, ws, cell_format, 
        s_type, key_flag, row, title_in, title_ot):
    sheet_it = "{}-instances".format(s_type)
    sheet_ri = "{}-reserved".format(s_type)
    lst_it = load_xlsx(file_in, sheet_it, sepa, title_in)
    lst_ri = load_xlsx(file_in, sheet_ri, sepa, title_in)
    lst_ret = compare(lst_it, lst_ri, key_flag)

    write2xlsx(ws, row, title_ot, cell_format)
    row += 1
    for lst_line in lst_ret:
        write2xlsx(ws, row, lst_line, cell_format)
        row += 1
    ws.write(row, 0, "")
    row += 1
    return row

def dump_summary(s_type, file_in, wb):
    cell_format = wb.add_format(get_sheet_format())
    ws = wb.add_worksheet(s_type)
    set_sheet_column(ws, s_type)
    row = 0

    # Series Weight
    title_in = TITLE_SERIES
    title_ot = ["Series", "Weight\nINST", "Weight\nRI", "Buy", "Memo"]
    row = dump_table(file_in, None, ws, cell_format, 
            s_type, "Series", row, title_in, title_ot)

    # Type Count
    title_in = TITLE_SUMMARY
    title_ot = ["Type", "Count\nINST", "Count\nRI", "Buy"]
    row = dump_table(file_in, DEF_TYPE_SUM, ws, cell_format, 
            s_type, "Series.Type", row, title_in, title_ot)


def summary(filename_in, filename_ot):
    today = datetime_serial(None, False, "%Y%m%d")
    dir_today = "{}/{}".format(DEF_OUT_DIR.rstrip('/'), today)
    if not os.path.isdir(dir_today):
        os.makedirs(dir_today)
    file_in = "{}/{}.xlsx".format(dir_today, filename_in)
    file_ot = "{}/{}.xlsx".format(dir_today, filename_ot)
    if not os.path.exists(file_in):
        print("File not exist. {}".format(file_in))
        return
    wb = xlsxwriter.Workbook(file_ot)
    #lst_type = ["ec2"]
    lst_type = ["ec2", "rds", "cache"]
    for s_type in lst_type:
        dump_summary(s_type, file_in, wb)
    wb.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 {} file_in file_out".format(sys.argv[0]))
        sys.exit(0)
    summary(sys.argv[1], sys.argv[2])
    # python3 summary.py op_bj summary_bj

