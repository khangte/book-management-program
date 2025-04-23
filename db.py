# db.py
"""
Database connection module.
Provides a function to get a pymssql connection to BookDB.
"""
import pymssql

def get_connection():
    """Return a new pymssql Connection to the BookDB."""
    return pymssql.connect(
        server='127.0.0.1',
        database='BookDB',
        user='kmh-tester1',
        password='1234',
        charset='utf8'
    )
