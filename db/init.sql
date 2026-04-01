USE rfid_crociera;

CREATE TABLE IF NOT EXISTS passeggeri (
  uid            VARCHAR(20) PRIMARY KEY,
  nome           VARCHAR(100) NOT NULL,
  cabina         VARCHAR(20),
  allergie       TEXT,
  saldo          DECIMAL(10,2) DEFAULT 0.00,
  autorizzazioni TEXT,
  creato_il      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS eventi_accesso (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  uid        VARCHAR(20) NOT NULL,
  reader_id  VARCHAR(50) NOT NULL,
  zona       VARCHAR(100),
  esito      ENUM('OK','KO') NOT NULL,
  timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES passeggeri(uid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posizioni (
  uid         VARCHAR(20) PRIMARY KEY,
  ultima_zona VARCHAR(100),
  aggiornato  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES passeggeri(uid)
);

CREATE TABLE IF NOT EXISTS transazioni (
  id        INT AUTO_INCREMENT PRIMARY KEY,
  uid       VARCHAR(20) NOT NULL,
  importo   DECIMAL(8,2) NOT NULL,
  servizio  VARCHAR(100),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW IF NOT EXISTS dispersi AS
  SELECT p.nome, p.cabina, pos.ultima_zona, pos.aggiornato
  FROM passeggeri p
  LEFT JOIN posizioni pos ON p.uid = pos.uid
  WHERE pos.ultima_zona NOT LIKE '%Muster%'
     OR pos.ultima_zona IS NULL;