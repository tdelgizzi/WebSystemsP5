"""REST API for the index endpoint."""
import pathlib
import re
import math
import flask
from flask import request
import index

index_package_dir = pathlib.Path(__file__).parent.parent
stopwords_filename = index_package_dir/"stopwords.txt"
pagerank_filename = index_package_dir/"pagerank.out"
inverted_filename = index_package_dir/"inverted_index.txt"
page_rank_file = open(pagerank_filename, "r")
PAGE_RANK_TEXT = "\n".join(page_rank_file.readlines())
inverted_indices = open(inverted_filename, 'r')
INDEX_TEXT = "\n".join(inverted_indices.readlines())
stop_words = open(stopwords_filename, "r").read().splitlines()


@index.app.route('/api/v1/', methods=["GET"])
def get_directory():
    """Handle directory route."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=["GET"])
def get_hits():
    """Handle /api/v1/hits/ route."""
    weight = request.args.get('w', type=float)
    query = request.args.get('q', type=str)
    hits = get_page_hits(query, weight)
    # just to see what prints:
    context = {
        "hits": hits
    }
    return flask.jsonify(**context)


def get_query_norm_score(query):
    """Calculate the normalization factor for query."""
    running_sum = 0
    for word in query:
        idf_k = float(query[word]['idf'])
        tf_k = int(query[word]['query_count'])
        running_sum += ((tf_k ** 2) * (idf_k ** 2))
    return running_sum


def add_to_hits(hits, new_val):
    """Insert new_val into hits list according to order."""
    if not hits:
        hits.append(new_val)
        return
    loop_index = 0
    while (loop_index < len(hits) and
           hits[loop_index]['score'] > new_val['score']):
        loop_index += 1
    if loop_index == len(hits):
        hits.append(new_val)
        return
    if hits[loop_index]['score'] == new_val['score']:
        if hits[loop_index]['docid'] < new_val['docid']:
            loop_index += 1
    # insert at new spot
    hits.insert(loop_index, new_val)


def get_page_rank(doc):
    """Retrieve the page rank score for doc."""
    doc_line = re.findall("^" + str(doc) + ",.+",
                          PAGE_RANK_TEXT, re.MULTILINE)[0]
    return float(doc_line.split(',')[1])


def calculate_score(query_norm, query, doc_dict, doc, weight):
    """Calculate the score of a given doc."""
    normalization_factor = (math.sqrt(query_norm) *
                            math.sqrt(float(doc_dict[doc]['normalization'])))
    page_rank = get_page_rank(doc)
    running_sum = 0
    for word in doc_dict[doc]["query_words"]:
        idf_word = float(query[word]['idf'])
        tf_query = int(query[word]['query_count'])
        tf_doc = int(doc_dict[doc]['query_words'][word])
        running_sum += (idf_word * tf_query) * (idf_word * tf_doc)
    score = (weight * page_rank + (1 - weight) *
             (running_sum / normalization_factor))
    new_val = {
        "docid": int(doc),
        "score": score
    }
    return new_val


def is_in_inverted_index(word):
    """Check if word is in inverted index."""
    return len(re.findall("^" + str(word) + " .+",
                          INDEX_TEXT, re.MULTILINE)) > 0


def get_page_hits(q_string, weight):
    """Calculate score of a doc d for query q_string with weight weight."""
    hits = []
    query = {}
    doc_dict = {}
    # read in query
    for term in q_string.split():
        term = re.sub(r'[^a-zA-Z0-9]+', '', term).lower()
        # make sure word is not a stopword
        if term not in stop_words:
            if not is_in_inverted_index(term):
                return []
            if term not in query:
                query[term] = {
                    'query_count': 1
                }
            else:
                query[term]['query_count'] += 1
    # read in inverted index
    for word in query:
        word_line_vec = re.findall("^" + str(word) + " .+",
                                   INDEX_TEXT, re.MULTILINE)[0].split()
        query[word]['idf'] = float(word_line_vec[1])
        for i in range(2, len(word_line_vec), 3):
            doc_id, occurrences, norm = word_line_vec[i:(i + 3)]
            if doc_id not in doc_dict:
                query_words = {
                    word: occurrences
                }
                doc_dict[doc_id] = {
                    "normalization": norm,
                    "query_words": query_words
                }
            else:
                doc_dict[doc_id]["query_words"][word] = occurrences
    # get query normalization score:
    query_norm = get_query_norm_score(query)
    # iterate through documents
    for doc in doc_dict:
        if len(doc_dict[doc]['query_words']) == len(query):
            add_to_hits(hits, calculate_score(query_norm,
                                              query,
                                              doc_dict,
                                              doc,
                                              weight))
    return hits
