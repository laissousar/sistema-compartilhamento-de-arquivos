import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog, QInputDialog, QMessageBox, QStyle
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import rpyc
import os

class FileClientGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configurações de Estilo
        self.setStyleSheet("background-color: white;")  # Fundo branco
        
        label_font = QFont("Verdana", 12)  # Fonte 

        # Tela de Conexão - Interface
        self.setWindowTitle('Cliente de Arquivos')
        self.setGeometry(200, 200, 800, 400)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter) 
        self.setLayout(self.layout)

        self.label = QLabel('Seja bem-vindo ao Sistema de Compartilhamento de arquivos!', self)
        self.label.setFont(label_font) 
        self.layout.setAlignment(Qt.AlignCenter)  
        self.layout.addWidget(self.label)

        self.layout.addSpacing(40) 

        self.label = QLabel('Clique aqui para se conectar ao servidor.', self)
        self.label.setFont(label_font)  
        self.layout.setAlignment(Qt.AlignCenter)  
        self.layout.addWidget(self.label)

        self.layout.addSpacing(20) 

        # Botão de conexão- Interface
        self.connect_button = QPushButton(self)
        self.connect_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))  
        self.connect_button.clicked.connect(self.connect_server)
        self.connect_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px") 
        self.layout.addWidget(self.connect_button)

    def connect_server(self):
        # Conecta ao servidor utilizando IP e porta fixos.
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
    
    def show_menu(self):
        """
        Exibe o menu principal após a conexão com o servidor.
        """
        self.clear_layout() # Limpa o layout atual

        self.setLayout(self.layout) # Define o layout

        label_font = QFont("Verdana", 14)  

        self.label = QLabel('Menu Principal', self)
        self.label.setFont(label_font)  
        self.label.setAlignment(Qt.AlignCenter)  
        self.layout.addWidget(self.label)

        # Botão de Upload 
        self.upload_button = QPushButton('Fazer Upload', self)
        self.upload_button.clicked.connect(self.show_upload_screen)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;") 
        self.layout.addWidget(self.upload_button)

        # Botão de Listar Arquivos 
        self.list_button = QPushButton('Listar Arquivos', self)
        self.list_button.clicked.connect(self.list_files)
        self.list_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;") 
        self.layout.addWidget(self.list_button)

        # Botão de Download 
        self.download_button = QPushButton('Fazer Download', self)
        self.download_button.clicked.connect(self.show_download_screen)
        self.download_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;")  
        self.layout.addWidget(self.download_button)

        # Botão de Registrar Interesse
        self.interest_button = QPushButton('Registrar Interesse', self)
        self.interest_button.clicked.connect(self.show_interest_screen)
        self.interest_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;")  
        self.layout.addWidget(self.interest_button)

        # Botão de Cancelar Interesse
        self.cancel_button = QPushButton('Cancelar Interesse', self)
        self.cancel_button.clicked.connect(self.show_cancel_interest_screen)
        self.cancel_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;")  # Botão verde amigável com bordas arredondadas
        self.layout.addWidget(self.cancel_button)

        # Botão de Desconectar
        self.disconnect_button = QPushButton('Sair', self)
        self.disconnect_button.clicked.connect(self.disconnect_server)
        self.disconnect_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;")  # Botão verde amigável com bordas arredondadas
        self.layout.addWidget(self.disconnect_button)

    def show_upload_screen(self):
        """
        Exibe a tela para selecionar e enviar um arquivo para o servidor.
        """
        filename, _ = QFileDialog.getOpenFileName(self, 'Escolher Arquivo')
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
            self.conn.root.upload_file(os.path.basename(filename), data)
            QMessageBox.information(self, 'Sucesso', 'Arquivo enviado com sucesso!')

    def list_files(self):
        """
        Exibe a lista de arquivos disponíveis no servidor.
        """
        files = self.conn.root.list_files()
        if files:
            file_list = '\n'.join(files)
            QMessageBox.information(self, 'Arquivos Disponíveis', file_list)
        else:
            QMessageBox.information(self, 'Arquivos Disponíveis', 'Nenhum arquivo disponível.')

    def show_download_screen(self):
        # Abre uma caixa de diálogo para o usuário digitar o nome do arquivo
        filename, ok = QInputDialog.getText(self, 'Download', 'Digite o nome do arquivo:')
        if ok:
            # Solicita o arquivo ao servidor
            data = self.conn.root.download_file(filename)
            
            if data:
                # Obtém o caminho para a pasta "Downloads" do usuário
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                
                # Cria o caminho completo onde o arquivo será salvo
                file_path = os.path.join(downloads_folder, filename)
                
                # Salva o arquivo na pasta "Downloads"
                with open(file_path, 'wb') as f:
                    f.write(data)
                
                # Informa ao usuário que o download foi bem-sucedido
                QMessageBox.information(self, 'Sucesso', f'Arquivo {filename} baixado com sucesso em {file_path}!')
            else:
                # Informa ao usuário que o arquivo não foi encontrado no servidor
                QMessageBox.warning(self, 'Erro', 'Arquivo não encontrado no servidor.')


    def show_interest_screen(self):
        """
        Exibe a tela para registrar interesse em um arquivo não disponível.
        """
        filename, ok = QInputDialog.getText(self, 'Interesse', 'Digite o nome do arquivo:')
        if ok:
            duration, ok = QInputDialog.getInt(self, 'Duração', 'Digite o tempo (em segundos) de interesse:')
            if ok:
                self.conn.root.register_interest(filename, duration)
                QMessageBox.information(self, 'Sucesso', f'Interesse no arquivo {filename} registrado!')

    def show_cancel_interest_screen(self):
        """
        Exibe a tela para cancelar o interesse registrado em um arquivo.
        """
        filename, ok = QInputDialog.getText(self, 'Cancelar Interesse', 'Digite o nome do arquivo:')
        if ok:
            self.conn.root.cancel_interest(filename)
            QMessageBox.information(self, 'Sucesso', f'Interesse no arquivo {filename} cancelado!')

    def disconnect_server(self):
        """
        Desconecta do servidor e encerra a aplicação.
        """
        self.conn.close()
        QMessageBox.information(self, 'Desconectado', 'Desconectado do servidor.')
        sys.exit()

class FileClientService(rpyc.Service):
    def exposed_notify_event(self, filename):
        """
        Notifica o cliente sobre a disponibilidade de um arquivo.
        """
        QMessageBox.information(None, 'Notificação', f"Arquivo '{filename}' já está disponível.")

if __name__ == "__main__":
    app = QApplication(sys.argv) # Cria a aplicação PyQt5
    client = FileClientGUI() # Cria a interface gráfica do cliente
    client.show()  # Exibe a interface gráfica
    sys.exit(app.exec_()) # Inicia o loop de eventos da aplicação
