class Entry():
    """Class for a journal entry
    """
    def __init__(self, id, concept, entry, moodId, date):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.moodId = moodId
        self.date = date
        self.mood = None
        self.tags = None