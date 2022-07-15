CREATE TABLE `JournalEntries` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
    `moodId` INTEGER NOT NULL,
    `date` DATE NOT NULL,
    FOREIGN KEY(`moodId`) REFERENCES `Moods`(`id`)
);

CREATE TABLE `Moods` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label` TEXT NOT NULL
);

CREATE TABLE `Tags` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name` TEXT NOT NULL
);

CREATE TABLE `EntryTags` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`entryId` INTEGER NOT NULL,
    `tagId` INTEGER NOT NULL,
    FOREIGN KEY(`entryId`) REFERENCES `JournalEntries`(`id`)
    FOREIGN KEY(`tagId`) REFERENCES `Tags`(`id`)
);

INSERT INTO `Tags` VALUES (null, "jimmy");
INSERT INTO `Tags` VALUES (null, "corn");
INSERT INTO `Tags` VALUES (null, "Korn");
INSERT INTO `Tags` VALUES (null, "grooming tips");

INSERT INTO `EntryTags` VALUES (null, 3, 1);
INSERT INTO `EntryTags` VALUES (null, 3, 3);
INSERT INTO `EntryTags` VALUES (null, 4, 2);
INSERT INTO `EntryTags` VALUES (null, 6, 1);
INSERT INTO `EntryTags` VALUES (null, 6, 3);
INSERT INTO `EntryTags` VALUES (null, 6, 4);
INSERT INTO `EntryTags` VALUES (null, 7, 4);
INSERT INTO `EntryTags` VALUES (null, 8, 1);
INSERT INTO `EntryTags` VALUES (null, 9, 4);


INSERT INTO `JournalEntries` VALUES (null, "Javascript", "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.", 1, "Wed Sep 15 2021 10:10:47");
INSERT INTO `JournalEntries` VALUES (null, "Python", "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 3, "Wed Sep 15 2021 10:11:33 ");
INSERT INTO `JournalEntries` VALUES (null, "Python", "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", 2, "Wed Sep 15 2021 10:13:11 ");
INSERT INTO `JournalEntries` VALUES (null, "Javascript", "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 4, "Wed Sep 15 2021 10:10:47");


INSERT INTO `Moods` VALUES (null, "vibing");
INSERT INTO `Moods` VALUES (null, "purely vibing");
INSERT INTO `Moods` VALUES (null, "Neggy Vibes :(");
INSERT INTO `Moods` VALUES (null, "str8 vibes aha");



SELECT * FROM JournalEntries;

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
        WHERE j.entry LIKE '%is%'

SELECT
        j.id,
        j.concept,
        j.entry,
        j.moodId,
        j.date,
        m.id,
        m.label,
        t.tagId
    FROM JournalEntries j
    JOIN Moods m
        ON j.moodId = m.id
    JOIN EntryTags t
        ON t.entryId = j.id

DELETE FROM EntryTags
        WHERE entryid = 10