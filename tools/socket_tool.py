import socket


class SocketTool:

    @staticmethod
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