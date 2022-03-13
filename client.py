import json
import socket
import struct
import time


def rpc(sock: socket.socket, in_, params):
    request = json.dumps({'in': in_, 'params': params})
    length_prefix = struct.pack('I', len(request))
    sock.sendall(length_prefix)
    sock.sendall(request.encode('utf-8'))
    length_prefix = sock.recv(4)
    legth, = struct.unpack('I', length_prefix)
    body = sock.recv(legth)
    response = json.loads(body)
    return response.get('out'), response.get('result')


def receive(sock: socket.socket, n):
    rs = []
    while n > 0:
        r = sock.recv(n)
        if not r:
            return rs
        r = r.decode('utf-8')
        rs.append(r)
        n -= len(r)
    return ''.join(rs)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))
    for i in range(10):
        out, result = rpc(s, 'ping', f'ireader {i}')
        print(out, result)
        time.sleep(1)
    s.close()
