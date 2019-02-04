#!/usr/bin/env python

#User config settings, change here
number_of_concurrent_allowed_user_sessions_per_account = 1
time_in_seconds_between_check_cycles = 30

#DB config settings
host = 'localhost'
database = 'rdmdb'
user = 'AccountWithPermissiontoModifytheDB'
password = 'YourStrongPassword'
port = '3306'

#Do not edit below this line unless you know what you are doing.

import datetime
import time
import mysql.connector
from mysql.connector import Error

while True:
  try:
     conn = mysql.connector.connect(host=host,
                               database=database,
                               user=user,
                               password=password,
                               port=port)


     #Query to find token of users over the set limit of logins
     sql_select_Query = "SELECT `token` FROM web_session WHERE `userid` IN (SELECT `userid` FROM (SELECT `userid` FROM web_session WHERE `userid` != '' GROUP BY `userid` HAVING COUNT(*) > %s)t);"
     cursor = conn.cursor()
     cursor.execute(sql_select_Query, (number_of_concurrent_allowed_user_sessions_per_account , ))
     alltokens = cursor.fetchall()

     #Query to find the tokens of the latest updated user sessions for all users
     sql_select_Query2 = "SELECT `token` FROM web_session s WHERE ( SELECT COUNT(*) FROM web_session f WHERE f.userid = s.userid AND f.updated >= s.`updated` ) <= %s AND `userid` != '' ORDER BY `s`.`updated` DESC;"
     cursor = conn.cursor()
     cursor.execute(sql_select_Query2, (number_of_concurrent_allowed_user_sessions_per_account , ))
     recenttokens = cursor.fetchall()

     #for printing out text for testing query results
     #print (alltokens)
     #print ("-----Line Break-----")
     #print (recenttokens)
     #print ("-----Line Break-----")

     #Retaining newest user session(s) only
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
         print(" ")
         print(cursor.rowcount, "Users Session(s) Deleted Successfully.")
         print("Users Found in Violation of Login Limit, Session(s) Deleted successfully, Token(s) Deleted from Database ")
         cursor.close()


  except Error as e :
      print ("Error while connecting to MySQL", e)
      print(" ")
      print("Script Ran with Error at: ")
      now = datetime.datetime.now()
      print (now.strftime("%H:%M:%S, %Y-%m-%d"))
      conn.rollback()
      time.sleep(time_in_seconds_between_check_cycles)

  finally:
      #closing database connection.
      if(conn.is_connected()):
          conn.close()
          print("MySQL connection is closed")
          print("Script Succesfully Ran at: ")
          now = datetime.datetime.now()
          print (now.strftime("%H:%M:%S, %Y-%m-%d"))
          time.sleep(time_in_seconds_between_check_cycles)
