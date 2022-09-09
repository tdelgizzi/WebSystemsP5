#!/usr/bin/env python3
"""Map 0."""

import sys

local_count = 0
for line in sys.stdin:
    local_count += 1
print("docs\t" + str(local_count))
