#!/usr/bin/python3

import argparse
import json
import re
from collections import defaultdict
from subprocess import Popen, PIPE

# Don't report on anything using less than 10 MB
THRESHOLD = 10
if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--rss", action="store_true", default=False, help="aggregate RSS(used physical memory)")
    group.add_argument("-v", "--size", action="store_true", default=False, help="aggregate SIZE(estimated swap usage)")
    args = parser.parse_args()
    if args.rss or (not args.rss and not args.size):
        metric_name = 'rss'
    else:
        metric_name = 'size'
    process = Popen(["ps", "-eo", "{},comm".format(metric_name)], stdout=PIPE)
     
    # map process_name -> memory used by all processes
    totals = defaultdict(int)
    grand_total = 0
    sout = process.communicate()[0].decode()
    for line in sout.split('\n')[1:]:
        i = line.strip().split(' ')
        if len(i)==2:
            totals[i[1]] += int(i[0])
            grand_total += int(i[0])
    print('omitting processes using less than {} MiB.'.format(THRESHOLD))    
    print('{:>10} {}'.format('MiB', 'Command'))
    for command in sorted(totals, key=totals.get):
          if totals[command]/1024.0 >= THRESHOLD:
              print('{:10} {}'.format(int(totals[command]/1024.0), command))
    print('\nSum of "{}" sizes for all processes: {} MiB'.format(metric_name, int(grand_total/1024.0)))

