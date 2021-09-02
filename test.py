#!/usr/bin/env python3
import pypyodbc

conn = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
  'Server=localhost;'
  'Database=TestDB;'
  'uid=sa;pwd=AgateZiedina2*') 



def main():
  print("Hello World!")

if __name__ == "__main__":
    main()
