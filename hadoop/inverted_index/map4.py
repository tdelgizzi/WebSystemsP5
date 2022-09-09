#!/usr/bin/env python3
"""Map 4."""

import sys

for line in sys.stdin:
    new_li = line.replace(", ", "\t", 1).replace('\n', '')
    print(new_li)
