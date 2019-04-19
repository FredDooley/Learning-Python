"""
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Using Databases with Python Week 3
Worked Example: Tracks.py

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Goal (7 Steps)
I. Read XML file
II. Find all tracks
III. Store track info (Artist, Album, Title) in SQL tables

––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"""

#1 Import libraries
import xml.etree.ElementTree as ET
import sqlite3

#2 Create database connection
conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

#3 Create tables
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

#4 Read in XML file
fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'

#5 Parse XML file
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))

#6 Read XML tree


def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None :
        continue

    print(name, artist, album, count, rating, length)

    #7 Insert XML data into SQL
    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count)
        VALUES ( ?, ?, ?, ?, ? )''',
        ( name, album_id, length, rating, count ) )

    conn.commit()
'''
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
Steps (memorize me)
1. Import libraries
2. Create database connection
3. Create tables
4. Read in XML file
5. Parse XML file
6. Read XML tree
7. Insert XML data into SQL
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''
