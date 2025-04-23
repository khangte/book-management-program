# db.py
"""
Database connection module.
Provides a function to get a pymssql connection to BookDB.
"""
import pymssql

def get_connection():
    """Return a new pymssql Connection to the BookDB."""
    return pymssql.connect(
        server='localhost',
        database='BookDB',
        user='SQLMaster',
        password='',
        charset='utf8'
    )
