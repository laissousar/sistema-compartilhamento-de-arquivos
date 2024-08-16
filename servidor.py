import rpyc
from rpyc.utils.server import ThreadedServer
import os
from time import time

class FileServerService(rpyc.Service):
    """
    Serviço de servidor de arquivos utilizando RPyC para comunicação remota.
    Permite upload, download, listagem de arquivos e registro de interesse em arquivos não disponíveis.
    """
    
    def __init__(self):
        """
        Inicializa o servidor com estruturas para armazenar arquivos e interesses de clientes.
        """
        self.files = {}  # Dicionário para armazenar nome e caminho dos arquivos disponíveis
        self.interests = []  # Lista para armazenar interesses dos clientes em arquivos não disponíveis

    def on_connect(self, conn):
        """
        Método chamado quando um cliente se conecta ao servidor."""
        
        print(f"Cliente conectado: {conn}")
        self.conn = conn # Armazena a conexão do cliente

    def on_disconnect(self, conn):
        """
        Método chamado quando um cliente se desconecta do servidor.
        """
        print(f"Cliente desconectado: {conn}")

    def exposed_upload_file(self, filename, data):
        """
        Exposto para permitir que um cliente faça upload de um arquivo para o servidor.

        Parâmetros:
        filename (str): Nome do arquivo a ser armazenado.
        data (bytes): Dados binários do arquivo a ser armazenado.
        """
        with open(filename, 'wb') as f:
            f.write(data)
        self.files[filename] = os.path.abspath(filename)
        print(f"Arquivo {filename} recebido e armazenado.")

        # Notificar clientes interessados se o arquivo estiver na lista de interesses
        self.check_and_notify_interests(filename)

    def exposed_list_files(self):
        """
        Exposto para permitir que um cliente liste os arquivos disponíveis no servidor.

        Retorna:
        list: Lista com os nomes dos arquivos disponíveis.
        """
        return list(self.files.keys())


    def exposed_download_file(self, filename):
        """
        Exposto para permitir que um cliente faça download de um arquivo disponível no servidor.

        Parâmetros:
        filename (str): Nome do arquivo a ser baixado.

        Retorna:
        bytes: Dados binários do arquivo, ou None se o arquivo não for encontrado.
        """
        if filename in self.files:
            print(f"Enviando arquivo {filename} para o cliente.")
            with open(self.files[filename], 'rb') as f:
                return f.read()    
        else:
            print(f"Arquivo {filename} não encontrado.")
            return None

    def exposed_register_interest(self, filename, duration):
        """
        Exposto para permitir que um cliente registre interesse em um arquivo não disponível.

        Parâmetros:
        filename (str)
        duration (float): Duração em segundos que o interesse é válido.
        """
        interest = {
            "filename": filename,
            "conn": self.conn,  # Armazena a conexão do cliente
            "valid_until": time() + duration
        }
        self.interests.append(interest)
        print(f"Interesse registrado para o arquivo {filename} pelo cliente {self.conn}")

    def exposed_cancel_interest(self, filename):
        """Cancelar registro de interesse."""

        if not hasattr(self, 'conn'):
            raise Exception("Conexão não estabelecida")
        
        self.interests = [i for i in self.interests if not (i['filename'] == filename and i['conn'] == self.conn)]
        print(f"Interesse cancelado para o arquivo {filename} pelo cliente {self.conn}")


    def check_and_notify_interests(self, filename):
        """
        Verifica a lista de interesses e notifica os clientes se o arquivo estiver disponível."""
        to_remove = []
        for interest in self.interests:
            if interest["filename"] == filename and interest["valid_until"] > time():
                try:
                    conn = interest["conn"]
                    async_notify = rpyc.async_(conn.root.notify_event)  # Torna a chamada assíncrona
                    async_notify(filename).add_callback(self.notify_callback)
                    print(f"Cliente notificado sobre a disponibilidade do arquivo {filename}.")
                except Exception as e:
                    print(f"Erro ao notificar o cliente: {e}")
                to_remove.append(interest)
        # Remover interesses satisfeitos
        self.interests = [i for i in self.interests if i not in to_remove]

    def notify_callback(self, result):
        """Callback para tratar resultados de notificações assíncronas.
        
        Parâmetros:
        result: Resultado da operação assíncrona de notificação."""
        if result.error:
            print(f"Erro na notificação: {result.error}")
        else:
            print("Notificação enviada com sucesso.") 

if __name__ == "__main__":
    server = ThreadedServer(FileServerService, port=12345)
    print("Servidor iniciado na porta 12345")
    server.start()
