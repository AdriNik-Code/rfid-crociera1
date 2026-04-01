import os
import random
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')

# ---------------------------------------------------------------------------
# Configurazione database
# ---------------------------------------------------------------------------

def get_db_connection():
    """Crea e restituisce una connessione al database MySQL."""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST', 'db'),
            port=int(os.environ.get('MYSQL_PORT', 3306)),
            database=os.environ.get('MYSQL_DATABASE', 'rfid_crociera'),
            user=os.environ.get('MYSQL_USER', 'rfid_user'),
            password=os.environ.get('MYSQL_PASSWORD', ''),
        )
        return conn
    except Error as e:
        print(f"Errore connessione DB: {e}")
        return None


# ---------------------------------------------------------------------------
# Rotte principali
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Redirect alla dashboard principale."""
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Dashboard principale con gli ultimi eventi RFID."""
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', error="Impossibile connettersi al database.", eventi=[], passeggeri_totali=0, accessi_oggi=0, dispersi=0)

    cursor = conn.cursor(dictionary=True)

    # Ultimi 20 eventi
    cursor.execute("""
        SELECT e.id, e.uid, p.nome, e.reader_id, e.zona, e.esito, e.timestamp
        FROM eventi_accesso e
        LEFT JOIN passeggeri p ON e.uid = p.uid
        ORDER BY e.timestamp DESC
        LIMIT 20
    """)
    eventi = cursor.fetchall()

    # Contatori per le card statistiche
    cursor.execute("SELECT COUNT(*) AS tot FROM passeggeri")
    passeggeri_totali = cursor.fetchone()['tot']

    cursor.execute("SELECT COUNT(*) AS tot FROM eventi_accesso WHERE DATE(timestamp) = CURDATE()")
    accessi_oggi = cursor.fetchone()['tot']

    cursor.execute("SELECT COUNT(*) AS tot FROM dispersi")
    dispersi = cursor.fetchone()['tot']

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        eventi=eventi,
        passeggeri_totali=passeggeri_totali,
        accessi_oggi=accessi_oggi,
        dispersi=dispersi,
        error=None
    )


# ---------------------------------------------------------------------------
# Gestione passeggeri
# ---------------------------------------------------------------------------

@app.route('/passeggeri')
def passeggeri():
    """Lista di tutti i passeggeri registrati."""
    conn = get_db_connection()
    if not conn:
        return render_template('passeggeri.html', error="DB non raggiungibile.", passeggeri=[])

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, pos.ultima_zona, pos.ultimo_aggiornamento
        FROM passeggeri p
        LEFT JOIN posizioni pos ON p.uid = pos.uid
        ORDER BY p.nome
    """)
    lista = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('passeggeri.html', passeggeri=lista, error=None)


@app.route('/passeggeri/<uid>')
def dettaglio_passeggero(uid):
    """Dettaglio di un singolo passeggero con storico eventi."""
    conn = get_db_connection()
    if not conn:
        return render_template('dettaglio.html', error="DB non raggiungibile.", passeggero=None, eventi=[], transazioni=[])

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM passeggeri WHERE uid = %s", (uid,))
    passeggero = cursor.fetchone()

    if not passeggero:
        cursor.close()
        conn.close()
        return render_template('dettaglio.html', error="Passeggero non trovato.", passeggero=None, eventi=[], transazioni=[])

    cursor.execute("""
        SELECT * FROM eventi_accesso WHERE uid = %s ORDER BY timestamp DESC LIMIT 50
    """, (uid,))
    eventi = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM transazioni WHERE uid = %s ORDER BY timestamp DESC LIMIT 20
    """, (uid,))
    transazioni = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dettaglio.html', passeggero=passeggero, eventi=eventi, transazioni=transazioni, error=None)


# ---------------------------------------------------------------------------
# Simulazione emergenza
# ---------------------------------------------------------------------------

