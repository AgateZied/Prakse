#!/usr/bin/env python3
import pypyodbc

def conn():
  conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
    'Server=localhost;'
    'Database=TestDB;'
    'uid=sa;pwd=AgateZiedina2*')
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE testTableSec(
    FirstName TEXT NOT NULL,
    LastName  TEXT NOT NULL );''')
  conn.commit()
  conn.close()
  return conn

def main():
  print("Hello!")
  conn()
  print("BYE!")

if __name__ == "__main__":
    main()
