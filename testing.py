#!/usr/bin/env python3
import pypyodbc
import logging
def logFileWriting(txt):
  logging.basicConfig(filename="someLogFile.log",
    format='%(asctime)s %(message)s',
    filemode='a')
  logger=logging.getLogger()
  logger.setLevel(logging.DEBUG)
  logger.info(txt)
def connections():
  conn = None
  conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
    'Server=localhost;'
    'Database=TestDB;'
    'uid=sa;pwd=AgateZiedina2*')

  return conn

logingInformation = 'Today is friday!'
logFileWriting(logingInformation)

def create_table(connectionBool):
  cursor = connectionBool.cursor()
  cursor.execute('''CREATE TABLE testTable(
      FirstName TEXT NOT NULL,
      LastName  TEXT NOT NULL );''')
  connectionBool.commit()
 # connectionBool.close()

def insert_table(connectionBool):
  cursor = connectionBool.cursor()
  cursor.execute('''INSERT INTO testTable(FirstName,LastName) VALUES
      ('Santaa','Santina'),
      ('Janis', 'Kalnins')''')
  connectionBool.commit()
  connectionBool.close()

def main():
  print("Hello!")
  connBool =connections()
  #create_table(connBool)
  #insert_table(connBool)

  if connBool:
    connBool.close()
    logFileWriting('Logegd out')
  print("BYE!")

if __name__ == "__main__":
    main()
