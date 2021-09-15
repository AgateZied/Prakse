#!/usr/bin/env python3
import pypyodbc
import mariadb
import logging
import time
import datetime

#logfailu izveido un ieraksta tajā padoto info
def logFileWriting(txt):
  logging.basicConfig(filename="someLogFile.log",
    format='%(asctime)s %(message)s',
    filemode='a')
  logger=logging.getLogger()
  logger.setLevel(logging.DEBUG)
  logger.info(txt)

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
def connections():
  conn = None
  try:
    #pieslēgšanās mariadb serverim dati
    conn = mariadb.connect(
        user="root",
        host="localhost",
        password='',
        port=3306,
        database="project")
    
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

def create_table(connectionBool):
  try:
    cursor = connectionBool.cursor()
  
    firstName = 'ecr_cheques_items_2333' #nemainīgā nosaukuma daļa tabulai
    curDate = time.strftime('%Y%m') #paņem tekošo mēnesi un gadu
    tableNameOne = ("%s_%s" % (firstName, curDate)) # pievieno tekošo mēnesi pilnajam tabulas nosaukumam
    tableName = (tableNameOne,) #lai nosaukums tabulai atbilstu, to vajag ielikt kā tupli
    #tableName = ("ecr_cheques_items_2333_202109",) #tādam jābūt tabulas nosaukumam
    
    q="SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME =?" #? zīme vairāk atbilst lai ieliktu mainīgo querijā
    cursor.execute(q,tableName) #palaiž queriju
    #cursor.execute('''SHOW TABLES FROM project''') 3vecā versija
   
    #vēl viens variants lai veiktu pārbaudi vai tabula eksistē, bet šis pagaidām nedarbojas
    '''
    cursor.execute(
        """SELECT count(*)
        FROM information_schema.TABLES
        WHERE (TABLE_SCHEMA = 'project') AND (TABLE_NAME = '{}')""".format(tableName))
    '''    
    #jaatceras, ka fetchall() nedrīkst izmantot vairākas reizes, jo tikai pirmā nostrādās, nākamajās jau parādīsies None vērtības
    #print("rindA:",cursor.fetchall())
    
    result =cursor.fetchall() #piešķir mainīgajam visus tabulas nosaukumus, kas tika paņemti no db
    Counter=0 #vajadzīgs, lai nokontrolētu kad drīkstēs un kad nedrīkstēs ifā ieiet. 0=nav tabulu, 1= ir tabula
    counterTwo=0
    
    #print("garums: ",len(result))

  #cikls, kurā iziet cauri visām tabulām un skatās vai ir vienāds tabulas nosaukums ar padoto
    while (counterTwo<len(result)):
      
      if result[counterTwo] is None: # ja ir None, tad nav nevienas tabulas
        print("error")
        Counter = 1
        connectionBool.close()
        break;
      elif result[counterTwo]== tableName: #ja sakrīt nosaukums, tad eksistē jau tāda tabula db
        #print("vienads", x) #testēšanas pārbaude
        Counter = 1
        #print("elif iekšā:",counterTwo)
        connectionBool.close() #aizver savienojumu ar db
        break; # iet ārā no cikla, jo ja ir atrasta viena tabula, tad nav vajadzības meklēt tālāk
      #print("NAV vienads", x) #testēšanas pārbaude
      counterTwo +=1
      #print("for otrais:",result[counterTwo])
      
    #VĒL DAŽAS TESTA PĀRBAUDES:
    
    #print("table name:", tableName)
    #print("counter name: ", someCount)
    #ja counters=0, tad nav iekš db tabulas, bet ja ir 1, tad neies if
    #print("te counter one:",Counter)
    if Counter== 0:
      #vēl dažas pārbaudes:
      #print("sakums")
      #print(cursor.fetchone())

      #tiek palaists skripts
      #VAJAG NOŅEMT IEKAVAS UN KOMATU NO NOSAUKUMA, LAI PALAISTU ŠO SKRIPTU
      mainigais=tableName
      mainigais = str(mainigais).replace("'", "")
      mainigais = str(mainigais).replace(",", "")
      mainigais = str(mainigais).replace("(", "")
      mainigais = str(mainigais).replace(")", "")
      print("tagad table nosaukums:",mainigais)
      tableName = mainigais #UZSTĀDĪTS JAUNAIS MAINĪGAIS
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
    #else:
      #vēl dažas pārbaudes:

      #print("beigas")
      #print(cursor.fetchone()) 
      #connectionBool.close()
      #print("EXISTS")
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
  connBool =connections() #savienojms izveidots
  create_table(connBool) #tiek veidota jauna tabula
  #insert_table(connBool) #pievienoti ieraksti tabulā
  
#mēģināju izveidot: ja savienojums ar db, tad to noslēgt beigās un ierakstīt logfailā
"""
  if bool(connBool):
    connBool.close()
    logFileWriting('Logged out')
  print("BYE!")
"""
if __name__ == "__main__":
    main()
