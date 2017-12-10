#!/usr/bin/python

"""Pipe strace to this script to generate write counts.  inotify is
probably a better tool for this, but that isn't always available.
# strace -fp PID -y 2>&1 | egrep -v 'lseek|read' | grep write\( | strace-aggregate-counts.py
NB: Produces boatloads of output.
"""

import re
import sys
from collections import defaultdict
import json



totals = defaultdict(int)
path = re.compile('.*whisper/collectd/[^/]*/([^/]*)/.*')
for line in sys.stdin:
    m = path.search(line)
    if m:
        totals[m.group(1)] += 1
        for key, value in sorted(totals.iteritems(), key=lambda (k,v): (v,k), reverse=False):
            print "%s %s" % (value, key)
        print ''
