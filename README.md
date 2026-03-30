# Sistema Digitale Integrato per Nave da Crociera

Questo progetto simula il cuore digitale di una nave da crociera moderna: ogni passeggero riceve una **card con ID univoco** che gli permette di aprire la propria cabina, pagare a bordo e risultare sempre localizzato per la sicurezza.

---

## Cosa fa, in concreto?

### Accesso alle Cabine
La card apre la porta della cabina assegnata. Il sistema riconosce la tessera, verifica l'associazione e registra ogni tentativo — riuscito o negato. 
Esattamente come sulle navi reali.

### Pagamenti a Bordo
La stessa card diventa un portafoglio digitale. Ristorante, negozi, bar: il passeggero avvicina la card e il saldo si aggiorna. Ogni transazione viene salvata, il saldo è sempre visibile e la ricarica è immediata.

### Sicurezza e Tracciamento RFID
Sulla nave sono presenti vari reader che rilevano automaticamente il passaggio delle card. In questo modo è sempre possibile sapere chi è a bordo, chi è sceso a terra e chi non viene rilevato da troppo tempo — un sistema fondamentale in caso di emergenza.

---

## Come è costruito

| Componente | Ruolo nel progetto |
|---|---|
| **Python + Flask** | Backend web: gestisce le logiche, le pagine e i servizi |
| **MySQL** | Database relazionale: salva passeggeri, accessi, transazioni e rilevazioni |
| **HTML/CSS + Jinja2** | Dashboard web: mostra tutto in tempo reale |
| **Moduli RFID RC522 / MFRC522** | Simulano i lettori di card fisici (cabine, casse, reader di bordo) |

---

## Perché RC522?

I moduli **MFRC522** sono la scelta naturale per un progetto come questo:
- Economici e facili da reperire
- Compatibili con tag **MIFARE Classic 1K**
- Comunicano via **SPI**, semplici da collegare a microcontrollori
- Ampiamente documentati e utilizzati in ambito didattico

La stessa card funziona per tutto: apre la cabina, paga al ristorante, viene rilevata dai reader. Proprio come accade sulle navi vere.

---

## Struttura del Progetto
```
/
├── sistema_cabine/       # Accessi, tentativi, log porte
├── sistema_pagamenti/    # Saldo, transazioni, ricariche
├── sistema_sicurezza/    # Reader RFID, posizione passeggeri
└── dashboard/            # Interfaccia web di monitoraggio
```

Tutti e tre i moduli condividono lo stesso database MySQL e sono monitorabili dalla dashboard in tempo reale.

---

## Requisiti

- Python 3.x
- Flask
- MySQL
- Hardware: modulo MFRC522 + tag MIFARE Classic 1K

---

*Progetto scolastico — sviluppato per simulare i sistemi digitali reali presenti sulle navi da crociera moderne.*
