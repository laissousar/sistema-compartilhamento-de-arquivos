
# Sistema de Compartilhamento de Arquivo

Este projeto implementa um sistema de compartilhamento de arquivos utilizando RPyC para comunicação entre cliente e servidor. O cliente pode realizar operações de upload, download, listar arquivos disponíveis, e registrar interesse em arquivos não disponíveis. O servidor gerencia as operações de arquivos e notifica os clientes interessados quando um arquivo se torna disponível.


## Funcionalidades

### Cliente
- Conectar ao servidor: Conecta-se ao servidor utilizando um IP e porta fixos.
- Fazer Upload: Permite o upload de arquivos para o servidor.
- Listar Arquivos: Exibe a lista de arquivos disponíveis no servidor.
- Fazer Download: Permite o download de arquivos disponíveis do servidor.
- Registrar Interesse: Registra o interesse em um arquivo não disponível, com a possibilidade de receber uma notificação quando o arquivo estiver disponível.
- Cancelar Interesse: Cancela o interesse em um arquivo previamente registrado.
- Desconectar do servidor: Encerra a conexão com o servidor.

### Servidor

- Receber Upload: Recebe e armazena arquivos enviados pelos clientes.
- Listar Arquivos: Mantém uma lista de arquivos disponíveis para download.
- Enviar Arquivos: Envia arquivos disponíveis para os clientes mediante solicitação.
- Registrar Interesse: Registra interesse de clientes em arquivos não disponíveis.
- Notificar Clientes: Notifica clientes interessados quando um arquivo de interesse se torna disponível.



## Stack utilizada

**Linguagem de Programação:** Python

**Bibliotecas e Ferramentas:** PyQt5, RPyC

**Protocolo de Comunicação:** RPC (Remote Procedure Call)

## Demonstração

Insira um gif ou um link de alguma demonstração


## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/laissousar/sistema-compartilhamento-de-arquivos.git
```

Entre no diretório do projeto

```bash
  cd local-my-project
```

Instale as dependências

```bash
  pip install rpyc
  pip install pyqt5
```

Inicie o servidor

```bash
  python servidor.py

```
Inicie o cliente

```bash
  python cliente.py
  
```

## Autores

- [@laissousar](https://github.com/laissousar)

- [@bi4lim4](https://github.com/bi4lim4/)

