#!/usr/bin/env python3
"""Map 1."""

import sys
import csv
import re

csv.field_size_limit(sys.maxsize)
data = sys.stdin.readlines()
stop_words = open("stopwords.txt", "r").read().splitlines()

for line in csv.reader(data):
    doc_id = line[0]
    terms = line[1] + " " + line[2]
    for word in terms.split():
        word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower()
        # make sure word is not a stopword
        if word not in stop_words and word:
            print(word + ", " + str(doc_id) + "\t1")
