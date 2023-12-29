from dotenv import load_dotenv
import os

import typing as tp
import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor

load_dotenv()
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST_IP = os.environ["DB_HOST_IP"]


def fetch_all(query: str, args: tp.Dict):
    with psycopg2.connect(
        dbname="book_club",
        user="machine_solution", 
        password="P@2sw0rd_forPG",
        host="51.250.121.111",
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query=query, vars=args)
            return [dict(row) for row in cursor.fetchall()]


def fetch_one(query: str, args: tp.Dict):
    with psycopg2.connect(
        dbname="book_club",
        user="machine_solution", 
        password="P@2sw0rd_forPG",
        host="51.250.121.111",
    ) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query=query, vars=args)
            try:
                row = cursor.fetchone()
                return dict(row)
            except:
                return None
