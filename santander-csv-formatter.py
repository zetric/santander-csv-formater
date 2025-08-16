#!/usr/bin/python3

import csv
import re
import argparse
import os
import sys
from pathlib import Path

######################
# Constants
######################

TARGET_HEADER=['Buchungsdatum','Wertstellung','Betrag','Saldo','Empfänger','TransferID','IBAN','BIC','Verwendungszweck','EREF','MREF','CRED']
TMP_FILE="_tmp.csv"

######################
# Export functions
######################

def receiver(row):
  data = re.findall(r'(?:.*VON |AN )(.*)(?: \b[0-9]{11}[A-Z]{7}\b IBAN)', row)
  if data:
    return(data[0])
  else:
    return("")

def transfer_id(row):
  data = re.findall(r'(?:.*)(\b[0-9]{11}[A-Z]{7}\b)(?: IBAN)', row)
  if data:
    return(data[0])
  else:
    return("")

def iban(row):
  data = re.findall(r'IBAN *(\b[A-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16})', row)
  if data:
    return(data[0][0])
  else:
    return("")

def bic(row):
  data = re.findall(r'BIC (\b[A-Z0-9]*\b)', row)
  if data:
    return(data[0])
  else:
    return("")
  
def purpose(row):
  data = re.findall(r'SVWZ[+](.*)', row)
  if data:
    return(data[0])
  else:
    return("")
  
def eref(row):
  data = re.findall(r"EREF[+]([A-Za-z0-9+?\/\-:().,']*)", row)
  if data:
    return(data[0])
  else:
    return("")
  
def mref(row):
  data = re.findall(r"MREF[+]([A-Za-z0-9+?\/\-:().,']*)", row)
  if data:
    return(data[0])
  else:
    return("")
  
def cred(row):
  data = re.findall(r"CRED[+]([A-Za-z0-9+?\/\-:().,']*)", row)
  if data:
    return(data[0])
  else:
    return("")


######################
# Row handler
######################

def transfer(data_purpose_raw):
  row_return = []
  
  # Remove additional whitespaces
  data_clean = str(re.sub(r' +', ' ', data_purpose_raw)).strip()
  
  # Receiver
  data_receiver = receiver(data_clean)
  if data_receiver:
    row_return.append(data_receiver)
  else:
    row_return.append("")
  
  # Transfer ID
  data_transfer_id = transfer_id(data_clean)
  if data_transfer_id:
    row_return.append(data_transfer_id)
  else:
    row_return.append("")
  
  # IBAN
  data_iban = iban(data_clean)
  if data_iban:
    row_return.append(data_iban)
  else:
    row_return.append("")

  # BIC
  data_bic = bic(data_clean)
  if data_bic:
    row_return.append(data_bic)
  else:
    row_return.append("")

  # Purpose
  data_purpose = purpose(data_clean)
  if data_purpose:
    row_return.append(data_purpose)
  else:
    row_return.append("")

  # EREF
  data_eref = eref(data_clean)
  if data_eref:
    row_return.append(data_eref)
  else:
    row_return.append("")

  # MREF
  data_mref = mref(data_clean)
  if data_mref:
    row_return.append(data_mref)
  else:
    row_return.append("")
  
  # CRED
  data_cred = cred(data_clean)
  if data_cred:
    row_return.append(data_cred)
  else:
    row_return.append("")

  return row_return


######################
# Main start
######################

# Check if arguments were passed
if not len(sys.argv) > 1:
  print("No arguments passed. Use '-h' parameter for help.")
  sys.exit(0)

# Parsing arguments
parser = argparse.ArgumentParser(description="This script will convert raw CSV file exports from the Santander bank and convert it into a usable format (German field names).")
parser.add_argument('-i', action="store", required=True, dest="inputfile", help="csv input file")
parser.add_argument('-o', action="store", required=True, dest="outputfile", help="csv output file")
args = parser.parse_args()

SOURCE_FILE = args.inputfile
TARGET_FILE = args.outputfile

# Cleanup target and tmp file
target_file = Path(TARGET_FILE)
if target_file.is_file():
  os.remove(TARGET_FILE)
tmp_file = Path(TMP_FILE)
if tmp_file.is_file():
  os.remove(TMP_FILE)

# Cleanup source file (remove useless garbage)
with open(SOURCE_FILE,"r") as source_file:
  
  content = source_file.readlines()
    
  with open(TMP_FILE, mode="a") as tmp_file:
    for row in content:
      if re.findall(r'[0-9]*', row.split('.')[0])[0] or row.find("Buchungsdatum") >= 0:
        tmp_file.write(row.rstrip() + "\n")



# Start
with open(TMP_FILE) as source_file:
  
  content = csv.DictReader(source_file, delimiter=';')
  
  with open(TARGET_FILE, mode="a") as target_file:
  
    writer = csv.DictWriter(target_file, fieldnames=TARGET_HEADER, delimiter=';')
    writer.writeheader()
  
    for row in content:
  
      data_date = row['Buchungsdatum']
      data_valuta = row['Wertstellung']
      data_sum = row['Betrag(EUR)']
      data_position = row['Saldo(EUR)']
      data_purpose_raw = str(re.sub(r' +', ' ',row['Verwendungszweck'])).strip()

      
      row_transfer = re.findall(r'VON|AN', data_purpose_raw)
      if row_transfer:
        data_transfer = transfer(data_purpose_raw)
        target_row={'Buchungsdatum': data_date,
                    'Wertstellung': data_valuta,
                    'Betrag': data_sum,
                    'Saldo': data_position,
                    'Empfänger': data_transfer[0],
                    'TransferID': data_transfer[1],
                    'IBAN': data_transfer[2],
                    'BIC': data_transfer[3],
                    'Verwendungszweck': data_transfer[4],
                    'EREF': data_transfer[5],
                    'MREF': data_transfer[6],
                    'CRED': data_transfer[7]}

           
      writer.writerow(target_row)

# Clean up tmp file
os.remove(TMP_FILE)