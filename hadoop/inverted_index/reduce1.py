#!/usr/bin/env python3
"""Reduce 1."""

import sys

word_doc_frequency = {}
for line in sys.stdin:
    # count number of occurrences of word in each doc that has it
    key = line.split("\t")[0]
    if key in word_doc_frequency:
        word_doc_frequency[key] += 1
    else:
        # start at 1, not 0
        word_doc_frequency[key] = 1

for dict_key in word_doc_frequency:
    # print values in dictionary
    print(dict_key + ", " + str(word_doc_frequency[dict_key]))
