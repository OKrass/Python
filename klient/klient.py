import socket
import sys
# Put your IP and port here
TCP_IP = '127.0.0.1'
TCP_PORT = 3001
BUFFER_SIZE = 1024
message = 'all data accepted\t'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print >> sys.stderr, 'connection from', TCP_IP
        # Receive the data and print it
    while True:
        data = s.recv(BUFFER_SIZE)
        print >> sys.stderr, 'received "%s"' % data
        if data:
            continue
        else:
            s.send(message)
            print >> sys.stderr, 'no more data from', TCP_IP
            break


finally:
     # Clean up the connection
    s.close()



