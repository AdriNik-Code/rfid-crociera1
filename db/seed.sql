INSERT INTO passeggeri (uid, nome, cabina, allergie, saldo, autorizzazioni) VALUES
  ('A1B2C3D4', 'Mario Rossi',    'Deck5-C12', 'nessuna',  250.00, 'cabina,ristorante,spa'),
  ('11223344', 'Laura Bianchi',  'Deck3-A08', 'glutine',  180.00, 'cabina,ristorante'),
  ('AABBCCDD', 'Marco Verdi',    'Deck7-B22', 'nessuna',  500.00, 'cabina,ristorante,spa,piscina'),
  ('FFEE1122', 'Capo Equipaggio','CREW-01',   'nessuna',    0.00, 'tutto');

INSERT INTO posizioni (uid, ultima_zona) VALUES
  ('A1B2C3D4', 'Deck5-Corridoio'),
  ('11223344', 'Ristorante-Principale'),
  ('AABBCCDD', 'Piscina-Lido'),
  ('FFEE1122', 'Plancia');
```

**Infine dentro `app/`** crea `requirements.txt`:
```
Flask==3.0.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
pyserial==3.5