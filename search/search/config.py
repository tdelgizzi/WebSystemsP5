"""Search server development confirguration."""

import pathlib

APPLICATION_ROOT = '/search/'

INDEX_API_URL = "http://localhost:8001/api/v1/hits/"

ASK485_ROOT = pathlib.Path(__file__).resolve().parent.parent

DATABASE_FILENAME = ASK485_ROOT/'search'/'var'/'index.sqlite3'