@app.route('/emergenza')
def emergenza():
    """Pagina simulazione emergenza - mostra i dispersi."""
    conn = get_db_connection()
    if not conn:
        return render_template('emergenza.html', error="DB non raggiungibile.", dispersi=[], totale_passeggeri=0)

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM dispersi ORDER BY nome")
    dispersi = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS tot FROM passeggeri")
    totale = cursor.fetchone()['tot']

    cursor.close()
    conn.close()

    al_sicuro = totale - len(dispersi)

    return render_template(
        'emergenza.html',
        dispersi=dispersi,
        totale_passeggeri=totale,
        al_sicuro=al_sicuro,
        error=None
    )


# ---------------------------------------------------------------------------
# Simulatore lettura tag (senza Arduino fisico)
# ---------------------------------------------------------------------------

READERS = [
    {'id': 'READER-CABINA-A1',    'zona': 'Deck5-Cabina-A1'},
    {'id': 'READER-CABINA-B3',    'zona': 'Deck5-Cabina-B3'},
    {'id': 'READER-CORRIDOIO-A',  'zona': 'Deck3-Corridoio-Prua'},
    {'id': 'READER-CORRIDOIO-B',  'zona': 'Deck3-Corridoio-Poppa'},
    {'id': 'READER-RISTORANTE',   'zona': 'Deck7-Ristorante'},
    {'id': 'READER-SPA',          'zona': 'Deck8-Spa'},
    {'id': 'READER-POS-BAR',      'zona': 'Deck6-Bar'},
    {'id': 'READER-MUSTER-1',     'zona': 'Deck2-MusterStation-1'},
    {'id': 'READER-MUSTER-2',     'zona': 'Deck2-MusterStation-2'},
]


@app.route('/simulatore')
def simulatore():
    """Pagina del simulatore lettura tag RFID."""
    conn = get_db_connection()
    if not conn:
        return render_template('simulatore.html', error="DB non raggiungibile.", passeggeri=[], readers=READERS)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT uid, nome, autorizzazioni, saldo FROM passeggeri ORDER BY nome")
    passeggeri = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('simulatore.html', passeggeri=passeggeri, readers=READERS, error=None)


