"""
pip install xlsxwriter
"""

import sys
import os
import re
import time
import json
import requests
import argparse
import xlsxwriter
from collections import defaultdict
from utils import datetime_serial
from settings import *

def get_sheet_format():
    dic_format = {
            "text_wrap": True,
            "align": "center",
            "valign": "vcenter"
        }
    return dic_format

def set_sheet_column(ws, sheet_name):
    if sheet_name.startswith("ec2-instances"):
        lst_size = [25, 16, 22, 20, 16, 16, 12]
    elif sheet_name.startswith("ec2-reserved"):
        lst_size = [15, 15, 15, 15, 15, 15]
    elif sheet_name.startswith("rds-instances"):
        lst_size = [20, 25, 22, 15, 16, 16]
    elif sheet_name.startswith("rds-reserved"):
        lst_size = [25, 16, 22, 20, 16, 16, 18]
    elif sheet_name.startswith("cache-instances"):
        lst_size = [16, 30, 10, 15, 18, 18]
    elif sheet_name.startswith("cache-reserved"):
        lst_size = [16, 15, 22, 15, 15, 15, 18]
    elif sheet_name in ["ec2", "rds", "cache"]:
        lst_size = [20, 10, 10, 10]
    else:
        return

    for i in range(len(lst_size)):
        column = chr(65 + i)
        ws.set_column("{col}:{col}".format(col=column), lst_size[i])

def write2xlsx(worksheet, row, lst_data, cell_format):
    for col, item in enumerate(lst_data):
        worksheet.write(row, col, item, cell_format)

def dump2xlsxfile(lst_title, lst_ret, wb, sheet_name):
    cell_format = wb.add_format(get_sheet_format())
    ws = wb.add_worksheet(sheet_name)
    set_sheet_column(ws, sheet_name)
    row = 0

    dic_series_c, dic_series_w = get_summary(lst_ret)
    write2xlsx(ws, row, [DEF_SERIES_SUM], cell_format)
    row += 1
    write2xlsx(ws, row, TITLE_SERIES, cell_format)
    row += 1
    lst_s = sorted(dic_series_w, reverse=False)
    for s in lst_s:
        w = dic_series_w[s]
        write2xlsx(ws, row, [s, w], cell_format)
        row += 1
    ws.write(row, 0, "")
    row += 1

    write2xlsx(ws, row, [DEF_TYPE_SUM], cell_format)
    row += 1
    write2xlsx(ws, row, TITLE_SUMMARY, cell_format)
    row += 1
    #for (s, dic_v) in dic_series_c.items():
    for s in lst_s:
        dic_v = dic_series_c[s]
        for (t, c) in dic_v.items():
            weight = TYPE2WEIGHT[t]
            sum_weight = weight * c
            lst_data = [s, t, c, weight, sum_weight]
            write2xlsx(ws, row, lst_data, cell_format)
            row += 1
    ws.write(row, 0, "")
    row += 1

    write2xlsx(ws, row, [DEF_TYPE_LIST], cell_format)
    row += 1
    write2xlsx(ws, row, lst_title, cell_format)
    row += 1
    for dic_ret in lst_ret:
        lst_data = [str(dic_ret.get(title, "")) for title in lst_title]
        write2xlsx(ws, row, lst_data, cell_format)
        row += 1

def append2list(lst_ret, dic_ret):
    if dic_ret.get("State", "") == "retired":
        print("##### Filter Retired Records:")
        print(json.dumps(dic_ret))
        return
    if "Name" in dic_ret:
        name = dic_ret["Name"]
        if name and (name.endswith("-as") or name.endswith("_as")):
            dic_ret["AutoScale"] = 1
        else:
            dic_ret["AutoScale"] = 0
    if dic_ret.get("AutoScale", 0) == 1:
        print("##### Filter AutoScale Records:")
        print(json.dumps(dic_ret))
        return
    lst_ret.append(dic_ret)

def run_cmd(cmd_prefix, profile):
    cmd = cmd_prefix + " --profile " + profile
    print(cmd)

    lines = ""
    with os.popen(cmd, "r", 1) as fp:
        for line in fp:
            line = line.strip()
            if len(line) < 1:
                continue
            lines += line

        fp.close()
    #print(lines)
    if len(lines) > 0:
        lst_ret = json.loads(lines)
        lst_new = []
        for one in lst_ret:
            if type(one) is list:
                for dic_inst in one:
                    append2list(lst_new, dic_inst)
            else:
                append2list(lst_new, one)
        lst_ret = lst_new
    else:
        lst_ret = []
    return lst_ret

