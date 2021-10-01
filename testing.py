#!/usr/bin/env python3
#ConfigurationManager.ConnectionStrings["myDatabaseConnection"].ConnectionString;  
import pypyodbc
import mariadb
import logging
import time
import datetime
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet
import os
#logfailu izveido un ieraksta tajā padoto info
def logFileWriting(txt):
  logging.basicConfig(filename="someLogFile.log",
    format='%(asctime)s %(message)s',
    filemode='a')
  logger=logging.getLogger()
  logger.setLevel(logging.DEBUG)
  logger.info(txt)
#FUNKCIJAS KAS UZĢENERĒ ATSLĒGU ŠIFRĒŠANAI
def write_key():
    key = Fernet.generate_key()
    #IERAKSTA FAILĀ ATSSLĒGU
    with open("key.key", "wb") as key_file:
        key_file.write(key)
#FUNKCIJAS KAS IELĀDĒ ATSLĒGU NO ESOŠA KEY FAILA
def load_key():

    return open("key.key", "rb").read()
#FUNKCIJAS KAS NOŠIFRĒ FAILU
def encrypt(filename, key):

    f = Fernet(key)
    with open(filename, "rb") as file:
        #LASA FAILU
        file_data = file.read()
    # NOŠIFRĒ
    encrypted_data = f.encrypt(file_data)
    # IERAKSTA FAILĀ NOŠIFRĒTO
    with open(filename, "wb") as file:
        file.write(encrypted_data)
#FUNKCIJAS KAS ATŠIFRĒ FAILU
def decrypt(filename, key):

    f = Fernet(key)
    with open(filename, "rb") as file:
        # LASA FAILU
        encrypted_data = file.read()
    #ATŠIFRĒ FAILU
    decrypted_data = f.decrypt(encrypted_data)
    #IERAKSTA FAILĀ ATŠIFRĒJUMU
    with open(filename, "wb") as file:
        file.write(decrypted_data)

#nebeidzamais loops, kurš iet no 7-22 dienā
def endlessLoop():
  a=bool(True)
  startTime = time.strftime('07:00:00', time.localtime())
  endTime = time.strftime('22:00:00', time.localtime())
  while(a):
    #lokālais laiks
    timeLocal = time.strftime('%H:%M:%S', time.localtime())  
    try:
    #Ja lokālais laiks ir starp sākuma un beigu laika, tad ieies ifā
      if timeLocal>=startTime and timeLocal<=endTime: 
        connBool = connections()
        cursor = connBool.cursor()
        #pievieno vērtības db
        cursor.execute('''INSERT INTO testTable(FirstName,LastName) VALUES
          ('Jautrite','bersina')''')
        connBool.commit()
        #izdzēš visas vērtības no db
        cursor.execute('''DELETE FROM testTable ''')
        connBool.commit()
        connBool.close()
        #logfaaila funkciju izsauc, lai ierakstītu failā pārbaudes info
        logFileWriting('Is working in loop!!!')
      else: #nav konkrētā laika periodā, aiziet uz miegu uz 9 stundām
        logFileWriting('Out of time period!!')
        time.sleep(32400) # 9h from 22-07.00
        #logFileWriting(timeLocal)
      #a = False
    except Exception as e:
      logFileWriting(logging.exception(e))  # full error message
      #a = False

#pieslēgšanās serverim funkcija
def connections(server1,user1,database1,password1):
  conn = None
  try:
    #pieslēgšanās mariadb serverim dati
    '''
    conn = mariadb.connect(
        user="root",
        host="localhost",
        password='',
        port=3306,
        database="project")
    '''
    #SASLĒDZAS AR XML FAILU mariadb
    #filename= "mariaDBConnection.xml"
    #filename=content
    #xmlTree = ET.parse(filename)
    #rootElement = xmlTree.getroot()  #PIEVIENO VISU "KOKU" MAINĪGAJAM
    
    '''
    for element in rootElement.find("connectMariadb/connection"):
      some=(element.attrib['name'])
    if not some:

    print(bool(some))
    '''
    '''
    #IEIET FOR CIKLĀ UN MEKLĒ VAJADZĪGOS ATRIBŪTUS
    for element in rootElement.find("connectMariadb/connection"):
      server1=(element.attrib['host'])
      user1=element.attrib['user']
      database1=element.attrib['database']
      password1=element.attrib['password']
      #print(server1, user1, database1, password1)
    '''
