import sqlite3


def InsertNewEntry(nome, tipo, aut1, aut2, genre_one, genre_two, lent, lent_w, volume):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO acervo (nome, tipo, autor_one, autor_two, genre_one, genre_two, lent, lent_who, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (nome, tipo, aut1, aut2, genre_one, genre_two, lent, lent_w, volume))
    db.commit()
    db.close()


def RetrieveAll():
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''SELECT nome, tipo, autor_one, autor_two, genre_one, genre_two, lent, lent_who, volume FROM acervo''')
    entradas = cursor.fetchall()
    db.close()
    return entradas


def UpdateEntry(nome, volume, new_lent, new_lent_w):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''UPDATE acervo SET lent = ?, lent_who = ? WHERE nome = ? AND volume = ?''', (new_lent, new_lent_w, nome, volume))
    db.commit()
    db.close()

def DeleteEntry(nome, volume):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''DELETE FROM acervo WHERE nome = ? AND volume = ?''', (nome, volume))
    db.commit()
    db.close()

def EnryExists(nome, volume):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    result = False
    cursor.execute('''SELECT nome, volume FROM acervo''')
    entradas = cursor.fetchall()
    db.close()
    for entrada in entradas:
        if (nome == entrada[0]) and (volume == entrada[1]):
            result = True
    else:
        return result

def CheckIfTableExists():
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS `acervo` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`nome`	TEXT NOT NULL,
	`tipo`	TEXT NOT NULL,
	`autor_one`	TEXT NOT NULL,
	`autor_two`	TEXT,
	`genre_one`	TEXT NOT NULL,
	`genre_two`	TEXT NOT NULL,
	`lent`	TEXT NOT NULL,
	`lent_who`	TEXT,
	`volume`	INTEGER
)''')
    db.close()

def SearchSimilarTitles(title):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''SELECT nome, tipo, autor_one, autor_two, genre_one, genre_two, lent, lent_who, volume FROM acervo WHERE nome LIKE ?''', ('%'+title+'%',))
    entradas = cursor.fetchall()
    db.close()
    return entradas

def SearchSimilarAutor(autor):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''SELECT nome, tipo, autor_one, autor_two, genre_one, genre_two, lent, lent_who, volume FROM acervo WHERE autor_one LIKE ? OR autor_two LIKE ?''', ('%'+autor+'%', '%'+autor+'%',))
    entradas = cursor.fetchall()
    db.close()
    return entradas

def SearchSimilarGenre(genre):
    db = sqlite3.connect('my_app.db')
    cursor = db.cursor()
    cursor.execute('''SELECT nome, tipo, autor_one, autor_two, genre_one, genre_two, lent, lent_who, volume FROM acervo WHERE genre_one LIKE ? OR genre_two LIKE ?''', ('%'+genre+'%', '%'+genre+'%',))
    entradas = cursor.fetchall()
    db.close()
    return entradas
