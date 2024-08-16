import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QInputDialog, QMessageBox, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import rpyc
import os

class FileClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Tela de Conexão
        self.setWindowTitle('Cliente de Arquivos')
        self.setGeometry(200, 200, 800, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Seja bem-vindo ao Sistema de Compartilhamento de arquivos!', self)
        self.layout.addWidget(self.label)

        self.label = QLabel('Clique em Iniciar para se conectar ao servidor.', self)
        self.layout.addWidget(self.label)

        # Botão de conexão
        self.connect_button = QPushButton(self)
        self.connect_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))  # Seta para a direita
        self.connect_button.clicked.connect(self.connect_server)
        self.layout.addWidget(self.connect_button)

    def connect_server(self):
        # Definindo IP e porta fixos para conexão com o servidor
        ip = 'localhost'
        port = 12345
        try:
            self.conn = rpyc.connect(ip, port, service=FileClientService)
            QMessageBox.information(self, 'Sucesso', 'Conectado ao servidor com sucesso!')
            self.show_menu()
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao conectar ao servidor: {e}')

    def clear_layout(self):
        """Remove todos os widgets e layouts existentes do layout atual."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    #Fu
    def show_menu(self):
        self.clear_layout()

        self.setLayout(self.layout)

        self.label = QLabel('Menu Principal', self)
        self.layout.addWidget(self.label)

        self.upload_button = QPushButton('Fazer Upload', self)
        self.upload_button.clicked.connect(self.show_upload_screen)
        self.layout.addWidget(self.upload_button)

        self.list_button = QPushButton('Listar Arquivos', self)
        self.list_button.clicked.connect(self.list_files)
        self.layout.addWidget(self.list_button)

        self.download_button = QPushButton('Fazer Download', self)
        self.download_button.clicked.connect(self.show_download_screen)
        self.layout.addWidget(self.download_button)

        self.interest_button = QPushButton('Registrar Interesse', self)
        self.interest_button.clicked.connect(self.show_interest_screen)
        self.layout.addWidget(self.interest_button)

        self.cancel_button = QPushButton('Cancelar Interesse', self)
        self.cancel_button.clicked.connect(self.show_cancel_interest_screen)
        self.layout.addWidget(self.cancel_button)

        self.disconnect_button = QPushButton('Sair', self)
        self.disconnect_button.clicked.connect(self.disconnect_server)
        self.layout.addWidget(self.disconnect_button)

    def show_upload_screen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Escolher Arquivo')
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
            self.conn.root.upload_file(os.path.basename(filename), data)
            QMessageBox.information(self, 'Sucesso', 'Arquivo enviado com sucesso!')

    def list_files(self):
        files = self.conn.root.list_files()
        if files:
            file_list = '\n'.join(files)
            QMessageBox.information(self, 'Arquivos Disponíveis', file_list)
        else:
            QMessageBox.information(self, 'Arquivos Disponíveis', 'Nenhum arquivo disponível.')

    def show_download_screen(self):
        filename, ok = QInputDialog.getText(self, 'Download', 'Digite o nome do arquivo:')
        if ok:
            data = self.conn.root.download_file(filename)
            if data:
                with open(filename, 'wb') as f:
                    f.write(data)
                QMessageBox.information(self, 'Sucesso', f'Arquivo {filename} baixado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Arquivo não encontrado no servidor.')

    def show_interest_screen(self):
        filename, ok = QInputDialog.getText(self, 'Interesse', 'Digite o nome do arquivo:')
        if ok:
            duration, ok = QInputDialog.getInt(self, 'Duração', 'Digite o tempo (em segundos) de interesse:')
            if ok:
                self.conn.root.register_interest(filename, duration)
                QMessageBox.information(self, 'Sucesso', f'Interesse no arquivo {filename} registrado!')

    def show_cancel_interest_screen(self):
        filename, ok = QInputDialog.getText(self, 'Cancelar Interesse', 'Digite o nome do arquivo:')
        if ok:
            self.conn.root.cancel_interest(filename)
            QMessageBox.information(self, 'Sucesso', f'Interesse no arquivo {filename} cancelado!')

    def disconnect_server(self):
        self.conn.close()
        QMessageBox.information(self, 'Desconectado', 'Desconectado do servidor.')
        sys.exit()

class FileClientService(rpyc.Service):
    def exposed_notify_event(self, filename):
        QMessageBox.information(None, 'Notificação', f"Arquivo '{filename}' já está disponível.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = FileClientGUI()
    client.show()
    sys.exit(app.exec_())
