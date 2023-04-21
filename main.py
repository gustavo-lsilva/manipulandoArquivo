import os
import time
import psycopg2
import base64

# Configurações do banco de dados
host = "localhost"
port = "5432"
dbname = "bancoextratos"
user = "gustavo"
password = "senhaforte"

# Conexão com o banco de dados
conn = psycopg2.connect(host=host, port=port, dbname=dbname, user=user, password=password)
cur = conn.cursor()

# Loop infinito para verificar a pasta de extratos a cada 2 minutos
while True:
    # Diretório dos arquivos de extrato
    extrato_dir = "C:/Users/G Force/Documents/Curso/Projetos Pessoais/ajudachat/arquivos/extratos"

    # Percorre todos os arquivos do diretório de extratos
    for file in os.listdir(extrato_dir):
        # Verifica se o arquivo é um arquivo de texto
        if file.endswith(".txt"):
            # Caminho completo do arquivo
            caminho_arquivo = os.path.join(extrato_dir, file)

            # Lê o conteúdo do arquivo e converte em base64
            with open(caminho_arquivo, "rb") as f:
                conteudo = base64.b64encode(f.read()).decode('utf-8')

            # Insere o arquivo no banco de dados
            cur.execute("INSERT INTO principal (nome, arquivo) VALUES (%s, %s)", (file, conteudo))
            conn.commit()

            # Move o arquivo para o diretório de extratos processados
            extrato_processado_dir = "C:/Users/G Force/Documents/Curso/Projetos Pessoais/ajudachat/arquivos/extratosProcessados"
            os.rename(caminho_arquivo, os.path.join(extrato_processado_dir, file))

    # Espera 2 minutos antes de verificar novamente
    time.sleep(120)