def get_summary(lst_ret_detail):
    dic_series_c = defaultdict(lambda:defaultdict(float))
    dic_series_w = defaultdict(float)
    for dic_ret in lst_ret_detail:
        lst_type = dic_ret.get("Type", "").split(".")
        if len(lst_type) < 2:
            continue
        count = dic_ret.get("Count", 1)
        count = int(count)
        series = ".".join(lst_type[0:-1])
        s_type = lst_type[-1]
        sum_weight = TYPE2WEIGHT[s_type] * count
        dic_series_c[series][s_type] += count
        dic_series_w[series] += sum_weight
    return dic_series_c, dic_series_w

def proc(cmd, profile, titles, wb, sheet_name):
    lst_ret_detail = run_cmd(cmd, profile)
    # format datetime fields
    lst_field = ["Create", "Start", "End"]
    for i in range(len(lst_ret_detail)):
        for field in lst_field:
            if field in lst_ret_detail[i]:
                dt = lst_ret_detail[i][field]
                dt = datetime_serial(dt, True, "%Y-%m-%d")
                lst_ret_detail[i][field] = dt
        if "Time" in lst_ret_detail[i]:
            secs = int(lst_ret_detail[i]["Time"])
            days = int(secs/86400)
            lst_ret_detail[i]["Time"] = "{} days".format(days)
    dump2xlsxfile(titles, lst_ret_detail, wb, sheet_name)

def get_ret(profile):
    today = datetime_serial(None, False, "%Y%m%d")
    dir_today = "{}/{}".format(DEF_OUT_DIR, today)
    if not os.path.isdir(dir_today):
        os.makedirs(dir_today)
    file_ot = "{}/{}.xlsx".format(dir_today, profile)
    wb = xlsxwriter.Workbook(file_ot)
    # ec2
    cmd = "aws ec2 describe-instances --filters Name=instance-state-code,Values=16 --query 'Reservations[*].Instances[*].{Instance:InstanceId,Address:PrivateIpAddress,Type:InstanceType,AZ:Placement.AvailabilityZone,Name:Tags[?Key==`Name`]|[0].Value,Owner:Tags[?Key==`Owner`]|[0].Value}' --output json"
    proc(cmd, profile, TITLE_EC2_INST, wb, "ec2-instances")
    cmd = "aws ec2 describe-reserved-instances --filters Name=state,Values=active --query 'ReservedInstances[*].{Type:InstanceType,Count:InstanceCount,OS:ProductDescription,Offer:OfferingClass,Start:Start,End:End}' --output json"
    proc(cmd, profile, TITLE_EC2_RESV, wb, "ec2-reserved")
    # rds
    cmd = "aws rds describe-db-instances --query 'DBInstances[*].{Engine:Engine,Name:DBInstanceIdentifier,Status:DBInstanceStatus,Create:InstanceCreateTime,Type:DBInstanceClass,Cluster:DBClusterIdentifier}' --output json"
    proc(cmd, profile, TITLE_RDS_INST, wb, "rds-instances")
    cmd = "aws rds describe-reserved-db-instances --query 'ReservedDBInstances[*].{State:State,Class:ProductDescription,Start:StartTime,Type:DBInstanceClass,Offer:OfferingType,Count:DBInstanceCount,Time:Duration}' --output json"
    proc(cmd, profile, TITLE_RDS_RESV, wb, "rds-reserved")
    # cache
    cmd = "aws elasticache describe-cache-clusters --query 'CacheClusters[*].{Node:CacheClusterId,Status:CacheClusterStatus,Type:CacheNodeType,Engine:Engine,Num:NumCacheNodes,Create:CacheClusterCreateTime}' --output json"
    proc(cmd, profile, TITLE_CACHE_INST, wb, "cache-instances")
    cmd = "aws elasticache describe-reserved-cache-nodes --query 'ReservedCacheNodes[*].{Type:CacheNodeType,Start:StartTime,Time:Duration,Count:CacheNodeCount,Class:ProductDescription,Offer:OfferingType,State:State}' --output json"
    proc(cmd, profile, TITLE_CACHE_RESV, wb, "cache-reserved")
    wb.close()

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument(
            "-p", "--profile", type=str,
            help="op_ri_9674"
        )
    args = parse.parse_args()
    profile = args.profile
    get_ret(profile)

    #cmd = ""
    # python3 get_aws_ri.py --profile op_ri_bj

