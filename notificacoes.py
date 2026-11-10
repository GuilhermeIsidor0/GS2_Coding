import os
import socket


def avisar_nova_ocorrencia(identificador):
    # aqui envia somente o número da ocorrência, sem dados pessoais.
    try:
        with socket.create_connection(("127.0.0.1", int(os.getenv("SOCKET_PORT", "5051"))), timeout=0.5) as conexao:
            conexao.sendall(f"Nova ocorrencia: {identificador}".encode("utf-8"))
    except OSError:
        # A API continua funcionando mesmo com o servidor_tcp desligado.
        pass
