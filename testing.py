#!/usr/bin/env python3
import pypyodbc
import logging
import sys
def logFileWriting(txt):
  logging.basicConfig(filename="someLogFile.log",
    format='%(asctime)s %(message)s',
    filemode='a')
  logger=logging.getLogger()
  logger.setLevel(logging.DEBUG)
  logger.info(txt)

def endlessLoop():
  a=bool(True)
  while(a):
    connBool = connections()
    cursor = connBool.cursor()
    cursor.execute('''INSERT INTO testTable(FirstName,LastName) VALUES
      ('Jautrite','bersina')''')
    connBool.commit()
    cursor.execute('''DELETE FROM testTable ''')
    connBool.commit()
    connBool.close()
    
def connections():
  conn = None
  try:
    conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
      'Server=localhost;'
      'Database=TestDB;'
      'uid=sa;pwd=AgateZiedina2*')
    logFileWriting('Database connection successful!')
  except Exception as e:
    #message = sys.exc_info()[2]
    logFileWriting(logging.exception(e))  #full error message
    #logFileWriting( "Error: %s" % message)

  return conn

def create_table(connectionBool):
  try:
    cursor = connectionBool.cursor()
    cursor.execute('''CREATE TABLE testTable(
        FirstName TEXT NOT NULL,
        LastName  TEXT NOT NULL );''')
    connectionBool.commit()
   # connectionBool.close()
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
  endlessLoop()
  #connBool =connections()
  #create_table(connBool)
  #insert_table(connBool)
"""
  if bool(connBool):
    connBool.close()
    logFileWriting('Logged out')
  print("BYE!")
"""
if __name__ == "__main__":
    main()
