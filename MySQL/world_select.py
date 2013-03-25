import os
import logging
import MySQLdb


logger = logging.getLogger("DB connection")
logger.setLevel(logging.DEBUG)
#create console handler and set level to error
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
#create file handler and set level to debug
fh = logging.FileHandler("dbcon.log")
fh.setLevel(logging.DEBUG)
#create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)
#add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)


try:
    logger.info("attempting to connection to Database")
    db = MySQLdb.connect(host="192.168.1.4", user="root", passwd="", db="world")
    
except Exception as e:
    logger.error('Error connecting to database!')
    sys.exit('eror connecting to database')



cursor = db.cursor()
cursor.execute('Select DISTINCT language from countrylanguage LIMIT 10')
result = cursor.fetchall()
print result
logger.info("Successfull DB query")
