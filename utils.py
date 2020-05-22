import sys
import time
import traceback
from datetime import date
from datetime import datetime
from datetime import timezone
from dateutil.parser import parse
from dateutil import tz
import socket
import hashlib
import math

'''
pip3 install python-dateutil
'''
# 24/Mar/2018 12:47:48 +0000
# 24/Mar/2018 12:47:48
def conv_date(s_date):
    to_zone = tz.gettz('Asia/Shanghai')
    dt = parse(s_date)
    print(dt)
    print(dt.tzinfo)
    if dt.tzinfo:
        local = dt.astimezone(to_zone)
    else:
        local = dt
    print(local)
    s_date = local.strftime("%Y-%m-%d %H:%M:%S")
    return s_date

def datetime_serial(obj=None, keep_null=False, t_format=None):
    """JSON serializer for objects not serializable by default json code"""

    to_zone = tz.gettz('Asia/Shanghai')
    if obj is None:
        if keep_null:
            return None
        obj = int(time.time())

    if not t_format:
        t_format = "%Y-%m-%dT%H:%M:%S+0800"
    if isinstance(obj, datetime):
        dt = obj
        if dt.tzinfo:
            local = dt.astimezone(to_zone)
        else:
            local = dt
        #serial = local.strftime("%Y-%m-%d %H:%M:%S")
        serial = local.strftime(t_format)
        return serial
    #raise TypeError("Type %s not serializable." % type(obj))

    if isinstance(obj, int):
        if len(str(obj))==16: # 微秒
            obj = obj/1000000
        elif len(str(obj))==13: # 毫秒
            obj = obj/1000
        elif len(str(obj))==10: # 秒
            pass
        else:
            return obj
        dt = datetime.utcfromtimestamp(obj)
        #local = dt.astimezone(to_zone)
        local = dt.replace(tzinfo=timezone.utc).astimezone(to_zone)
        s_date = local.strftime(t_format)
        return s_date

    if isinstance(obj, str):
        if not obj:
            return ""
        if "0000-00-00 00:00:00.000000" == obj:
            return ""
        dt = parse(obj)
        if dt.tzinfo:
            local = dt.astimezone(to_zone)
        else:
            local = dt
        s_date = local.strftime(t_format)
        return s_date
    return obj

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    numargs = len(sys.argv) - 1
    if numargs < 1:
        print("usage: python3 {} '24/Mar/2018 12:47:48 +0000'".format(sys.argv[0]))
        sys.exit(1)
    print(datetime_serial(sys.argv[1]))
    #conv_date(sys.argv[1])

