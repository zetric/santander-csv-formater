# santander-csv-formatter

⚠️ Important: This script works only for German accounts as fields are in German. But feel free to modify it acording to your needs :).

## 🏃‍➡️ TL;DR

Reads the CSV export of transactions from a Santander account and creates a CSV file out of it that has a usable format. The purpose field is split into parts. With that the target file can be imported better into other applications (e.g. accounting).

```bash
python3 santander-csv-formatter.py -i <input> -o <output> -a "<account owner>"
```
Example:

```bash
python3 santander-csv-formatter.py -i transactions.csv -o target.csv -a "My Name"
```

| Parameter       | Meaning                                                                                                   | 
| --------------- | --------------------------------------------------------------------------------------------------------- |
| `input`         | CSV input file with transactions exported from Santander bank web UI                                      |
| `output`        | CSV output file with transactions parsed by the script                                                    |
| `account owner` | The name of the account owner for assigning a name to income bookings without a receiver (e.g. dividends) |

##  🧾 Shortened example

### Source

```
Kontonummer:;DE1234

Von:;01.01.2025
Bis:;30.01.2025
Kontostand vom 30.01.2025 (EUR):1,00

Buchungsdatum;Wertstellung;Betrag(EUR);Saldo(EUR);Verwendungszweck
01.01.2025;01.01.2025;10,00;100,00;ÜBERWEISUNG VON Testfirma     12345678901ABCDEFG IBAN    DE1234 BIC ABC123 EREF+001234  MREF+09876   CRED+123-456-789  SVWZ+Sonderzahlung wegen sonstwas                       
```

### Target

```
Buchungsdatum;Wertstellung;Betrag;Saldo;Empfänger;TransferID;IBAN;BIC;Verwendungszweck;EREF;MREF;CRED
01.01.2025;01.01.2025;10,00;100,00;Testfirma;12345678901ABCDEFG;DE1234;ABC123;Sonderzahlung wegen sonstwas;001234;09876;123-456-789
```

## Curently supported booking types

- Dividens starting with `ISIN`
- Transfers starting with `ECHTZEIT-ÜBERWEISUNG` or  `ÜBERWEISUNG`
- Debits starting with `SEPA-LASTSCHRIFT`
- Card payments starting with `ZAHLUNG AN` (no recipient IBAN or BIC here as Santander does not show them neither online nor in the export)
- Cash payouts starting wiht `BARGELDAUSZAHLUNG`

## 🙋 Disclaimer

Humans make mistakes. Due to that the code is provided as is without any warrenty (see license). Especially please check the resulting CSV file for errors.
If you find any errors, please report an issue.