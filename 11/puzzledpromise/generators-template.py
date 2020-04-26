"""
Turn the following unix pipeline into Python code using generators

$ for i in ../*/*py; do grep ^import $i|sed 's/import //g' ; done | sort | uniq -c | sort -nr
   4 unittest
   4 sys
   3 re
   3 csv
   2 tweepy
   2 random
   2 os
   2 json
   2 itertools
   1 time
   1 datetime
"""
import glob
import re
from collections import Counter

def gen_files(pat):
    for f in glob.glob(pat):
        yield f

def gen_lines(files):
    for f in files:
        with open(f, 'r') as file:
            for line in file.readlines():
                yield line


def gen_grep(lines, pattern):
    re_pat = re.compile(pattern)
    for l in lines:
        match = re_pat.match(l)
        if match:
            yield match[0]

def gen_count(lines):
    counter = Counter([l.replace('import ', '') for l in lines])
    for c in counter.most_common():
        yield f"{c[1]} {c[0]}"


if __name__ == "__main__":
    # call the generators, passing one to the other
    files = gen_files('../*/*.py')
    lines = gen_lines(files)
    greps = gen_grep(lines, '^import .*')
    print(list(gen_count(greps)))
