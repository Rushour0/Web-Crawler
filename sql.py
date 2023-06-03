import mysql.connector
import mysql 



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  port=3306,
  password="Einstein10!#"
)

print(mydb)