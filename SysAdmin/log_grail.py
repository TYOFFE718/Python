#!/usr/bin/python
import smtplib
import string
import time


#Email info
MAILHOST = 'mailhost.us.icap.com'
SUBJECT = "Test email from Python"
TO = "Tal.Yoffe@us.icap.com"
FROM = "TestSFTP@PYTHON.com"
text =  "MarketLink Client ACME:63099 Disconnect" + " " +  "@ " + " " + time.strftime('%X')
BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        text
        ), "\r\n")
server = smtplib.SMTP(MAILHOST)
server = smtplib.SMTP(MAILHOST)
server.sendmail(FROM, [TO], BODY)




def tail(log_file):
    log_file.seek(0, 2)

    while True:
        line = log_file.readline()

        if not line:
            time.sleep(1.0)
            continue

        yield line




def process_match(matchtext):
     while True:
         line = (yield)
         if matchtext in line:
             server.sendmail(FROM, [TO], BODY, matchtext)


list_of_matches = ['Disconnected', ' Connected']
matches = [process_match(string_match) for string_match in list_of_matches]


for m in matches:
         m.next()


while True:
         grep_log = tail(open('C:\\Documents and Settings\\tyoffe\\Desktop\\new.txt') )
         for line in grep_log:
                              for m in matches:
                                  m.send(line)
