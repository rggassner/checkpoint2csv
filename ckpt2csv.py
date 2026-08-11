#!venv/bin/python3
#pylint: disable=too-many-branches
"""
Check Point Log Parser

This script reads raw Check Point log entries from standard input (stdin), extracts specific
fields, and outputs them in either a key-value format (Checkpoint style) or a CSV format.
It automatically converts Unix timestamps into human-readable local time strings.

Fields extracted: time, src, s_port, dst, service, xlatesrc.

Usage:
    cat logs.txt | python3 script.py [options]

Options:
    -c, --checkpoint    Output in key="value" format (default is CSV).
    -r, --require-all   Filter output to only include log lines where every specified
                        field was successfully found.

Example:
    tail -f /var/log/messages | python3 script.py --checkpoint --require-all
"""
import sys
import re
import argparse
from datetime import datetime

fields_list = "time,user,src,s_port,dst,service,xlatesrc,office_mode_ip,action".split(',')

def process_logs(output_format, require_all):
    """
    Processes logs from stdin. 
    output_format: 'ckp' or 'csv'
    require_all: Boolean, if True only lines with all fields are printed.
    """
    if output_format == 'csv':
        # Print CSV Header
        header = []
        for f in fields_list:
            if f == 'time':
                header.extend(['time_formatted', 'time'])
            else:
                header.append(f)
        print(",".join(header))

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        extracted = {}
        found_count = 0

        for field in fields_list:
            result = re.search(r' ' + field + r'="(.*?)"', line)
            if result:
                extracted[field] = result.group(1)
                found_count += 1
            else:
                extracted[field] = None

        # Filter logic: if require_all is True, check if we found everything
        if require_all and found_count < len(fields_list):
            continue

        # Output Generation
        if output_format == 'ckp':
            lineout = ''
            for field in fields_list:
                val = extracted[field]
                if val is not None:
                    if field == 'time':
                        fmt_time = datetime.fromtimestamp(
                                float(val)).astimezone().isoformat(sep=' ', timespec='seconds'
                                )
                        lineout += f'time_formatted="{fmt_time}" time="{val}" '
                    else:
                        lineout += f'{field}="{val}" '
            if lineout:
                print(lineout.strip())

        else: # CSV format
            row = []
            for field in fields_list:
                val = extracted[field]
                if field == 'time':
                    if val:
                        fmt_time = datetime.fromtimestamp(
                                float(val)).astimezone().isoformat(sep=' ', timespec='seconds'
                                )
                        row.extend([fmt_time, val])
                    else:
                        row.extend(['', ''])
                else:
                    row.append(val if val is not None else '')
            print(",".join(row))

if __name__ == "__main__":
    ARGPARSER = argparse.ArgumentParser(description='Parse Check Point logs from stdin.')
    ARGPARSER.add_argument('-c', '--checkpoint', action='store_true',
                           help='Output in checkpoint format instead of csv.')
    ARGPARSER.add_argument('-r', '--require-all', action='store_true',
                           help='Only output lines that contain all specified fields.')
    args = ARGPARSER.parse_args()

    FMT = 'ckp' if args.checkpoint else 'csv'
    process_logs(FMT, args.require_all)
