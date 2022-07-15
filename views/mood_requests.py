import sqlite3
import json
from models import Mood

def get_all_moods():
    """
    THIS FUNCTION GETS ALL MOODS
    """
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)

        # Initialize an empty list to hold all animal representations
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a Mood instance from the current row
            mood = Mood(row['id'], row['label'])

            # Add the dictionary representation of the location to the mood
            
            moods.append(mood.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(moods)
