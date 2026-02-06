# MODULI
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_session import Session
import db_interaction
from datetime import date
import os
import re
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Accedi per visualizzare questa pagina'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

# HOME E PAGINA PER UN PODCAST SINGOLA
@app.route('/')
def home():
    podcasts = db_interaction.get_podcasts()
    categorie = ['Tutte', 'Cucina', 'Scienza', 'Sport', 'Tecnologia', 'Altro']
    if current_user.is_authenticated:
        isactive = True
        userid = current_user.get_id()
        user = db_interaction.get_user_by_id(userid)
        return render_template('home.html', podcasts=podcasts, user=user, isactive=isactive, categorie=categorie)
    else:
        isactive = False
        return render_template('home.html', podcasts=podcasts, categorie=categorie, isactive=isactive)

@app.route('/categoria/<nome_categoria>')
def categoria(nome_categoria):
    categorie_valide = {'cucina': 'Cucina', 'scienza': 'Scienza', 'sport': 'Sport', 'tecnologia': 'Tecnologia', 'altro': 'Altro'}
    if nome_categoria.lower() not in categorie_valide:
        return render_template('errori.html', titolo='404', testo='Categoria non trovata.'), 404

    nome_display = categorie_valide[nome_categoria.lower()]
    podcasts = db_interaction.get_podcasts_by_categoria(nome_categoria.lower())

    if current_user.is_authenticated:
        isactive = True
        userid = current_user.get_id()
        user = db_interaction.get_user_by_id(userid)
        return render_template('categoria.html', podcasts=podcasts, user=user, isactive=isactive, categoria=nome_display, categoria_slug=nome_categoria.lower())
    else:
        isactive = False
        return render_template('categoria.html', podcasts=podcasts, isactive=isactive, categoria=nome_display, categoria_slug=nome_categoria.lower())

@app.route('/profilo/<int:user_id>')
@login_required
def profilo(user_id):
    podcast_seguiti = db_interaction.get_podcast_seguiti(user_id)
    id_podcast_seguiti = db_interaction.get_id_podcast_seguiti(user_id)
    user = db_interaction.get_user_by_id(user_id)
    isactive = True
    return render_template('profilo.html', podcast_seguiti=podcast_seguiti, user=user, isactive=isactive, id_podcast_seguiti=id_podcast_seguiti)

@app.route('/podcast/<int:podcast_id>')
def podcast(podcast_id):
    podcast = db_interaction.get_podcast_by_id(podcast_id)
    episodi = db_interaction.get_episodi_by_podcast_id(podcast_id)

    if current_user.is_authenticated:
        userid = current_user.get_id()
        user = db_interaction.get_user_by_id(userid)
        podcast_seguiti = db_interaction.get_podcast_seguiti(userid)
        id_podcast_seguiti = db_interaction.get_id_podcast_seguiti(userid)
        isactive = True
        return render_template('podcast.html', podcast=podcast, episodi=episodi, user=user, isactive=isactive, podcast_seguiti=podcast_seguiti, id_podcast_seguiti=id_podcast_seguiti)
    else:
        isactive = False
        return render_template('podcast.html', podcast=podcast, isactive=isactive, episodi=episodi)

@app.route('/singoloEpisodio/<int:episodio_id>')
def singoloEpisodio(episodio_id):
    episodio = db_interaction.getEpisodio_byID(episodio_id)
    podcast_id = episodio['podcast_id']
    podcast = db_interaction.get_podcast_by_id(podcast_id)
    commenti = db_interaction.get_commenti_e_autori_by_episodio_id(episodio_id)

    if current_user.is_authenticated:
        userid = current_user.get_id()
        user = db_interaction.get_user_by_id(userid)
        isactive = True
        return render_template('singoloEpisodio.html', isactive=isactive, episodio=episodio, user=user, commenti=commenti, podcast=podcast)
    else:
        isactive = False
        return render_template('singoloEpisodio.html', episodio=episodio, commenti=commenti, isactive=isactive)

def valida(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)

