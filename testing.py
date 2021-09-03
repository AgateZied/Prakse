#!/usr/bin/env python3
import pypyodbc

def connections():
  conn = None
  conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
    'Server=localhost;'
    'Database=TestDB;'
    'uid=sa;pwd=AgateZiedina2*')

  return conn
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
      ('Santa','Santina'),
      ('Janis', 'Kalnins')''')
  connectionBool.commit()
  connectionBool.close()
def main():
  print("Hello!")
  connBool =connections()
  create_table(connBool)
  insert_table(connBool)
  print("BYE!")

if __name__ == "__main__":
    main()
