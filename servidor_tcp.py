import os
import socket


def iniciar():
    # aqui é o servidor local para receber avisos enviados pela API.
    porta = int(os.getenv("SOCKET_PORT", "5051"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind(("127.0.0.1", porta))
        servidor.listen(5)
        print(f"Servidor TCP aguardando na porta {porta}")
        while True:
            conexao, _ = servidor.accept()
            with conexao:
                mensagem = conexao.recv(256).decode("utf-8", errors="replace")
                print(mensagem)


if __name__ == "__main__":
    iniciar()
