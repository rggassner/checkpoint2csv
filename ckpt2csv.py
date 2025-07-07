#!/usr/bin/python3
import sys,re,tzlocal,argparse
from datetime import datetime

fields="time,src,s_port,dst,service,service_id,action,xlatesrc"

def ckp_output():
    """
    Reads lines from stdin and extracts defined fields in Check Point log format.

    For each line, it parses the specified fields and prints them in key="value" format.
    Additionally, for the `time` field, it appends a `time_formatted` field with a human-readable timestamp.
    """
    for line in sys.stdin:
        line=line.strip()
        lineout=''
        for field in fields.split(','):
            result=re.search(r' '+field+'="(.*?)"',line)
            if result:
                if field == 'time':
                    lineout=lineout+'time_formatted="'+str(datetime.fromtimestamp(float(result.group(1)),tzlocal.get_localzone()))+'" '+field+'="'+result.group(1)+'" '
                else:
                    lineout=lineout+field+'="'+result.group(1)+'" '
        print('{}'.format(lineout))
        lineout=''

def csv_header():
    """
    Prints a CSV header line based on the defined fields.

    Includes an additional `time_formatted` column for the `time` field.
    """
    header=''
    for field in fields.split(','):
        if field == 'time':
            header=header+'time_formatted,time,'
        else:
            header=header+field+','
    header=header[:-1]
    print(header)

def csv_output():
    """
    Reads lines from stdin and extracts defined fields, outputting them in CSV format.

    Includes a human-readable `time_formatted` field for the `time` value.
    If a field is missing from the log line, it leaves the corresponding CSV column empty.
    """
    csv_header()
    for line in sys.stdin:
        line=line.strip()
        lineout=''
        for field in fields.split(','):
            result=re.search(r' '+field+'="(.*?)"',line)
            if result:
                if field == 'time':
                    lineout=lineout+str(datetime.fromtimestamp(float(result.group(1)),tzlocal.get_localzone()))+','+result.group(1)+','
                else:
                    lineout=lineout+result.group(1)+','
            else:
                lineout=lineout+','
        lineout=lineout[:-1]
        print('{}'.format(lineout))
        lineout=''

argParser = argparse.ArgumentParser()
argParser.add_argument('-c','--checkpoint',action='store_true',help='Output in checkpoint format instead of csv.')
argParser.set_defaults(checkpoint=False)
args=argParser.parse_args()

ckp=args.checkpoint

if ckp:
    ckp_output()
else:
    csv_output()

