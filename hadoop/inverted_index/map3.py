#!/usr/bin/env python3
"""Map 3."""

import sys

for line in sys.stdin:
    new_line = line.replace(", ", "\t", 1).replace('\n', '')
    print(new_line)
