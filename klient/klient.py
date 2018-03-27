import socket
import sys
#setting all needed variavles
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
BUFFER_SIZE = 1024
message = 'sasaqt'

try:
    print >> sys.stderr, 'connection from', TCP_IP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
        # Receive the data and print it
    while True:
        data = s.recv(BUFFER_SIZE)
        print >> sys.stderr, 'received "%s"' % data
        if data:
            continue
        else:
            print >> sys.stderr, 'no more data from', TCP_IP
            break


finally:
     # Clean up the connection
    s.close()



