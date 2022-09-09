#!/usr/bin/env python3
"""Reduce 3."""

import sys
import math

docs = []
last_val = ''
N = int(open('total_document_count.txt', 'r').read())


def write_lines(key, docs, n_k):
    """Print line for term associated with key."""
    idf = (math.log(N / int(n_k), 10))
    # idf could have also been added in reduce3
    print_string = key + " " + str(idf)
    for doc in docs:
        print_string = print_string + " " + doc.replace('\n', '')
    print(print_string)


for line in sys.stdin:
    # Gather together information for each word
    first_split = line.split("\t")  # split between key and value
    key = first_split[0]
    if key != last_val:
        # reset
        # write key data to line
        if len(docs) != 0:
            write_lines(last_val, docs, n_k)
        docs.clear()
    last_val = key
    occurrences, n_k, doc_id, normalization_factor = first_split[1].split(', ')
    docs.append(doc_id + " " + occurrences + " " + normalization_factor)

if len(docs) != 0:
    # necessary for the last lines to get added to the output files
    write_lines(key, docs, n_k)
