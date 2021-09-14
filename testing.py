#!/usr/bin/env python3
import pypyodbc
import mariadb
import logging
import time
import datetime

def logFileWriting(txt):
  logging.basicConfig(filename="someLogFile.log",
    format='%(asctime)s %(message)s',
    filemode='a')
  logger=logging.getLogger()
  logger.setLevel(logging.DEBUG)
  logger.info(txt)

def endlessLoop():
  a=bool(True)
  startTime = time.strftime('07:00:00', time.localtime())
  endTime = time.strftime('22:00:00', time.localtime())
  while(a):
    timeLocal = time.strftime('%H:%M:%S', time.localtime())
    try:
      if timeLocal>=startTime and timeLocal<=endTime:
        connBool = connections()
        cursor = connBool.cursor()
        cursor.execute('''INSERT INTO testTable(FirstName,LastName) VALUES
          ('Jautrite','bersina')''')
        connBool.commit()
        cursor.execute('''DELETE FROM testTable ''')
        connBool.commit()
        connBool.close()
        logFileWriting('Is working in loop!!!')
      else:
        logFileWriting('Out of time period!!')
        time.sleep(32400) # 9h from 22-07.00
        #logFileWriting(timeLocal)
      #a = False
    except Exception as e:
      logFileWriting(logging.exception(e))  # full error message
      #a = False

def connections():
  conn = None
  try:
    conn = mariadb.connect(
        user="root",
        host="localhost",
        password='',
        port=3306,
        database="project")
    #conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
     # 'Server=localhost;'
      #'Database=TestDB;'
      #'uid=sa;pwd=AgateZiedina2*')
    #logFileWriting('Database connection successful!')
  except Exception as e:
    #message = sys.exc_info()[2]
    logFileWriting(logging.exception(e))  #full error message
    #logFileWriting( "Error: %s" % message)

  return conn

def create_table(connectionBool):
  try:
    cursor = connectionBool.cursor()
   # cursor.execute('''CREATE TABLE testTable(
        #FirstName TEXT NOT NULL,
       # LastName  TEXT NOT NULL );''')
  
    firstName = 'ecr_cheques_items_2333'
    curDate = time.strftime('%Y%m')
    tableName = "%s_%s" % (firstName, curDate)
    cursor.execute('''CREATE TABLE if not exists {} (
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
  print("Hello!")
  #endlessLoop()
  connBool =connections()
  create_table(connBool)
  #insert_table(connBool)
"""
  if bool(connBool):
    connBool.close()
    logFileWriting('Logged out')
  print("BYE!")
"""
if __name__ == "__main__":
    main()
