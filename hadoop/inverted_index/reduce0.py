#!/usr/bin/env python3
"""Reduce 0."""

import sys

count = 0
for line in sys.stdin:
    count += int(line.split("\t")[1])
with open("total_document_count.txt", "w+") as word_count:
    # count total number of lines in input (for number of docs)
    word_count.write(str(count))
