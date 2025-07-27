# santander-csv-formater

Important: This script works only for German accounts as fields are in German. But feel free to modify it for your needs :).

## TL;DR

Liest ein CSV Export der Umsätze eines Santander Kontos ein und erstellt daraus eine CSV Datei in einem sinnvoll nutzbaren Format. Der Verwendungszweck wird aufgeteilt. Dadurch kann die Zieldatei besser in andere Programme importiert werden (bspw. Buchhaltung).

Reads the CSV export of transactions from a Santander account and creates a CSV file out of it that has a usable format. The purpose field is split into parts. With that the target file can be imported better into other applications (e.g. accounting).

```bash
python3 santander-csv-formater.py -i <input> -o <output>
```
Beispiel / Example:

```bash
python3 santander-csv-formater.py -i transactions.csv -o target.csv
```

## Verkürztes Beispiel / Shortened example

### Quelle / Source

```
Kontonummer:;DE1234

Kontostand vom 01.02.2025 (EUR):1,00

Buchungsdatum;Wertstellung;Betrag(EUR);Saldo(EUR);Verwendungszweck
01.01.2025;01.01.2025;10,00;100,00;ÜBERWEISUNG VON Testfirma     12345678901ABCDEFG IBAN    DE1234 BIC ABC123 EREF+001234  MREF+09876   CRED+123-456-789  SVWZ+Sonderzahlung wegen sonstwas                       
```

### Ziel / Target

```
Buchungsdatum;Wertstellung;Betrag;Saldo;Empfänger;TransferID;IBAN;BIC;Verwendungszweck;EREF;MREF;CRED
01.01.2025;01.01.2025;10,00;100,00;Testfirma;12345678901ABCDEFG;DE1234;ABC123;Sonderzahlung wegen sonstwas;001234;09876;123-456-789
```