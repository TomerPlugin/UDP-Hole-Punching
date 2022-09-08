from http import server
import socket
import sys
import threading

server = ('113.30.191.147', 55555)

# connect to server
print('connecting to server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto('Tomer PC'.encode(), server)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, src_sport, dst_port = data.split(' ')
src_sport = int(src_sport)
dst_port = int(dst_port)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(src_sport))
print('  dest port:   {}\n'.format(dst_port))

# punch hole
# equiv: echo 'punch hole' | nc -u -p src_port x.x.x.x dst_port
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', src_sport))
sock.sendto(b'0', (ip, dst_port))

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l src_port
def listen():
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(('0.0.0.0', src_sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p dst_port x.x.x.x src_sport
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dst_port))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, src_sport))
