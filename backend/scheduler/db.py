import sqlite3


DB_PATH = "scheduler.db"


def get_connection():

    return sqlite3.connect(
        DB_PATH
    )