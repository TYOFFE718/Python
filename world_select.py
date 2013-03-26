import os
import logging
import logging.handlers
import MySQLdb
import sys


#Create logger
logger = logging.getLogger("DB connection")
logger.setLevel(logging.DEBUG)


#create file handler and set level to debug
hand = logging.handlers.RotatingFileHandler("dbcon.log", 'a', 100,4)
logger.setLevel(logging.DEBUG)

#create formatter
form = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
hand.setFormatter(form)
logger.addHandler(hand)


try:
    logger.info("attempting to connection to Database")
    db = MySQLdb.connect(host="localhost", user="root", passwd="brooklyn77", db="world")
    
except Exception as e:
    logger.error('Error connecting to database!')
    sys.exit('eror connecting to database')



cursor = db.cursor()
cursor.execute('Select DISTINCT language from CountryLanguage LIMIT 10')
result = cursor.fetchall()
print result
logger.info("Successfull DB query")
