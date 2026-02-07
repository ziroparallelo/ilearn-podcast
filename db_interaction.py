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

    success = False
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

    success = False
    sql = 'DELETE FROM EPISODI WHERE Titolo=?'

    try:
        cursor.execute(
            sql, (titolo,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
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

    success = False
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

    success = False
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

    success = False
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


# ============================================
# FASE 1: DURATA EPISODI
# ============================================

def update_durata_episodio(episodio_id, durata):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute('UPDATE EPISODI SET Durata = ? WHERE episodio_id = ?', (durata, episodio_id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success


# ============================================
# FASE 2: EPISODI SALVATI / PREFERITI
# ============================================

def salva_episodio(utente_id, episodio_id, data_salvataggio):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(
            'INSERT OR IGNORE INTO SALVATI(utente_id, episodio_id, DataSalvataggio) VALUES(?,?,?)',
            (utente_id, episodio_id, data_salvataggio))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def rimuovi_salvato(utente_id, episodio_id):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute(
            'DELETE FROM SALVATI WHERE utente_id = ? AND episodio_id = ?',
            (utente_id, episodio_id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_episodi_salvati(utente_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT E.*, P.Titolo AS PodcastTitolo, P.podcast_id, P.Estensione AS PodcastEstensione, S.DataSalvataggio
        FROM SALVATI S
        JOIN EPISODI E ON S.episodio_id = E.episodio_id
        JOIN PODCAST P ON E.podcast_id = P.podcast_id
        WHERE S.utente_id = ?
        ORDER BY S.DataSalvataggio DESC
    ''', (utente_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_id_episodi_salvati(utente_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT episodio_id FROM SALVATI WHERE utente_id = ?', (utente_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row['episodio_id'] for row in result]


# ============================================
# FASE 3: TAG PER EPISODI
# ============================================

def get_or_create_tag(nome):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT tag_id FROM TAGS WHERE Nome = ?', (nome,))
    tag = cursor.fetchone()
    if tag:
        tag_id = tag['tag_id']
    else:
        cursor.execute('INSERT INTO TAGS(Nome) VALUES(?)', (nome,))
        conn.commit()
        tag_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return tag_id

def add_tags_to_episodio(episodio_id, tag_names):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    for nome in tag_names:
        nome = nome.strip().lower()
        if not nome:
            continue
        cursor.execute('SELECT tag_id FROM TAGS WHERE Nome = ?', (nome,))
        tag = cursor.fetchone()
        if tag:
            tag_id = tag[0]
        else:
            cursor.execute('INSERT INTO TAGS(Nome) VALUES(?)', (nome,))
            tag_id = cursor.lastrowid
        try:
            cursor.execute('INSERT OR IGNORE INTO EPISODIO_TAGS(episodio_id, tag_id) VALUES(?,?)', (episodio_id, tag_id))
        except Exception as e:
            print('ERROR', str(e))
    conn.commit()
    cursor.close()
    conn.close()

def get_tags_by_episodio(episodio_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT T.tag_id, T.Nome FROM TAGS T
        JOIN EPISODIO_TAGS ET ON T.tag_id = ET.tag_id
        WHERE ET.episodio_id = ?
        ORDER BY T.Nome
    ''', (episodio_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_episodi_by_tag(nome_tag):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT E.*, P.Titolo AS PodcastTitolo, P.podcast_id, P.Estensione AS PodcastEstensione, U.Username
        FROM EPISODI E
        JOIN EPISODIO_TAGS ET ON E.episodio_id = ET.episodio_id
        JOIN TAGS T ON ET.tag_id = T.tag_id
        JOIN PODCAST P ON E.podcast_id = P.podcast_id
        JOIN UTENTI U ON P.utente_id = U.ID
        WHERE T.Nome = ?
        ORDER BY E.DataCreazione DESC
    ''', (nome_tag,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def remove_tags_from_episodio(episodio_id):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM EPISODIO_TAGS WHERE episodio_id = ?', (episodio_id,))
        conn.commit()
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()

def get_all_tags():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TAGS ORDER BY Nome')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# ============================================
# FASE 4: RATING STELLE (1-5)
# ============================================

def add_or_update_valutazione(utente_id, podcast_id, voto, data_voto):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute('''
            INSERT INTO VALUTAZIONI(utente_id, podcast_id, Voto, DataVoto)
            VALUES(?,?,?,?)
            ON CONFLICT(utente_id, podcast_id) DO UPDATE SET Voto = ?, DataVoto = ?
        ''', (utente_id, podcast_id, voto, data_voto, voto, data_voto))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_valutazione_utente(utente_id, podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT Voto FROM VALUTAZIONI WHERE utente_id = ? AND podcast_id = ?', (utente_id, podcast_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['Voto'] if result else 0

def get_media_valutazioni(podcast_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT AVG(Voto) as media, COUNT(*) as totale FROM VALUTAZIONI WHERE podcast_id = ?', (podcast_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and result['totale'] > 0:
        return {'media': round(result['media'], 1), 'totale': result['totale']}
    return {'media': 0, 'totale': 0}

def get_podcasts_con_valutazioni():
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT P.podcast_id, AVG(V.Voto) as media, COUNT(V.Voto) as totale
        FROM PODCAST P
        LEFT JOIN VALUTAZIONI V ON P.podcast_id = V.podcast_id
        GROUP BY P.podcast_id
    ''')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    ratings = {}
    for row in result:
        ratings[row['podcast_id']] = {
            'media': round(row['media'], 1) if row['media'] else 0,
            'totale': row['totale']
        }
    return ratings


# ============================================
# FASE 5: FEED NUOVI EPISODI
# ============================================

def get_nuovi_episodi_feed(utente_id, limit=20):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT E.*, P.Titolo AS PodcastTitolo, P.Estensione AS PodcastEstensione,
               P.podcast_id, U.Username
        FROM EPISODI E
        JOIN PODCAST P ON E.podcast_id = P.podcast_id
        JOIN UTENTI U ON P.utente_id = U.ID
        JOIN FOLLOW F ON F.podcast_id = P.podcast_id
        WHERE F.utente_id = ?
        ORDER BY E.DataCreazione DESC
        LIMIT ?
    ''', (utente_id, limit))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# ============================================
# FASE 6: TRENDING + TOP RATED
# ============================================

def get_podcast_trending(limit=6):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT P.*, U.Username, COUNT(F.utente_id) as follower_count
        FROM PODCAST P
        JOIN UTENTI U ON P.utente_id = U.ID
        LEFT JOIN FOLLOW F ON P.podcast_id = F.podcast_id
        GROUP BY P.podcast_id
        ORDER BY follower_count DESC
        LIMIT ?
    ''', (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_podcast_top_rated(limit=6):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT P.*, U.Username, AVG(V.Voto) as media_voto, COUNT(V.Voto) as num_voti
        FROM PODCAST P
        JOIN UTENTI U ON P.utente_id = U.ID
        JOIN VALUTAZIONI V ON P.podcast_id = V.podcast_id
        GROUP BY P.podcast_id
        HAVING num_voti > 0
        ORDER BY media_voto DESC, num_voti DESC
        LIMIT ?
    ''', (limit,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# ============================================
# FASE 7: RICERCA GLOBALE AVANZATA
# ============================================

def search_global(query, filtro='tutto', categoria=None):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    results = []
    q = '%' + query + '%'

    if filtro in ('tutto', 'podcast'):
        sql = '''
            SELECT P.podcast_id as id, P.Titolo, P.Descrizione, P.Categoria, P.Estensione,
                   U.Username, 'podcast' as tipo
            FROM PODCAST P
            JOIN UTENTI U ON P.utente_id = U.ID
            WHERE P.Titolo LIKE ? OR P.Descrizione LIKE ?
        '''
        params = [q, q]
        if categoria:
            sql += ' AND P.Categoria = ?'
            params.append(categoria)
        cursor.execute(sql, params)
        results.extend(cursor.fetchall())

    if filtro in ('tutto', 'episodi'):
        sql = '''
            SELECT E.episodio_id as id, E.Titolo, E.Descrizione, P.Categoria, P.Estensione,
                   U.Username, 'episodio' as tipo, E.podcast_id
            FROM EPISODI E
            JOIN PODCAST P ON E.podcast_id = P.podcast_id
            JOIN UTENTI U ON P.utente_id = U.ID
            WHERE E.Titolo LIKE ? OR E.Descrizione LIKE ?
        '''
        params = [q, q]
        if categoria:
            sql += ' AND P.Categoria = ?'
            params.append(categoria)
        cursor.execute(sql, params)
        results.extend(cursor.fetchall())

    if filtro in ('tutto', 'tag'):
        sql = '''
            SELECT T.tag_id as id, T.Nome as Titolo, '' as Descrizione, '' as Categoria,
                   '' as Estensione, '' as Username, 'tag' as tipo
            FROM TAGS T
            WHERE T.Nome LIKE ?
        '''
        cursor.execute(sql, (q,))
        results.extend(cursor.fetchall())

    cursor.close()
    conn.close()
    return results


# ============================================
# FASE 8: PROGRESSO ASCOLTO
# ============================================

def update_progresso(utente_id, episodio_id, posizione, durata, completato, timestamp):
    conn = sqlite3.connect('db/podcast.db')
    cursor = conn.cursor()
    success = False
    try:
        cursor.execute('''
            INSERT INTO PROGRESSO(utente_id, episodio_id, Posizione, Durata, Completato, UltimoAggiornamento)
            VALUES(?,?,?,?,?,?)
            ON CONFLICT(utente_id, episodio_id)
            DO UPDATE SET Posizione = ?, Durata = ?, Completato = ?, UltimoAggiornamento = ?
        ''', (utente_id, episodio_id, posizione, durata, completato, timestamp,
              posizione, durata, completato, timestamp))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_progresso(utente_id, episodio_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PROGRESSO WHERE utente_id = ? AND episodio_id = ?', (utente_id, episodio_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_progressi_utente(utente_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PROGRESSO WHERE utente_id = ?', (utente_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    progressi = {}
    for row in result:
        progressi[row['episodio_id']] = {
            'posizione': row['Posizione'],
            'durata': row['Durata'],
            'completato': row['Completato']
        }
    return progressi


# ============================================
# FASE 9: STATISTICHE PROFILO
# ============================================

def get_user_stats(utente_id):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as n FROM FOLLOW WHERE utente_id = ?', (utente_id,))
    seguiti = cursor.fetchone()['n']

    cursor.execute('SELECT COUNT(*) as n FROM SALVATI WHERE utente_id = ?', (utente_id,))
    salvati = cursor.fetchone()['n']

    cursor.execute('SELECT COUNT(*) as n FROM COMMENTI WHERE utente_id = ?', (utente_id,))
    commenti = cursor.fetchone()['n']

    cursor.execute('SELECT COUNT(*) as n FROM VALUTAZIONI WHERE utente_id = ?', (utente_id,))
    valutazioni = cursor.fetchone()['n']

    cursor.close()
    conn.close()

    return {
        'seguiti': seguiti,
        'salvati': salvati,
        'commenti': commenti,
        'valutazioni': valutazioni
    }


# ============================================
# FASE 10: PAGINAZIONE
# ============================================

def get_podcasts_paginated(page=1, per_page=9):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM PODCAST')
    total = cursor.fetchone()['total']

    offset = (page - 1) * per_page
    cursor.execute('''
        SELECT * FROM PODCAST, UTENTI
        WHERE PODCAST.utente_id = UTENTI.ID
        ORDER BY PODCAST.podcast_id DESC
        LIMIT ? OFFSET ?
    ''', (per_page, offset))
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    import math
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    return podcasts, total, total_pages

def get_podcasts_by_categoria_paginated(categoria, page=1, per_page=9):
    conn = sqlite3.connect('db/podcast.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total FROM PODCAST WHERE Categoria = ?', (categoria,))
    total = cursor.fetchone()['total']

    offset = (page - 1) * per_page
    cursor.execute('''
        SELECT * FROM PODCAST, UTENTI
        WHERE PODCAST.utente_id = UTENTI.ID AND PODCAST.Categoria = ?
        ORDER BY PODCAST.podcast_id DESC
        LIMIT ? OFFSET ?
    ''', (categoria, per_page, offset))
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    import math
    total_pages = math.ceil(total / per_page) if total > 0 else 1
    return podcasts, total, total_pages
