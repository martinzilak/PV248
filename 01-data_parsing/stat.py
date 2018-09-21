#!/usr/bin/env python

import sys
import re
import codecs
from collections import Counter

MODES = ['composer', 'century']

if len(sys.argv) != 3:
    raise ValueError('Wrong number of arguments passed')
if sys.argv[2] not in MODES:
    raise ValueError('Unknown mode passed, possible values are: ', MODES)

f = codecs.open(sys.argv[1], 'r', encoding = "cp1250", errors='ignore')
mode = sys.argv[2]

ctr = Counter()

#stolen from https://stackoverflow.com/a/36977549
suf = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))

def century(year):
    c = year // 100 + 1
    return(suf(c) + ' century')

for line in f:
    if mode == 'composer':
        rcomposer = re.compile(r"Composer:\s(.*)\n")
        ryear = re.compile(r"(.*?)\(.*?\)")
        mcomposer = rcomposer.match(line)
        if mcomposer:
            for name in mcomposer.group(1).split(';'):
                myear = ryear.match(name)
                if myear:
                    ctr[myear.group(1).strip()] += 1
                else:
                    ctr[name.strip()] += 1
    if mode == 'century':
        r = re.compile(r"\sYear:\s(\d*)\n")
        m = r.match(line)
        if m:
            y = append(m.group(1).strip())
            if len(y) > 0:
                ctr[century(int(y))] += 1

for k, v in ctr.items():
    print(k, ': ', v, sep = '')

'''
found year formats:
XXXX
XXXX/XXXX
XXth century
XXXX Leipzig
ca XXXX
ca. XXXX
XXXX--XXXX
XXXX, Hamburg
'''

