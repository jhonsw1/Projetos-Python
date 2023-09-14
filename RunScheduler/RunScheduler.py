import json
import pytz
import datetime
import winreg
import os
import subprocess
import time
import calendar
import subprocess




path = winreg.HKEY_CURRENT_USER
dadosReg = winreg.OpenKeyEx(path, r"SOFTWARE\\Linx Sistemas\\LinxPOS-e\\")

myvalueServer = winreg.QueryValueEx(dadosReg, "Server")
myvalueDB = winreg.QueryValueEx(dadosReg, "Database")

agendar_backup = ''
agendar_reindex = ''
opcao_dados = ''
horas = '13'
data_modificado = '20230101'
contador_semana = 7

ano_atual = datetime.datetime.now().year
mes_atual = datetime.datetime.now().month
contador_mes = calendar.monthrange(ano_atual, mes_atual)[1]


pasta = 'C:\\temp'
nome_arquivo = f'RunScheduler_log{datetime.date.today().strftime("%Y-%m-%d")}.txt'
caminho_arquivo = os.path.join(pasta, nome_arquivo)

if not os.path.exists(pasta):
    os.makedirs(pasta)
    print(f'Pasta {pasta} criada com sucesso.')

if not os.path.isfile(caminho_arquivo):
    with open(caminho_arquivo, "a") as arquivo:
        arquivo.write("Serviço iniciado!! " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")
    print(f'Arquivo {nome_arquivo} criado com sucesso.')
else:
   with open(caminho_arquivo, "a") as arquivo:
        arquivo.write("Serviço iniciado!! " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")

def atualizar_contador_semana(contador_semana):
    if opcao_dados == '1x Semana':
        while contador_semana >= 1:
            print(f"Contador Semana: {contador_semana}")
            print(24 * 60 * 60)
            time.sleep(24 * 60 * 60)  # Aguarda 24 horas
            contador_semana -= 1
    else:
        contador_semana = 0
      
    return contador_semana        

def atualizar_contador_mes(contador_mes):
    if opcao_dados == '1x Mes':
        while contador_mes >= 1:
            print(f"Contador Semana: {contador_mes}")
            print(24 * 60 * 60)
            time.sleep(24 * 60 * 60)  # Aguarda 24 horas
            contador_mes -= 1
    else:
        contador_mes = 0
      
    return contador_mes     

def Ler_json_dias_faltante():
    with open("registro_dias.json", "r") as arquivo:
        # Carrega os dados do arquivo JSON para a variável
        dados = json.load(arquivo)

        # Extrai os valores dos dados para variáveis individuais
        faltante_semana = dados["qtde_dias_semana_faltante"]
        faltante_mes = dados["qtde_dias_mes_faltante"]
        return faltante_semana, faltante_mes    

def Ler_json(data_modificado):
    print('entrou no json')
    time.sleep(5)
    # Caminho completo do arquivo JSON
    caminho_arquivo = r"C:\RunScheduler\dados_agendador.json"

    # Obter o timestamp da última modificação do arquivo
    timestamp_modificacao = os.path.getmtime(caminho_arquivo)

    # Converter o timestamp em um objeto de data e hora
    data_modificacao = datetime.datetime.fromtimestamp(timestamp_modificacao)

    if (data_modificacao != data_modificado):
        # Abre o arquivo em modo de leitura
        with open(caminho_arquivo, "r") as arquivo:
            # Carrega os dados do arquivo JSON para a variável
            dados = json.load(arquivo)

        # Extrai os valores dos dados para variáveis individuais
        agendar_bk = dados["Agendar Backup"]
        agendar_rd = dados["Agendar Reindex"]
        opcao = dados["Opcao de Dados"]
        horas_gerar = dados["Horas"]
        data_modificado = data_modificacao
        return agendar_bk, agendar_rd, opcao, horas_gerar, data_modificado
    else:
        agendar_bk = agendar_backup
        agendar_rd = agendar_backup
        opcao = opcao_dados
        horas_gerar = horas
        return agendar_bk, agendar_rd, opcao, horas_gerar, data_modificado

def Salvar_agendamento(contador_semana, contador_mes):
    qtde_dias_semana_faltante = contador_semana
    qtde_dias_mes_faltante = contador_mes


    # Cria um dicionário com os dados
    dados = {
        "qtde_dias_semana_faltante": qtde_dias_semana_faltante,
        "qtde_dias_mes_faltante": qtde_dias_mes_faltante
    }

    # Abre o arquivo em modo de escrita
    with open("registro_dias.json", "w") as arquivo:
        # Escreve os dados no arquivo no formato JSON
        json.dump(dados, arquivo)



def controle_dados_str(myvalue):  
    myvalue_str_server = str(myvalue)
    # Encontrar a posição do primeiro caractere de aspas simples
    primeira_aspas_server = myvalue_str_server.find("'")
    # Encontrar a posição do segundo caractere de aspas simples
    segunda_aspas_server = myvalue_str_server.find("'", primeira_aspas_server + 1)
    # Extrair o valor entre as aspas
    dado_str_reg = myvalue_str_server[primeira_aspas_server + 1:segunda_aspas_server]
    return dado_str_reg

Server = controle_dados_str(myvalueServer)
database = controle_dados_str(myvalueDB)

def Execute_backup():
    
    caminho_log = f'C:\\temp\\RunScheduler_log{datetime.date.today().strftime("%Y-%m-%d")}.txt'
    server = Server
    data = database
    username = 'sa'
    password = ''
    base_folder = 'C:\\Base'
    backup_folder = os.path.join(base_folder, 'BKP automatizado')
    backup_file = f'Backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.bak'
    backup_location = os.path.join(backup_folder, backup_file)

    # Verificar se a pasta base existe e criar a estrutura de pastas, se necessário
    arquivo = open(caminho_log, "a")
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        arquivo.writent(f"Pasta base '{base_folder}' criada." "\n")

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        arquivo.write(f"Pasta de backup '{backup_folder}' criada." "\n")

    # Excluir todos os arquivos existentes na pasta de backup
    for file in os.listdir(backup_folder):
        file_path = os.path.join(backup_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            arquivo.write(f"Arquivo existente '{file}' excluído." "\n")

    # Construir o comando de backup
    backup_command = f'sqlcmd -S {server} -U {username} -P "{password}" -Q "BACKUP DATABASE {data} TO DISK=\'{backup_location}\' WITH INIT, FORMAT"'

    
    try:
        # Executar o comando de backup usando o utilitário sqlcmd
        result = subprocess.run(backup_command, shell=True, capture_output=True, text=True)
        arquivo = open(caminho_log, "a")
        if result.returncode == 0:
            arquivo.write("Backup realizado com sucesso!! caminho do arquivo: " + backup_location  + "\n")
        else:
            arquivo.write("Erro ao tentar executar o backup " + result.stderr + "\n")
    except subprocess.CalledProcessError as e:
            print("error")

fuso_horario = pytz.timezone('America/Sao_Paulo')
hora_atual = datetime.datetime.now(fuso_horario)
hora_atual = hora_atual.strftime('%H:%M')

agendar_backup, agendar_reindex, opcao_dados, horas, data_modificado = Ler_json(data_modificado)

while horas != hora_atual or horas == hora_atual: 
    while (opcao_dados == '1x Dia') and horas != hora_atual or horas == hora_atual:
        print('Entrou no while, aguardando ' + opcao_dados, horas, hora_atual)
        if (horas == hora_atual):
            print('entrou no if para o backup')
            Execute_backup()

        fuso_horario = pytz.timezone('America/Sao_Paulo')
        hora_atual = datetime.datetime.now(fuso_horario)
        hora_atual = hora_atual.strftime('%H:%M')  
        agendar_backup, agendar_reindex, opcao_dados, horas, data_modificado = Ler_json(data_modificado)

        if (horas == '00:00'):
            # Executar o outro arquivo Python
            subprocess.call(['python', 'C:\RunScheduler\DownloadArquivos.py'])        


    while (opcao_dados == '1x Semana') and horas != hora_atual or horas == hora_atual :
        print('Entrou no while, aguardando ' + opcao_dados, horas, hora_atual)
        contador_semana, contador_mes = Ler_json_dias_faltante()
        if contador_semana >0:
            Salvar_agendamento(contador_semana, contador_mes)
            contador_semana = atualizar_contador_semana(contador_semana)

        if (horas == hora_atual  and contador_semana ==0):
            print('entrou no if para o backup')
            Execute_backup()
            Salvar_agendamento(7, contador_mes)

        fuso_horario = pytz.timezone('America/Sao_Paulo')
        hora_atual = datetime.datetime.now(fuso_horario)
        hora_atual = hora_atual.strftime('%H:%M')  
        agendar_backup, agendar_reindex, opcao_dados, horas, data_modificado = Ler_json(data_modificado)

        if (horas == '00:00'):
            # Executar o outro arquivo Python
            subprocess.call(['python', 'C:\RunScheduler\DownloadArquivos.py'])        

    while (opcao_dados == '1x Mes') and horas != hora_atual or horas == hora_atual :
        print('Entrou no while, aguardando ' + opcao_dados, horas, hora_atual)
        #print('esperando dar a hora' + opcao_dados)
        contador_semana, contador_mes = Ler_json_dias_faltante()
        if contador_mes >0:
            Salvar_agendamento(contador_semana, contador_mes)
            contador_mes = atualizar_contador_mes(contador_mes)

        if (horas == hora_atual and contador_mes ==0):
            print('entrou no if para o backup')
            Execute_backup()
            ano_atual = datetime.datetime.now().year
            mes_atual = datetime.datetime.now().month
            contador_mes = calendar.monthrange(ano_atual, mes_atual)[1] 
            Salvar_agendamento(contador_semana, contador_mes)         

        fuso_horario = pytz.timezone('America/Sao_Paulo')
        hora_atual = datetime.datetime.now(fuso_horario)
        hora_atual = hora_atual.strftime('%H:%M')  
        agendar_backup, agendar_reindex, opcao_dados, horas, data_modificado = Ler_json(data_modificado)

        if (horas == '00:00'):
            # Executar o outro arquivo Python
            subprocess.call(['python', 'C:\RunScheduler\DownloadArquivos.py'])
    