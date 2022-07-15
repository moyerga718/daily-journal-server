import json
import sqlite3
from models import Tag

def get_all_tags():
    """
    THIS FUNCTION GETS ALL TAGS
    """
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM Tags t
        """)

        # Initialize an empty list to hold all animal representations
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            tag = Tag(row['id'], row['name'])

            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)