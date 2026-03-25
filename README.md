# Sistema Digitale Integrato per Nave da Crociera

Il progetto simula i principali sistemi digitali presenti su una nave da crociera moderna.  
Ogni passeggero riceve una **card con ID univoco**, che permette di interagire con tre funzioni fondamentali:  
- accesso alla cabina  
- pagamenti a bordo  
- sicurezza e tracciamento  

L’obiettivo è mostrare come un’unica card possa diventare la chiave di tutto ciò che il passeggero fa durante la crociera.

---

## 1. Sistema di Accesso alle Cabine

La card permette al passeggero di aprire la propria cabina.  
Il sistema:

- riconosce la card  
- verifica a quale cabina è associata  
- registra ogni tentativo di accesso (riuscito o negato)

Questo simula il funzionamento delle porte elettroniche presenti sulle navi reali.

---

## 2. Sistema Pagamenti a Bordo

La card funziona come un **portafoglio digitale**.  
Il passeggero può usarla per:

- acquistare prodotti nei negozi  
- pagare al ristorante  
- ricaricare il proprio saldo  

Il sistema mantiene lo storico delle spese e il saldo rimanente.

---

## 3. Sistema di Sicurezza con Reader RFID

Sulla nave sono presenti vari **reader** che rilevano automaticamente il passaggio delle card.  
Questo permette di sapere:

- chi è a bordo  
- chi è sceso a terra  
- chi non è stato rilevato di recente  

È una simulazione dei sistemi reali usati per la sicurezza e per la gestione delle emergenze.

---

# Strumenti Utilizzati

### **Python + Flask**
Utilizzati per creare l’applicazione web che gestisce tutti i sistemi.  
Flask permette di definire pagine, funzioni e servizi in modo semplice e veloce.

### **MySQL**
SQLite è un database leggero, perfetto per un progetto scolastico.  
SQLAlchemy permette di gestire i dati in modo ordinato e sicuro.

### **HTML/CSS + Jinja2**
Usati per costruire la **dashboard web**, che mostra:

- lo stato dei passeggeri  
- gli accessi alle cabine  
- le transazioni  
- le rilevazioni dei reader  

Jinja2 permette di inserire dati dinamici nelle pagine HTML.

---

# Organizzazione del Progetto

Il progetto è diviso in tre parti principali:

1. **Sistema Cabine** – Gestisce accessi e tentativi di apertura.  
2. **Sistema Pagamenti** – Gestisce saldo, acquisti e storico transazioni.  
3. **Sistema Sicurezza** – Gestisce reader RFID e posizione dei passeggeri.

Tutti i sistemi condividono lo stesso database e sono controllati da una dashboard web che permette di monitorare la nave in tempo reale.

---

# RC522 per la Simulazione delle Cabine

Per simulare l’accesso alle cabine vengono utilizzati i **moduli RFID RC522**, dispositivi economici e molto diffusi nei progetti didattici.

I motivi della scelta:

- perfetti per simulare una porta elettronica  
- facili da integrare con microcontrollori  
- affidabili e ben documentati  
- costo molto basso  

Ogni cabina avrà un RC522 che legge la card del passeggero e invia l’ID al backend, che decide se l’accesso è consentito o negato.



---

# RC522 anche per i Pagamenti

Per mantenere il sistema coerente e a basso costo, gli stessi moduli **RC522** vengono utilizzati anche per simulare i pagamenti a bordo.

In questo modo:

- la stessa card funziona sia come chiave della cabina sia come portafoglio digitale  
- un RC522 posizionato in un “punto cassa” legge l’ID della card  
- il backend scala il saldo del passeggero  
- ogni pagamento viene registrato nello storico transazioni  

Questa scelta rende il sistema realistico, semplice da dimostrare e perfetto per un progetto scolastico a budget limitato.

---
