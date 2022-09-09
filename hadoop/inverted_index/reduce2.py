#!/usr/bin/env python3
"""Reduce 2."""

import sys

doc_tfs = []
last_val = ''


def write_line(key, tf_list):
    """Output doc_id, tf, term, n_k for each document and word."""
    n_k = len(tf_list)
    for doc in tf_list:
        print(doc + ", " + key + ", " + str(n_k))


for line in sys.stdin:
    # calculate n_k for each term (key)
    key = line.split("\t")[0]
    if key != last_val:
        # reset
        # write key data to line
        if len(doc_tfs) != 0:
            write_line(last_val, doc_tfs)
        doc_tfs.clear()
    last_val = key
    doc_tfs.append(line.split("\t")[1].replace("\n", ''))

if len(doc_tfs) != 0:
    # needed to add the last lines
    write_line(key, doc_tfs)
