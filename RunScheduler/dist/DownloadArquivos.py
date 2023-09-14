from ftplib import FTP
import os
import zipfile
import psutil
import json
import datetime

def __downloadftp__():

    pasta = 'C:\\temp'
    nome_arquivo = f'RunScheduler_log{datetime.date.today().strftime("%Y-%m-%d")}.txt'
    caminho_arquivo = os.path.join(pasta, nome_arquivo)

    def Ler_json():
        with open("Config.json", "r") as arquivo:
            # Carrega os dados do arquivo JSON para a variável
            dados = json.load(arquivo)

            # Extrai os valores dos dados para variáveis individuais
            hostnameFTP = dados["hostname"]
            username = dados["username"]
            password = dados["password"]
            return hostnameFTP, username, password   

    def fechar_programa(nome_programa):
        for proc in psutil.process_iter():
            if proc.name().lower() == nome_programa.lower():
                proc.kill()

    def extract_files(source_dir, destination_dir):
        # Verifica se o diretório de destino existe e cria se necessário
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Percorre todos os arquivos no diretório de origem
        for file_name in os.listdir(source_dir):
            file_path = os.path.join(source_dir, file_name)

            # Verifica se o arquivo é um arquivo ZIP
            if zipfile.is_zipfile(file_path):
                # Extrai o conteúdo do arquivo ZIP para o diretório de destino
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(destination_dir)

                # Remove o arquivo ZIP após a extração
                os.remove(file_path)
                print(f"Arquivo '{file_name}' extraído e removido.")
                with open(caminho_arquivo, "a") as arquivo:
                    arquivo.write(f"Arquivo '{file_name}' extraído e removido." "\n")                
            else:
                print(f"Arquivo '{file_name}' não é um arquivo ZIP.")
                with open(caminho_arquivo, "a") as arquivo:
                    arquivo.write(f"Arquivo '{file_name}' não é um arquivo ZIP." "\n")         

    # Exemplo de uso
    source_dir = 'c:/RunScheduler/assets'
    destination_dir = 'C:/Linx Sistemas/Linxpos-e'

    def download_ftp_files(hostname, username, password, remote_path, local_path):
        try:
            # Conecta-se ao servidor FTP
            ftp = FTP(hostname)
            ftp.login(username, password)

            # Navega até o diretório remoto
            ftp.cwd(remote_path)

            # Obtém a lista de arquivos no diretório remoto
            files = ftp.nlst()

            # Verifica se há arquivos na lista
            if files:
                # Itera sobre cada arquivo na lista
                for file_name in files:
                    # Define o caminho local completo para salvar o arquivo
                    local_file_path = f"{local_path}/{file_name}"

                    # Abre o arquivo local para escrita binária
                    with open(local_file_path, 'wb') as file:
                        # Faz o download do arquivo do diretório remoto
                        ftp.retrbinary(f'RETR {file_name}', file.write)

                    print(f"Download do arquivo '{file_name}' concluído.")

                    #Fechando o LINXPOS antes de extrair o arquivo para a pasta Linx Sistemas
                    fechar_programa("notepad.exe")
                    extract_files(source_dir, destination_dir)
            else:
                print("Nenhum arquivo encontrado no diretório remoto.")
                with open(caminho_arquivo, "a") as arquivo:
                    arquivo.write("Nenhum arquivo encontrado no diretório remoto." "\n")                      
            # Fecha a conexão FTP
            ftp.quit()
        except Exception as e:
            print("Erro ao conectar ao servidor FTP:", str(e))
            with open(caminho_arquivo, "a") as arquivo:
                arquivo.write(f"Erro ao conectar ao servidor FTP: {str(e)}" "\n")   

    remote_path = ''  # Deixe vazio para o diretório raiz
    local_path = 'c:/RunScheduler/assets'

    hostname, username, password = Ler_json()

    download_ftp_files(hostname, username, password, remote_path, local_path)


__downloadftp__()





