# -*- coding: utf-8 -*-

import sqlite3

con = sqlite3.connect("GooglePlayMetainfo.db")
con.text_factory = str
cur = con.cursor()
cur.execute('''
    create table if not exists metainfo (
        id integer primary key autoincrement,
        packageName text not null,
        title text not null,
        datePublished text not null,
        fileSize integer not null,
        numDownloads integer not null,
        numComments integer not null,
        softwareVersion text not null,
        operatingSystems text not null,
        contentRating text not null,
        price real not null,
        description text not null,
        developer text not null,
        devMail text not null,
        devLink text not null,
        category text not null,
        categoryUrl text not null,
        currentRating real not null,
        distRating text not null,
        avgRating real not null
    );
''')
con.commit()
cur.close()
con.close()
