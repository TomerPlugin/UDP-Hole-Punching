from http import server
import socket
import sys
import threading

server = ('113.30.191.147', 55555)

# connect to server
print('connecting to server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('0.0.0.0', 50001))

user_id = input('Your User ID: ')

sock.sendto('user_id'.encode(), server)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, port = data.split(' ')
port = int(port)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  port: {}'.format(port))

print('punching hole')

sock.sendto('PC!'.encode(), (ip, port))
print('ready to exchange messages\n')

# listen for
def listen():

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, port))
