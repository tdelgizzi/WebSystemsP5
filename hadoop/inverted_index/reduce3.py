#!/usr/bin/env python3
"""Reduce 3."""

import sys
import math

N = int(open('total_document_count.txt', 'r').read())
words_list = []
norm_val = 0
last_val = ""


def write_line(key, words, norm_val):
    """Output word, tf, n_k, doc_id, norm_val."""
    for word in words:
        word_split = word.split(", ")
        print(word_split[1] + ", " + word_split[0] + ", " + word_split[2] +
              ", " + key + ", " +
              str(norm_val))


for line in sys.stdin:
    # keep track of squared normalization value
    first_split = line.split("\t")
    key = first_split[0]
    tf, term, n_k = first_split[1].split(', ')
    tf = int(tf)
    n_k = int(n_k)
    if key != last_val:
        # reset
        # write key data to line
        if len(words_list) != 0:
            write_line(last_val, words_list, norm_val)
        words_list.clear()
        norm_val = 0
    idf = (math.log(N / n_k, 10))
    norm_val += (tf ** 2) * (idf ** 2)
    last_val = key
    words_list.append(line.split("\t")[1].replace("\n", ''))

if len(words_list) != 0:
    write_line(key, words_list, norm_val)
