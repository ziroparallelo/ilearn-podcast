import sqlite3
from models import User

# GESTIONE TABELLA USER
def get_user_with_password_by_email(email):
    conn = sqlite3.connect('db/podcast.db') 
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE email = ?'
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_with_password_by_id(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE ID = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_by_id(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ID, Email, Username, Tipo FROM UTENTI WHERE ID = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def add_user(user):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO UTENTI(Email,Password,Tipo,Username) VALUES(?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['email'], user['password'], user['type'], user['username']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# GESTIONE TABELLA SERIE

# RESTITUISCE LA CHIAVE PRIMARIA 
def add_podcast(podcast):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'INSERT INTO PODCAST(Titolo, Descrizione, utente_id, Categoria, Estensione) VALUES(?,?,?,?,?)'
    
    try:
        cursor.execute(
            sql, (podcast['Titolo'], podcast['Descrizione'], podcast['utente_id'], podcast['Categoria'], podcast['Estensione']))
        conn.commit()
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT podcast_id FROM PODCAST WHERE Titolo = ? AND utente_id = ?'
    cursor.execute(sql, (podcast['Titolo'], podcast['utente_id']))
    podcast_id = cursor.fetchone()

    cursor.close()
    conn.close()

    return podcast_id

def cancella_podcast_by_id(podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")

    cursor = conn.cursor()

    sql = 'DELETE FROM PODCAST WHERE podcast_id=?'

    try:
        cursor.execute(
            sql, (podcast_id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_podcast(podcast):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE PODCAST SET Titolo = ?, Descrizione = ?, utente_id = ?, Categoria = ? WHERE podcast_id = ?'
    
    try:
        cursor.execute(
            sql, (podcast['Titolo'], podcast['Descrizione'], podcast['utente_id'], podcast['Categoria'], podcast['podcast_id']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_podcasts():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM PODCAST, UTENTI WHERE PODCAST.utente_id = UTENTI.ID'
    cursor.execute(sql)
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts

def get_podcasts_by_categoria(categoria):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM PODCAST, UTENTI WHERE PODCAST.utente_id = UTENTI.ID AND PODCAST.Categoria = ?'
    cursor.execute(sql, (categoria,))
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts

def get_podcast_by_id(podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM PODCAST, UTENTI WHERE PODCAST.utente_id = UTENTI.ID AND podcast_id = ?'
    cursor.execute(sql, (podcast_id,))
    podcast = cursor.fetchone()

    cursor.close()
    conn.close()

    return podcast

def get_id_podcast_seguiti(user_id):
    seguiti = []
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = 'SELECT FOLLOW.podcast_id FROM FOLLOW, PODCAST WHERE FOLLOW.podcast_id = PODCAST.podcast_id AND FOLLOW.utente_id = ?'
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall() #elenco IDSerie in un oggetto row

    for row in result:
        elem = row[0]
        seguiti.append(elem)

    cursor.close()
    conn.close()

    return seguiti

def get_podcast_seguiti(userid):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM PODCAST, FOLLOW, UTENTI WHERE PODCAST.podcast_id = FOLLOW.podcast_id AND PODCAST.utente_id = UTENTI.ID AND FOLLOW.utente_id = ?'
    cursor.execute(sql, (userid,))
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts


# GESTIONE TABELLA EPISODI
def add_episodio(episodio):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO EPISODI(Titolo, Descrizione, DataCreazione, podcast_id, Estensione) VALUES(?,?,?,?,?)'
    
    try:
        cursor.execute(
            sql, (episodio['Titolo'], episodio['Descrizione'], episodio['DataCreazione'], episodio['podcast_id'], episodio['Estensione']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    if success:
        conn = sqlite3.connect('db/podcast.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        success = False
        sql = 'SELECT episodio_id FROM EPISODI WHERE Titolo = ? AND podcast_id = ? AND Descrizione = ?'
        cursor.execute(sql, (episodio['Titolo'], episodio['podcast_id'], episodio['Descrizione']))
        episodio_id = cursor.fetchone()
    else: 
        episodio_id = None

    return episodio_id

def get_episodi_by_podcast_id(podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # TODO ordinare episodi per data
    sql = 'SELECT * FROM EPISODI WHERE podcast_id = ? ORDER BY DataCreazione DESC'
    cursor.execute(sql, (podcast_id,))
    episodi = cursor.fetchall()

    cursor.close()
    conn.close()

    return episodi

def cancellaEpisodio_byTitolo(titolo):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    sql = 'DELETE FROM EPISODI WHERE Titolo=?'

    try:
        cursor.execute(
            sql, (titolo,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def getEpisodio_fromTitolo(titolo):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM EPISODI WHERE Titolo=?'
    cursor.execute(sql, (titolo,))
    episodio = cursor.fetchone()

    cursor.close()
    conn.close()

    return episodio

def update_episodio(episodio, id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE EPISODI SET Titolo = ?, Descrizione = ?, DataCreazione = ?, podcast_id = ?, Estensione = ? WHERE episodio_id = ?'
    
    try:
        cursor.execute(
            sql, (episodio['Titolo'], episodio['Descrizione'], episodio['DataCreazione'], episodio['podcast_id'], episodio['Estensione'], id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def getEpisodio_byID(id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM EPISODI WHERE episodio_id=?'
    cursor.execute(sql, (id,))
    episodio = cursor.fetchone()

    cursor.close()
    conn.close()

    return episodio

def getEpisodio_byCommentoID(commento_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM EPISODI, COMMENTI WHERE COMMENTI.episodio_id = EPISODI.episodio_id AND commento_id=?'
    cursor.execute(sql, (commento_id,))
    episodio = cursor.fetchone()

    cursor.close()
    conn.close()

    return episodio


# GESTIONE TABELLA COMMENTI
def update_commento(commento):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE COMMENTI SET Testo = ? WHERE commento_id = ?'
    
    try:
        cursor.execute(
            sql, (commento['Testo'], commento['commento_id']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def add_commento(commento):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO COMMENTI(utente_id, episodio_id, Testo) VALUES(?,?,?)'
    
    try:
        cursor.execute(
            sql, (commento['utente_id'], commento['episodio_id'], commento['Testo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_commenti_e_autori_by_episodio_id(episodio_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT commento_id, episodio_id, utente_id, Testo, Username FROM COMMENTI, UTENTI WHERE COMMENTI.utente_id == UTENTI.ID AND COMMENTI.episodio_id=?'
    cursor.execute(sql, (episodio_id,))
    commenti = cursor.fetchall()

    cursor.close()
    conn.close()

    return commenti

def get_commento_by_id(commento_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM COMMENTI WHERE commento_id=?'
    cursor.execute(sql, (commento_id,))
    commento = cursor.fetchone()

    cursor.close()
    conn.close()

    return commento

def cancellaCommento_by_id(commento_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    sql = 'DELETE FROM COMMENTI WHERE commento_id=?'

    try:
        cursor.execute(
            sql, (commento_id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


# GESTIONE TABELLA FOLLOW
def follow_podcast(userid, podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'INSERT INTO FOLLOW(podcast_id, utente_id) VALUES(?,?)'

    try:
        cursor.execute(
            sql, (podcast_id, userid))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def unfollow_podcast(userid, podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'DELETE FROM FOLLOW WHERE utente_id = ? AND podcast_id = ?'

    try:
        cursor.execute(
            sql, (userid, podcast_id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success
