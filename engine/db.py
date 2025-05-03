import csv
import sqlite3
import shutil

con = sqlite3.connect("application.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

#tmp=shutil.which('mysqlsh')
""" query = "INSERT INTO sys_command VALUES (null,'vlc','C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe')"
cursor.execute(query)
con.commit() """

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO web_command VALUES (null,'spotify','https://open.spotify.com/')"
cursor.execute(query)
con.commit() 