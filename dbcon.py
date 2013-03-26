#!/usr/bin/python
<<<<<<< HEAD

=======
>>>>>>> 0fb9bf41ec7edb0058e1ef168e151b3f814eb645
#Tal Yoffe
import MySQLdb
import sys
import os
import platform
<<<<<<< HEAD
import logging
=======
>>>>>>> 0fb9bf41ec7edb0058e1ef168e151b3f814eb645



try:
    db = MySQLdb.connect(host="ushslabesxi-db01", user="radmin", passwd="kitkat", db="Contribs")

except Exception as e:
    sys.exit('error connecting to database')
           
cursor = db.cursor()
cursor.execute('Select DISTINCT processName as procName from testSumStats')
result = cursor.fetchall()
print result


    
