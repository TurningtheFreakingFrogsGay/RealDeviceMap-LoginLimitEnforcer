#!/usr/bin/env python

import time
import mysql.connector
from mysql.connector import Error

while True:
  try:
     conn = mysql.connector.connect(host='localhost',
                               database='rdmdb',
                               user='accountwithpermissiontomodifytheDB',
                               password='YourStrongPassword')


     #Query to find token of users over the set limit of logins
     sql_select_Query = "SELECT `token` FROM web_session WHERE `userid` IN (SELECT `userid` from (SELECT `userid` FROM web_session WHERE `userid` != '' GROUP BY `userid` HAVING COUNT(*) > 2)t);"
     cursor = conn.cursor()
     cursor.execute(sql_select_Query)
     alltokens = cursor.fetchall()

     #Query to find the tokens of the latest updated user sessions for all users
     sql_select_Query2 = "SELECT `token` FROM web_session s WHERE ( SELECT COUNT(*) FROM web_session f WHERE f.userid = s.userid AND f.updated >= s.`updated` ) <= 2 AND `userid` != '' ORDER BY `s`.`updated` DESC;"
     cursor = conn.cursor()
     cursor.execute(sql_select_Query2)
     recenttokens = cursor.fetchall()

     #for printing out text for testing query results
     #print (alltokens)
     #print ("-----Line Break-----")
     #print (recenttokens)
     #print ("-----Line Break-----")

     #Retaining newest user sessions only
     tokenstobedeleted = [x for x in alltokens if x not in recenttokens]

     #for testing, printing out results to be deleted
     #print (tokenstobedeleted)


     if tokenstobedeleted == []:
         print(" ")
         print("No Users in Violation of Login Limit, No User Tokens or Sessions Removed from Database")
         cursor.close()

     else:
         sql_Delete_query = """DELETE FROM web_session WHERE `token` = %s;"""
         cursor = conn.cursor()
         cursor.executemany(sql_Delete_query, tokenstobedeleted)
         conn.commit()
         print("\n ", cursor.rowcount, "Users session deleted successfully. ")
         print("Users Found in Violation of Login Limit, Session(s) Deleted successfully, Token(s) Deleted from Database ")
         cursor.close()


  except Error as e :
      print ("Error while connecting to MySQL", e)
      print(" ")
      conn.rollback()
      time.sleep(120)

  finally:
      #closing database connection.
      if(conn.is_connected()):
          conn.close()
          print("MySQL connection is closed")
          time.sleep(120)
