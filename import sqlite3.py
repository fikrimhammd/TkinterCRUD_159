import sqlite3
con = sqlite3.connect("tutorial.db")

cur = con.cursor()
#cur.execute("CREATE TABLE movie(title text, year int, score double)")

#cur.execute("""
#   INSERT INTO movie VALUES
#        ('Monty Python and the Holy Grail', 1975, 8.2),
#       ('And Now for Something Completely Different', 1971, 7.5)
#""")
#con.commit()

_title=input("Masukan Judul Movie: ")
_year=input("Masukan tahun Release: ")
_rating=input("Masukan nilai rating movie: ")
cur.execute("""
            INSERT INTO movie VALUES
        ('{}', {}, {})
    """, format(_title, _year, _rating))
con.commit()