@app.route('/simulatore/leggi', methods=['POST'])
def simula_lettura():
    """
    Simula la lettura di un tag RFID da un reader.
    Riceve uid e reader_id via POST, scrive l'evento nel DB.
    """
    uid = request.form.get('uid', '').strip()
    reader_id = request.form.get('reader_id', '').strip()

    if not uid or not reader_id:
        return jsonify({'success': False, 'messaggio': 'UID e reader obbligatori'}), 400

    # Trova la zona del reader selezionato
    zona = next((r['zona'] for r in READERS if r['id'] == reader_id), 'Zona sconosciuta')

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'messaggio': 'DB non raggiungibile'}), 500

    cursor = conn.cursor(dictionary=True)

    # Recupera il passeggero
    cursor.execute("SELECT * FROM passeggeri WHERE uid = %s", (uid,))
    passeggero = cursor.fetchone()

    if not passeggero:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'messaggio': f'UID {uid} non trovato nel database'}), 404

    # Controlla le autorizzazioni
    autorizzazioni = passeggero.get('autorizzazioni', '') or ''
    aree_consentite = [a.strip().lower() for a in autorizzazioni.split(',')]

    # Mappa reader → parola chiave autorizzazione
    mappa_auth = {
        'READER-CABINA':      'cabina',
        'READER-CORRIDOIO':   'corridoio',
        'READER-RISTORANTE':  'ristorante',
        'READER-SPA':         'spa',
        'READER-POS-BAR':     'bar',
        'READER-MUSTER':      'muster',
    }

    esito = 'KO'
    for prefisso, area in mappa_auth.items():
        if reader_id.startswith(prefisso) and area in aree_consentite:
            esito = 'OK'
            break
    # Le muster station sono sempre accessibili (emergenza)
    if reader_id.startswith('READER-MUSTER'):
        esito = 'OK'

    # Scrivi l'evento nel DB
    cursor.execute("""
        INSERT INTO eventi_accesso (uid, reader_id, zona, esito)
        VALUES (%s, %s, %s, %s)
    """, (uid, reader_id, zona, esito))

    # Aggiorna la posizione del passeggero
    cursor.execute("""
        INSERT INTO posizioni (uid, ultima_zona, ultimo_aggiornamento)
        VALUES (%s, %s, NOW())
        ON DUPLICATE KEY UPDATE ultima_zona = %s, ultimo_aggiornamento = NOW()
    """, (uid, zona, zona))

    # Se è un POS, simula un pagamento
    importo = None
    if reader_id == 'READER-POS-BAR' and esito == 'OK':
        importo = round(random.uniform(2.5, 15.0), 2)
        if passeggero['saldo'] >= importo:
            cursor.execute("UPDATE passeggeri SET saldo = saldo - %s WHERE uid = %s", (importo, uid))
            cursor.execute("""
                INSERT INTO transazioni (uid, importo, descrizione)
                VALUES (%s, %s, %s)
            """, (uid, importo, f'Acquisto bar - {zona}'))
        else:
            esito = 'KO'
            importo = None
            # Aggiorna l'evento appena inserito
            cursor.execute("""
                UPDATE eventi_accesso SET esito = 'KO'
                WHERE uid = %s ORDER BY timestamp DESC LIMIT 1
            """, (uid,))

    conn.commit()

    # Rileggi il saldo aggiornato
    cursor.execute("SELECT saldo FROM passeggeri WHERE uid = %s", (uid,))
    saldo_aggiornato = cursor.fetchone()['saldo']

    cursor.close()
    conn.close()

    risposta = {
        'success': True,
        'uid': uid,
        'nome': passeggero['nome'],
        'reader_id': reader_id,
        'zona': zona,
        'esito': esito,
        'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'saldo': float(saldo_aggiornato),
    }
    if importo:
        risposta['importo_scalato'] = importo

    return jsonify(risposta)


# ---------------------------------------------------------------------------
# API JSON (per aggiornamenti live della dashboard)
# ---------------------------------------------------------------------------

@app.route('/api/ultimi-eventi')
def api_ultimi_eventi():
    """Restituisce gli ultimi 10 eventi in formato JSON (per polling AJAX)."""
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.uid, p.nome, e.reader_id, e.zona, e.esito,
               DATE_FORMAT(e.timestamp, '%%d/%%m/%%Y %%H:%%i:%%s') AS timestamp
        FROM eventi_accesso e
        LEFT JOIN passeggeri p ON e.uid = p.uid
        ORDER BY e.timestamp DESC
        LIMIT 10
    """)
    eventi = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(eventi)


@app.route('/api/statistiche')
def api_statistiche():
    """Restituisce le statistiche principali in JSON."""
    conn = get_db_connection()
    if not conn:
        return jsonify({})

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS tot FROM passeggeri")
    passeggeri_totali = cursor.fetchone()['tot']

    cursor.execute("SELECT COUNT(*) AS tot FROM eventi_accesso WHERE DATE(timestamp) = CURDATE()")
    accessi_oggi = cursor.fetchone()['tot']

    cursor.execute("SELECT COUNT(*) AS tot FROM dispersi")
    dispersi = cursor.fetchone()['tot']

    cursor.execute("SELECT COUNT(*) AS tot FROM eventi_accesso WHERE esito='KO' AND DATE(timestamp) = CURDATE()")
    accessi_negati = cursor.fetchone()['tot']

    cursor.close()
    conn.close()

    return jsonify({
        'passeggeri_totali': passeggeri_totali,
        'accessi_oggi': accessi_oggi,
        'dispersi': dispersi,
        'accessi_negati': accessi_negati,
    })


# ---------------------------------------------------------------------------
# Avvio applicazione
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    port = int(os.environ.get('APP_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
