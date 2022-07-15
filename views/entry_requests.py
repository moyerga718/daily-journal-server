import sqlite3
import json
from models import Entry
from models import Mood
from models import EntryTag
from models import Tag


def get_all_entries():
    """
    THIS FUNCTION GETS ALL Entries
    """
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            j.id,
            j.concept,
            j.entry,
            j.moodId,
            j.date,
            m.id,
            m.label
        FROM JournalEntries j
        JOIN Moods m
            ON j.moodId = m.id
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['moodId'],
                            row['date'])

            # Create a Location instance from the current row
            mood = Mood(row['moodId'], row['label'])

            # Add the dictionary representation of the location to the animal
            entry.mood = mood.__dict__

            # Set empty list that tag ids will get stored into
            tags = []

            #Make sql call to get the tag ids / names for this entry.
            db_cursor.execute("""
            SELECT
                e.tagId,
                t.name
            FROM EntryTags e
            JOIN Tags t
                ON e.tagId = t.id
            WHERE e.entryId = ?
            """, (row['id'], ))

            #Store response from SQL call to tagData
            tagData = db_cursor.fetchall()

            #Loop through rows from SQL call 
            for row in tagData:

                #Create a tag instance from data in each row
                tag = Tag(row['tagId'], row['name'])

                #turn this instance into a dictionary, add this dictionary to tags list
                tags.append(tag.__dict__)

            #Add tags list to entry
            entry.tags = tags

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


def get_single_entry(id):
    """
    THIS FUNCTION GETS ALL Entries
    """
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            j.id,
            j.concept,
            j.entry,
            j.moodId,
            j.date,
            m.id,
            m.label
        FROM JournalEntries j
        JOIN Moods m
            ON j.moodId = m.id
        WHERE j.id = ?
        """, (id, ))

        # Convert row into a Python list data
        data = db_cursor.fetchone()

        # Create an entry instance from the data
        entry = Entry(data['id'], data['concept'], data['entry'], data['moodId'],
                    data['date'])

        # Create a Location instance from the current row
        mood = Mood(data['id'], data['label'])

        # Add the dictionary representation of the location to the animal

        entry.mood = mood.__dict__

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry.__dict__)


def delete_entry(id):
    """DELETE ENTRY
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM JournalEntries
        WHERE id = ?
        """, (id, ))

        db_cursor.execute("""
        DELETE FROM EntryTags
        WHERE entryid = ?
        """, (id, ))


def get_searched_entries(searchTerm):
    """
    THIS RETURNS ALL ENTRIES THAT MATCH SEARCH
    """
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want

        searchTermString = f'%{searchTerm}%'

        db_cursor.execute("""
        SELECT
            j.id,
            j.concept,
            j.entry,
            j.moodId,
            j.date,
            m.id,
            m.label
        FROM JournalEntries j
        JOIN Moods m
            ON j.moodId = m.id
        WHERE j.entry LIKE ?
        """, (searchTermString, ))

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['moodId'],
                          row['date'])

            # Create a Location instance from the current row
            mood = Mood(row['id'], row['label'])

            # Add the dictionary representation of the location to the animal
            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)


def create_entry(new_entry):
    """GO ON NOW, MAKE AN ENTRY W/ SQL
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO JournalEntries
            ( concept, entry, moodId, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['moodId'], new_entry['date'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        entryId = db_cursor.lastrowid

        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = entryId

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTags
                ( entryId, tagId )
            VALUES
                ( ?, ?);
            """, (entryId, tag,))

    return json.dumps(new_entry)


def update_entry(id, new_entry):
    """update an entrys info, see if any entrys match the id that is provided to
    the method.
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE JournalEntries
            SET
                concept = ?,
                entry = ?,
                moodId = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['moodId'], new_entry['date'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