# LOGIN, SIGNUP E LOGOUT
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if valida(email):
        email_valida = True
    else:
        email_valida = False

    if (len(password) >= 8 and email_valida):
        user = db_interaction.get_user_with_password_by_email(email)

        if not user or not check_password_hash(user['password'], password):
            flash('Credenziali non valide, riprovare', 'danger')
            return redirect(url_for('login'))
        else:
            new = User(id=user['ID'], email=user['Email'], password=user['Password'], type=user['Tipo'], username=user['Username'])
            login_user(new, True)
            return redirect(url_for('home')) 
    else:
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    db_user = db_interaction.get_user_with_password_by_id(user_id)
    user = User(id=db_user['ID'], email=db_user['Email'], password=db_user['Password'], type=db_user['Tipo'], username=db_user['Username'])

    return user

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('usertype')
    username = request.form.get('username')

    if valida(email):
        email_valida = True
    else:
        email_valida = False

    if (len(password) >= 8 and (type == "1" or type == "0") and len(username)>= 3 and email_valida):
        user_in_db = db_interaction.get_user_with_password_by_email(email)
        if user_in_db:
            flash('C\'è già un utente registrato con questa email', 'danger')
            return redirect(url_for('login')) 
        else:
            new_user = {
                "email": email,
                "password": generate_password_hash(password, method='sha256'),
                "type": type,
                "username": username
            }

            success = db_interaction.add_user(new_user)

            if success:
                flash('Utente creato correttamente', 'success')
                return redirect(url_for('login'))
            else:
                flash('Errore nella creazione del utente: riprova!', 'danger')
                return redirect(url_for('signup'))
    else:
        flash('Campi errati, segui le indicazioni fornite!', 'danger')
        return redirect(url_for('signup'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# FOLLOW E UNFOLLOW DI UN PODCAST
@app.route('/follow/<int:podcast_id>')
@login_required
def follow_podcast(podcast_id):
    userid = current_user.get_id()
    success = db_interaction.follow_podcast(userid, podcast_id)

    if success:
        flash('Hai iniziato a seguire il podcast', 'success')
    else:
        flash('Non hai iniziato a seguire il podcast, riprova!', 'danger')

    return redirect(url_for('podcast', podcast_id=podcast_id))

@app.route('/unfollow/<int:podcast_id>')
@login_required
def unfollow_podcast(podcast_id):
    userid = current_user.get_id()
    success = db_interaction.unfollow_podcast(userid, podcast_id)

    if success:
        flash('Hai smesso di seguire il podcast', 'success')
    else:
        flash('Non hai smesso si seguire il podcast, riprova!', 'danger')
    
    return redirect(url_for('podcast', podcast_id=podcast_id))


# PODCAST
@app.route('/nuovoPodcast')
@login_required
def nuovoPodcast():
    categorie = ['Tutte', 'Cucina', 'Scienza', 'Sport', 'Tecnologia', 'Altro']
    return render_template('nuovoPodcast.html', categorie=categorie)

@app.route('/nuovoPodcast', methods = ['POST'])
@login_required
def nuovoPodcast_post():
    userid = current_user.get_id()
    titolo = request.form.get('title')
    descrizione = request.form.get('description')
    categoria = request.form.get('category')
    immagine = request.files['immagine_podcast']
    filename = immagine.filename
    if (immagine and (".jpg" in filename or ".jpeg" in filename or ".png" in filename) and len(descrizione) >= 10 and len(titolo) >= 3 and len(titolo) <= 30 and categoria):
        if ".jpg" in filename:
            estensione = ".jpg"
        elif ".jpeg" in filename:
            estensione = ".jpeg"
        elif ".png" in filename:
            estensione = ".png"
            
        podcast = {'utente_id': userid, 'Descrizione': descrizione, 'Titolo': titolo, 'Categoria': categoria, 'Estensione': estensione}
        success = db_interaction.add_podcast(podcast)

        if success:
            flash('Podcast creato correttamente', 'success')
            podcast_id = success[0] 
            immagine.save('static/' + "podcast" + str(podcast_id) + estensione)
            return redirect(url_for('podcast', podcast_id=podcast_id))
        else:
            flash('Errore nella creazione del podcast: riprova!', 'danger')
            return redirect(url_for('home'))
    else:
        flash('Sono stati inseriti campi errati: riprova!', 'danger')
        return redirect(url_for('home'))

@app.route('/modificaPodcast/<podcast_id>')
@login_required
def modificaPodcast(podcast_id):
    podcast = db_interaction.get_podcast_by_id(podcast_id) 
    if podcast:
        if int(podcast['utente_id']) == int(current_user.get_id()):
            categorie = ['Tutte', 'Cucina', 'Scienza', 'Sport', 'Tecnologia', 'Altro']
            return render_template('modificaPodcast.html', podcast=podcast, categorie=categorie)
        else:
            flash('Non sei il creatore di questo podcast', 'danger')
            return redirect(url_for('home'))
    else:
        flash('La richiesta non è andata a buon fine', "danger")
        return redirect(url_for('home'))


@app.route('/modificaPodcast/<podcast_id>', methods = ['POST'])
@login_required
def modificaPodcast_post(podcast_id):
    podcast_id = request.form.get('podcast_id')
    current_podcast = db_interaction.get_podcast_by_id(podcast_id)

    current_filename =  'static/' + "podcast" + str(podcast_id) + current_podcast['Estensione']

    new_titolo = request.form.get('title')
    new_descrizione = request.form.get('description')
    new_categoria = request.form.get('category')
    new_image = request.files['immagine_podcast']
    filename = new_image.filename

    if (new_image and (".jpg" in filename or ".jpeg" in filename or ".png" in filename)):
        if ".jpg" in filename:
            estensione = ".jpg"
        elif ".jpeg" in filename:
            estensione = ".jpeg"
        elif ".png" in filename:
            estensione = ".png"

        os.remove(current_filename)
        filename = 'static/' + "podcast" + str(podcast_id) + estensione
        new_image.save(filename)

    # se c'è un'immagine però non è s
    if not new_image:
        estensione = current_podcast['Estensione']
            
    if new_titolo and len(new_titolo) >= 3 and len(new_titolo) <= 30:
        titolo = new_titolo
    else:
        titolo = current_podcast['Titolo']

    if new_descrizione and len(new_descrizione) >= 10:
        descrizione = new_descrizione
    else: 
        descrizione = current_podcast['Descrizione']

    if (new_categoria):
        categoria = new_categoria
    else: 
        categoria = current_podcast['Categoria']

    autore_id = current_podcast['utente_id']

    podcast = {'Titolo': titolo, 'Descrizione': descrizione, 'utente_id': autore_id, 'Categoria': categoria, 'podcast_id': podcast_id, 'Estensione': estensione}

    success = db_interaction.update_podcast(podcast)

    if success:
        flash('Podcast modificato', 'success')
    else:
        flash('Podcast non modificato', 'danger')
    
    return redirect(url_for('podcast', podcast_id=podcast_id))

@app.route('/cancellaPodcast/<podcast_id>')
@login_required
def cancellaPodcast(podcast_id):
    podcast = db_interaction.get_podcast_by_id(podcast_id)

    if podcast:
        if int(podcast['utente_id']) == int(current_user.get_id()):
             episodi = db_interaction.get_episodi_by_podcast_id(podcast_id)
             episodi_id = []
             estensioni = []
             for episodio in episodi:
                episodi_id.append(episodio['episodio_id'])
                estensioni.append(episodio['Estensione'])
                
             success = db_interaction.cancella_podcast_by_id(podcast_id)
            
             if success:
                filename = 'static/' + "podcast" + str(podcast_id) + podcast['Estensione']
                os.remove(filename)
                i = 0
                for id in episodi_id:
                    filename = 'static/' + "episodio" + str(id) + "podcast" + str(podcast_id) + estensioni[i]
                    os.remove(filename)
                    i = i+1
                flash('Podcast cancellato', 'success')
             else:
                flash('Podcast non cancellato', 'danger')
                return redirect(url_for('home')) 
        else:
            flash('Non sei il creatore di questo podcast', 'danger')
            return redirect(url_for('home'))
    else:
        flash('La richiesta non è andata a buon fine', "danger")
        return redirect(url_for('home'))

# GESTIONE DI UN EPISODIO
@app.route('/nuovoEpisodio/<podcast_id>')
@login_required
def nuovoEpisodio(podcast_id):
    return render_template('nuovoEpisodio.html', podcast_id=podcast_id)

@app.route('/nuovoEpisodio/<podcast_id>', methods = ['POST'])
@login_required
def nuovoEpisodio_post(podcast_id):
    titolo = request.form.get('title')
    data = date.today()
    descrizione = request.form.get('description')
    podcast_id = request.form.get('podcast_id')
    audio = request.files['fileaudio']
    filename = audio.filename
    if (audio and (".mp3" in filename or ".wav" in filename) and len(descrizione) >= 10 and len(titolo) >= 3 and len(titolo) <= 30):
        if ".mp3" in filename:
            estensione = ".mp3"
        elif ".wav" in filename:
            estensione = ".wav"

        episodio = {'Titolo': titolo, 'Descrizione': descrizione, 'DataCreazione': data, 'podcast_id': podcast_id, 'Estensione': estensione}
        episodio_id = db_interaction.add_episodio(episodio)

        if episodio_id:
            flash('Episodio creato correttamente', 'success')
            audio.save('static/' + "episodio" + str(episodio_id[0]) + "podcast" + str(podcast_id) + estensione)
            return redirect(url_for('podcast', podcast_id=podcast_id))
        else:
            flash('Errore nella creazione dell\'episodio: riprova!', 'danger')
            return redirect(url_for('nuovoEpisodio', podcast_id=podcast_id))
            
    else:
        flash('Errore nei campi inseriti', 'danger')
        return redirect(url_for('nuovoEpisodio', podcast_id=podcast_id))
        
@app.route('/cancellaEpisodio/<titolo>')
@login_required
def cancellaEpisodio(titolo):
    episodio = db_interaction.getEpisodio_fromTitolo(titolo)
    if episodio:
        podcast = db_interaction.get_podcast_by_id(episodio['podcast_id'])
        if int(podcast['utente_id']) == int(current_user.get_id()):
            success = db_interaction.cancellaEpisodio_byTitolo(titolo)
            podcast_id = episodio['podcast_id']
        
            if success:
                filename = 'static/' + "episodio" + str(episodio['episodio_id']) + "podcast" + str(podcast_id) + episodio['Estensione']
                os.remove(filename)
                flash('Episodio cancellato', 'success')
            else:
                flash('Episodio non cancellato', 'danger')
            
            return redirect(url_for('podcast', podcast_id=podcast_id))
        else:
            flash('Non sei il creatore di questo podcast', 'danger')
            return redirect(url_for('home'))
    else:
        flash('La richiesta non è andata a buon fine', "danger")
        return redirect(url_for('home'))


@app.route('/modificaEpisodio/<titolo>')
@login_required
def modificaEpisodio(titolo):
    episodio = db_interaction.getEpisodio_fromTitolo(titolo)
    if episodio:
        podcast = db_interaction.get_podcast_by_id(episodio['podcast_id'])
        if int(podcast['utente_id']) == int(current_user.get_id()):
            success = db_interaction.cancellaEpisodio_byTitolo(titolo)
            podcast_id = episodio['podcast_id']
        
            if success:
                filename = 'static/' + "episodio" + str(episodio['episodio_id']) + "podcast" + str(podcast_id) + episodio['Estensione']
                os.remove(filename)
                flash('Episodio cancellato', 'success')
            else:
                flash('Episodio non cancellato', 'danger')
            
            return redirect(url_for('podcast', podcast_id=podcast_id))
        else:
            flash('Non sei il creatore di questo podcast', 'danger')
            return redirect(url_for('home'))
    else:
        flash('La richiesta non è andata a buon fine', "danger")
        return redirect(url_for('home'))


@app.route('/modificaEpisodio/<titolo>', methods = ['POST'])
@login_required
def modificaEpisodio_post(titolo):
    podcast_id = request.form.get('podcast_id')
    episodio_id = request.form.get('episodio_id')
    
    current_episodio = db_interaction.getEpisodio_byID(episodio_id)
    #titolo = episodio['Titolo']

    current_filename =  'static/' + "episodio" + str(episodio_id) + "podcast" + str(podcast_id) + current_episodio['Estensione']

    new_titolo = request.form.get('title')
    new_descrizione = request.form.get('description')
    new_fileaudio = request.files['fileaudio']
    filename = new_fileaudio.filename

    if (new_fileaudio and (".mp3" in filename or ".wav" in filename)):
        if ".mp3" in filename:
            estensione = ".mp3"
        elif ".wav" in filename:
            estensione = ".wav"

        os.remove(current_filename)
        filename = 'static/' + "episodio" + str(episodio_id) + "podcast" + str(podcast_id) + estensione
        new_fileaudio.save(filename)

    if not new_fileaudio:
        estensione = current_episodio['Estensione']

    if new_titolo and len(new_titolo) >= 3 and len(new_titolo) <= 30:
        titolo = new_titolo
    else:
        titolo = current_episodio['Titolo']
    
    if new_descrizione and len(new_descrizione) >= 10:
        descrizione = new_descrizione
    else: 
        descrizione = current_episodio['Descrizione']

    dataCreazione = current_episodio['DataCreazione']

    episodio = {'Titolo': titolo, 'Descrizione': descrizione, 'DataCreazione': dataCreazione, 'podcast_id': podcast_id, 'Estensione': estensione}

    success = db_interaction.update_episodio(episodio, episodio_id)

    if success:
        flash('Episodio modificato', 'success')
    else:
        flash('Episodio non modificato', 'danger')
    
    return redirect(url_for('podcast', podcast_id=podcast_id))


# GESTIONE COMMENTI
@app.route('/nuovoCommento', methods = ['POST'])
def nuovoCommento_post():
    testo_commento = request.form.get('testo_commento')
    user_id = current_user.get_id()
    episodio_id = request.form.get('episodio_id')

    commento = {'utente_id': user_id, 'episodio_id': episodio_id, 'Testo': testo_commento}

    success = db_interaction.add_commento(commento)

    if success:
        flash('Commento creato correttamente', 'success')
    else:
        flash('Errore nella creazione del commento: riprova!', 'danger')
        
    return redirect(url_for('singoloEpisodio', episodio_id=episodio_id))

@app.route('/modificaCommento/<commento_id>')
@login_required
def modificaCommento(commento_id):
    commento = db_interaction.get_commento_by_id(commento_id)

    if commento:
        episodio = db_interaction.getEpisodio_byCommentoID(commento_id)
        podcast = db_interaction.get_podcast_by_id(episodio['podcast_id'])
        if int(podcast['utente_id']) == int(current_user.get_id()):
            return render_template('modificaCommento.html', episodio=episodio, commento=commento)
        else:
            flash('Non sei il creatore di questo podcast', 'danger')
            return redirect(url_for('home'))
    else:
        flash('La richiesta non è andata a buon fine', "danger")
        return redirect(url_for('home'))

           
@app.route('/modificaCommento/<commento_id>', methods = ['POST'])
@login_required
def modificaCommento_post(commento_id):
    testo_commento_new = request.form.get('testo_commento')
    commento_id = request.form.get('commento_id')
    episodio_id = request.form.get('episodio_id')
    
    if (len(testo_commento_new) > 0):
        commento_new = {'commento_id': commento_id, 'Testo': testo_commento_new}
        success = db_interaction.update_commento(commento_new)

        if success:
            flash('Commento modificato correttamente', 'success')
        else:
            flash('Errore nella modifica del commento: riprova!', 'danger')
        
        return redirect(url_for('singoloEpisodio', episodio_id=episodio_id))
    
    else:
        flash('Errore nella modifica del commento: deve avere almeno un carattere, riprova!', 'danger')

@app.route('/cancellaCommento/<commento_id>')
@login_required
def cancellaCommento(commento_id):
    episodio = db_interaction.getEpisodio_byCommentoID(commento_id)
    if episodio:
        episodio_id = episodio['episodio_id']
        commento = db_interaction.get_commento_by_id(commento_id)
        if int(commento['utente_id']) == int(current_user.get_id()):
            success = db_interaction.cancellaCommento_by_id(commento_id)

            if success:
                flash('Commento cancellato', 'success')
            else:
                flash('Commento non cancellato', 'danger')
            
            return redirect(url_for('singoloEpisodio', episodio_id=episodio_id))
        else:
            flash('Non sei lo scrittore di questo commento', 'danger')
            return redirect(url_for('home'))
    else:
        flash('La richiesta non è andata a buon fine', "danger")
        return redirect(url_for('home'))


# ERRORI
@app.errorhandler(404)
def page_not_found(e):
    titolo = "404 Not Found"
    testo = "La pagina richiesta non è stata trovata sul server."
    return render_template('errori.html', titolo=titolo, testo=testo), 404

@app.errorhandler(500)
def internal_server_error(e):
    titolo = "500 Internal Server Error"
    testo = "Il server ha incontrato un errore interno e non è in grado di elaborare la richiesta."
    return render_template('errori.html', titolo=titolo, testo=testo), 500

@app.errorhandler(403)
def forbidden(e):
    titolo = "403 Forbidden"
    testo = "Non hai i permessi per accedere a questa pagina."
    return render_template('errori.html', titolo=titolo, testo=testo), 403

@app.errorhandler(400)
def request_timeout(e):
    titolo = "400 Bad Request"
    testo = "La richiesta inviata al server non è valida."
    return render_template('errori.html', titolo=titolo, testo=testo), 400

@app.errorhandler(408)
def request_timeout(e):
    titolo = "408 Request Timeout"
    testo = "La richiesta non è stata completata entro il tempo previsto."
    return render_template('errori.html', titolo=titolo, testo=testo), 408

@app.errorhandler(503)
def request_timeout(e):
    titolo = "503 Service Unavailable"
    testo = "Il server non è al momento in grado di gestire la richiesta a causa di un sovraccarico temporaneo o di manutenzione del server."
    return render_template('errori.html', titolo=titolo, testo=testo), 503


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)