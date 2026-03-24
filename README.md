#  Progetto RFID Crociera
Sistema di tracciamento passeggeri – Laboratorio TIPSIT

Un sistema RFID che simula il funzionamento delle navi da crociera: controllo accessi, tracciamento passeggeri, pagamenti contactless e dashboard in tempo reale.


##  Funzionalità
- Lettura tag RFID (Arduino + RC522)
- Registrazione eventi in MySQL
- Dashboard Flask in tempo reale
- Controllo accessi (OK/KO)
- Simulazione emergenza (vista `dispersi`)
- Pagamenti simulati con saldo cabina


##  Architettura

### Flusso dati
1. RC522 legge il tag  
2. Arduino invia l’UID via seriale  
3. Python scrive l’evento nel DB  
4. Flask mostra gli eventi sulla dashboard  

### Stack
| Livello | Tecnologia |
|--------|------------|
| Hardware | Arduino + RC522 |
| Backend | Python + Flask |
| Database | MySQL (Docker) |
| Deploy | Docker Compose + SSH |
| Versioning | GitHub |


##  Database

### Tabelle principali
| Tabella | Contenuto |
|---------|-----------|
| passeggeri | dati passeggero + saldo |
| eventi_accesso | log letture RFID |
| posizioni | ultima zona rilevata |
| transazioni | pagamenti simulati |

##  Collegamenti RC522 → Arduino

| Pin RC522 | Pin Arduino Uno | Funzione |
|-----------|------------------|----------|
| **VCC**   | 3.3V             | Alimentazione ( solo 3.3V) |
| **GND**   | GND              | Massa |
| **SCK**   | 13               | Clock SPI |
| **MOSI**  | 11               | Dati verso RC522 |
| **MISO**  | 12               | Dati dal RC522 |
| **SDA / SS** | 10           | Chip Select |
| **RST**   | 9                | Reset modulo |


