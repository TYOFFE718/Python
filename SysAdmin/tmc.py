import socket
import sys
# create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to server
host = sys.argv[1] # server address
port = int(sys.argv[2]) # server port
s.connect((host, port))
s.send(sys.argv[3]) # send test string
# read echo
i = 0
while(1):
    data = s.recv(1000000) # read up to 1000000 bytes
    i += 1
    if (i < 5): # look only at the first part of the messag
        print data
    if not data: # if end of data, leave loop
        break
    print 'received', len(data), 'bytes'
# close the connection
s.close


s.close()
