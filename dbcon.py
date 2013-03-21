#!/usr/bin/python
#Tal Yoffe
import MySQLdb
import sys
import os
import platform



try:
    db = MySQLdb.connect(host="ushslabesxi-db01", user="radmin", passwd="kitkat", db="Contribs")

except Exception as e:
    sys.exit('error connecting to database')
           
cursor = db.cursor()
cursor.execute('Select DISTINCT processName as procName from testSumStats')
result = cursor.fetchall()
print result


    