# SAVIENOJUMS AR DB
    conn=mariadb.connect(host=server1,user= user1, database=database1, password=password1)
 
    '''#ja vajag katrā tagā likt visus stringus 
    for element in rootElemnt.findall("connectMariadb"):
      print(element.tag)
      for child in element:
        print(child.tag ,"=","'",child.text,"'")
    ''' 
    
    #pieslēgšanās mssql serverim dati
    '''
    conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
      'Server=localhost;'
      'Database=TestDB;'
      'uid=sa;pwd=AgateZiedina2*')
    logFileWriting('Database connection successful!')
    '''
  except Exception as e:
    #message = sys.exc_info()[2] 
    logFileWriting(logging.exception(e))  #full error message
    #logFileWriting( "Error: %s" % message)  # īsā ziņa logfailā

  return conn
#FUNKCIJA KAS VEIDO TABULU
def create_table(connectionBool):
  try:
    cursor = connectionBool.cursor()
    curDate = time.strftime('%Y%m') #paņem tekošo mēnesi un gadu
    tableName = 'ecr_cheques_items_2333_'+curDate #nemainīgā nosaukuma daļa tabulai
    #tableNameOne = ("%s_%s" % (firstName, curDate)) # pievieno tekošo mēnesi pilnajam tabulas nosaukumam
    #tableName = (tableNameOne,) #lai nosaukums tabulai atbilstu, to vajag ielikt kā tupli
    #tableName = ("ecr_cheques_items_2333_202109",) #tādam jābūt tabulas nosaukumam
    q="SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME ='"+tableName+"';" #? zīme vairāk atbilst lai ieliktu mainīgo querijā
    cursor.execute(q) #palaiž queriju
    #cursor.execute('''SHOW TABLES FROM project''') vecā versija
    #vēl viens variants lai veiktu pārbaudi vai tabula eksistē, bet šis pagaidām nedarbojas
    '''
    cursor.execute(
        """SELECT count(*)
        FROM information_schema.TABLES
        WHERE (TABLE_SCHEMA = 'project') AND (TABLE_NAME = '{}')""".format(tableName))
    '''    
    #jaatceras, ka fetchall() nedrīkst izmantot vairākas reizes, jo tikai pirmā nostrādās, nākamajās jau parādīsies None vērtības
    result =cursor.fetchall() #piešķir mainīgajam visus tabulas nosaukumus, kas tika paņemti no db
    Counter=0 #vajadzīgs, lai nokontrolētu kad drīkstēs un kad nedrīkstēs ifā ieiet. 0=nav tabulu, 1= ir tabula
    counterTwo=0
    garums=len(result)
    #ja counters=0, tad nav iekš db tabulas, bet ja ir 1, tad neies if

    if garums==0:
      #tiek palaists skripts
      cursor.execute('''CREATE TABLE {} (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
          cheque_id INT UNSIGNED NOT NULL, 
          product_id INT UNSIGNED NOT NULL, 
          department_id INT UNSIGNED NOT NULL, 
          unit_id INT UNSIGNED NOT NULL, 
          vat_id INT UNSIGNED NOT NULL, 
          price DECIMAL(10, 3) NOT NULL, 
          count DECIMAL(13, 5) NOT NULL, 
          sum DECIMAL(12, 3) NOT NULL, 
          discount DECIMAL(10, 3) NOT NULL, 
          created_at TIMESTAMP DEFAULT 0 NOT NULL,
          updated_at TIMESTAMP DEFAULT 0 NOT NULL) DEFAULT CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI;'''.format(tableName)) 
      connectionBool.commit()
      cursor.execute('''alter table {} add index if not exists `ecr_cheques_items_cheque_id_index`(`cheque_id`);'''.format(tableName))
      connectionBool.commit()
      cursor.execute('''alter table {} add index if not exists `ecr_cheques_items_product_id_index`(`product_id`);'''.format(tableName))
      connectionBool.commit()
      cursor.execute('''alter table {} add index if not exists `ecr_cheques_items_department_id_index`(`department_id`);'''.format(tableName))
      connectionBool.commit()
      cursor.execute('''alter table {} add index if not exists `ecr_cheques_items_unit_id_index`(`unit_id`);'''.format(tableName))
      connectionBool.commit()
      cursor.execute('''alter table {} add index if not exists `ecr_cheques_items_vat_id_index`(`vat_id`);'''.format(tableName))
      connectionBool.commit()
      connectionBool.close()
      
    
    logFileWriting('TABLE Successful CREATED')
  except Exception as e:
    #message = sys.exc_info()[2]
    logFileWriting(logging.exception(e))  #full error message
    #logFileWriting("<p>Error: %s</p>" % message) #short error message

