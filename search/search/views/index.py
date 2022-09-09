"""File containing all endpoints for search server."""

import json
import flask
from flask import request
import requests
import search


@search.app.route('/')
def show_index():
    """Handle main endpoint."""
    weight = request.args.get('w', type=str)
    query = request.args.get('q', type=str)
    if weight and query:
        link = (search.app.config['INDEX_API_URL'] + "?q=" +
                query + "&w=" + weight)
        response = json.loads(requests.get(link).text)
        hits = response['hits']
        results = []
        connection = search.model.get_db()
        count = 1
        for doc in hits:
            if count > 10:
                break
            cur = connection.execute(
                "select title, summary, url "
                "from Documents "
                "where docid = ?", (doc['docid'],)
            )
            datum = cur.fetchall()
            results.append(datum[0])
            count += 1
        no_results = 1
        if len(results) > 0:
            no_results = 0
        context = {
            "results": results,
            "no_results": no_results
        }
        return flask.render_template('index.html', **context)
    return flask.render_template('index.html')
