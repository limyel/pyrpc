import json
import socket
import struct

from tools.socket_tool import SocketTool


def handle_conn(conn: socket.socket, addr, handlers):
    print(addr, 'comes')
    # 循环读写
    while True:
        # 请求长度前缀
        length_prefix = conn.recv(4)
        # 连接已关闭
        if not length_prefix:
            print(addr, 'bye')
            conn.close()
            # 退出，处理下一个
            break
        length, = struct.unpack('I', length_prefix)
        body = conn.recv(length)
        request = json.loads(body)
        in_ = request.get('in')
        params = request.get('params')
        print(in_, params)
        # 请求处理器
        handler = handlers.get(in_)
        handler(conn, params)


def loop(sock: socket.socket, handlers):
    while True:
        conn, addr = sock.accept()
        handle_conn(conn, addr, handlers)


def ping(conn, params):
    send_result(conn, 'pong', params)


def send_result(conn: socket.socket, out, result):
    response = json.dumps({'out': out, 'result': result})
    length_prefix = struct.pack('I', len(response))
    conn.sendall(length_prefix)
    conn.sendall(response.encode('utf-8'))


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 8080))
    sock.listen(1)
    handlers = {
        'ping': ping
    }
    loop(sock, handlers)