#funkcija, kas ievietos ierakstus tabulā
def insert_table(connectionBool):
  try:
    cursor = connectionBool.cursor()
    cursor.execute('''INSERT INTO testTable(FirstName,LastName) VALUES
        ('Jasmine','Santina'),
        ('Karlis', 'Kalnins')''')
    connectionBool.commit()
    connectionBool.close()
    logFileWriting('VALUES Successful INSERTED INTO TABLE')
  except Exception as e:
    #message = sys.exc_info()[2]
    logFileWriting(logging.exception(e))  #full error message
    #logFileWriting( "<p>Error: %s</p>" % message)

def main():
 #print("Hello!")
  #endlessLoop() #lai atkļūdotu, endless loops
  #PASKATĀS VAI EKSISTĒ FAILS KEY UN JA NAV, TAD AIZIET UZ FUNKCIJU UN IZVEIDO
  if not os.path.isfile('./key.key'):
    write_key()
  key = load_key() #IELĀDĒ ATSLĒGU NO KEY FAILA
  filename= open("mariaDBConnection.xml", "r")
  #NOLASA 1 SIMBOLU NO FAILA UN JA TAS NAV <, TAD FAILS IR ŠIFRĒTS
  stringToUse=(filename.read(1))
  filename= "mariaDBConnection.xml" #ATKAL NODEFINĒ FAILA NOSAUKUMU, BET ŠOREIZ KĀ XML FAILU
  #JA NAV SIMBOLS, TAD FAILS ŠIFRĒTS
  if not stringToUse=="<":
    decrypt(filename, key) #ATŠIFRĒ FAILU

  xmlTree = ET.parse(filename)
  rootElement = xmlTree.getroot()  #PIEVIENO VISU "KOKU" MAINĪGAJAM
  for element in rootElement.find("connectMariadb/connection"):
      server1=(element.attrib['host'])
      user1=element.attrib['user']
      database1=element.attrib['database']
      password1=element.attrib['password']
      #print(server1, user1, database1, password1)
  print("HELLO: ALL DONE!")
  encrypt(filename, key)
  '''
  with open('mariaDBConnection.xml') as f:
    contents = f.read()
    print(contents)
  '''
  connBool =connections(server1,user1,database1,password1) #savienojms izveidots
  create_table(connBool) #tiek veidota jauna tabula
  #insert_table(connBool) #pievienoti ieraksti tabulā
  #FAILU NOŠIFRĒ, KAD VISAS DARBĪBAS IR PABEIGTAS
  
#mēģināju izveidot: ja savienojums ar db, tad to noslēgt beigās un ierakstīt logfailā
"""
  if bool(connBool):
    connBool.close()
    logFileWriting('Logged out')
  print("BYE!")
"""
if __name__ == "__main__":
    main()
