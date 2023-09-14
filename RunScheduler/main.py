import pyodbc
import winreg
import os
import sys
import subprocess
import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import pytz
import json

# Abre o arquivo em modo de leitura
with open("C:\RunScheduler\dados_agendador.json", "r") as arquivo:
    # Carrega os dados do arquivo JSON para a variável
    dados = json.load(arquivo)

# Extrai os valores dos dados para variáveis individuais
agendar_backup = dados["Agendar Backup"]
agendar_reindex = dados["Agendar Reindex"]
opcao_dados = dados["Opcao de Dados"]
horas = dados["Horas"]


path = winreg.HKEY_CURRENT_USER
dadosReg = winreg.OpenKeyEx(path, r"SOFTWARE\\Linx Sistemas\\LinxPOS-e\\")

myvalueServer = winreg.QueryValueEx(dadosReg, "Server")
myvalueDB = winreg.QueryValueEx(dadosReg, "Database")

if dadosReg:
    winreg.CloseKey(dadosReg)
    winreg.CloseKey(dadosReg)

def Salvar_agendamento():
    agendar_backup = check_var1.get()
    agendar_reindex = check_var2.get()
    opcao_dados = combo.get()
    horas = combo_horas.get()

    # Cria um dicionário com os dados
    dados = {
        "Agendar Backup": agendar_backup,
        "Agendar Reindex": agendar_reindex,
        "Opcao de Dados": opcao_dados,
        "Horas": horas
    }

    # Abre o arquivo em modo de escrita
    with open("C:\RunScheduler\dados_agendador.json", "w") as arquivo:
        # Escreve os dados no arquivo no formato JSON
        json.dump(dados, arquivo)
    
    messagebox.showinfo("Agendamento", "Dados salvos com sucesso!")

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

def adicionar_registro(mensagem):
    grade.insert(END, mensagem + "\n")
    grade.see(END)  # Rolagem automática para exibir o registro mais recente

# Redirecionar a função `print` para adicionar registros à grade
sys.stdout.write = adicionar_registro
sys.stderr.write = adicionar_registro

def execute_backup():
    server = Server
    data = database
    username = 'sa'
    password = ''
    base_folder = 'C:\\Base'
    backup_folder = os.path.join(base_folder, 'BKP automatizado')
    backup_file = f'Backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.bak'
    backup_location = os.path.join(backup_folder, backup_file)

    # Verificar se a pasta base existe e criar a estrutura de pastas, se necessário
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        print(f"Pasta base '{base_folder}' criada.")

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        print(f"Pasta de backup '{backup_folder}' criada.")

    # Excluir todos os arquivos existentes na pasta de backup
    for file in os.listdir(backup_folder):
        file_path = os.path.join(backup_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Arquivo existente '{file}' excluído.")
                     
    # Construir o comando de backup
    backup_command = f'sqlcmd -S {server} -U {username} -P "{password}" -Q "BACKUP DATABASE {data} TO DISK=\'{backup_location}\' WITH INIT, FORMAT"'

    # Executar o comando de backup usando o utilitário sqlcmd
    try:
        subprocess.run(backup_command, shell=True)
        Msg = "Backup gerado no caminho: " + backup_location
        adicionar_registro(Msg)
        messagebox.showinfo("Sucesso!!", "Backup gerado com sucesso!!!")
    except subprocess.run:
        messagebox.showinfo("ATENÇÃO!!", "Falha ao tentar executar o backup, verifique")
def executar_botao():
   
    if Server == 'LOCALHOST' or Server == 'localhost' or Server == 'Localhost' or Server == 'LocalHost' or Server == 'localHost':
        messagebox.showinfo("ATENÇÃO!","Verifique o registro Server, o mesmo não pode estar como " + Server)
    else:

        dados_conexao = (
        "Driver={SQL Server};"
        f"Server={Server};"
        f"Database={database};"
        )
        try:
            conexao = pyodbc.connect(dados_conexao)
            Msg = 'Conexão efetuada com Sucesso!!'
            adicionar_registro(Msg)
        except pyodbc.Error:
            Msg = 'Ocorreu um erro ao tentar se conectar ao banco de dados'  
            adicionar_registro(Msg)
            adicionar_registro(Msg)
            messagebox.showinfo("ATENÇÃO!","Ocoreu um erro ao tentar se conectar ao banco de dados " + database)
     
        def executar_script():  
        
            comando = f"""{conteudo_sql}"""
            try:
                conexao.execute(comando)
                Msg = 'Script ' + arquivo + ' executado com sucesso!!'
                adicionar_registro(Msg)
            except pyodbc.Error:
                Msg = 'Ocorreu um erro ao tentar executar o script ' + arquivo  
                adicionar_registro(Msg)
                messagebox.showinfo("ALERTA GRAVE!", "Falha ao executar o Script " + arquivo +" , verifique o log")
            conexao.commit()
            
        def ler_arquivo_sql(nome_arquivo):
            diretorio = "C:\RunScheduler"
            caminho_pasta_scripts = os.path.join(diretorio, "scripts")
            caminho_arquivo = os.path.join(caminho_pasta_scripts, nome_arquivo)
            print(caminho_arquivo)
            with open(caminho_arquivo, 'r') as arquivo:
                conteudo = arquivo.read()
            return conteudo

        pasta_scripts = os.path.join(os.getcwd(), "scripts")
        arquivos = os.listdir(pasta_scripts)

        for arquivo in arquivos:
            conteudo_sql = ler_arquivo_sql(arquivo)
            executar_script()

janela = Tk()
janela.title("Execute Scripts")
janela.geometry("510x600")

# Definir cores personalizadas
cor_azul = "#0078D7"
cor_cinza_claro = "#EAEAEA"
cor_cinza_escuro = "#333333"
cor_branco = "#FFFFFF"

# Cria uma instância do estilo temático
style = ttk.Style()
style.theme_use("clam")

# Estilo dos widgets
style.configure("TLabel",
                foreground=cor_branco,  # Cor do texto
                background=cor_cinza_escuro,  # Cor de fundo
                font=("Arial", 12, "bold")  # Fonte
                )

style.configure("TButton",
                relief="raised",  # Define uma borda em relevo
                borderwidth=1,  # Largura da borda
                foreground=cor_branco,  # Cor do texto
                background=cor_azul,  # Cor de fundo
                font=("Arial", 12),  # Fonte
                padding=5  # Espaçamento interno
                )


janela.title("Configurador HunScheduler")
janela.geometry("560x600")
janela.resizable(width=False, height=False)  


# Informação do Servidor
frame_servidor = Frame(janela, bg=cor_cinza_claro)
frame_servidor.pack(fill=X, padx=20, pady=10)

texto_servidor = Label(frame_servidor, text="Servidor:", font=("Arial", 12, "bold"))
texto_servidor.pack(side=LEFT, padx=(0, 10))

nome_servidor = Label(frame_servidor, text=Server, font=("Arial", 12))
nome_servidor.pack(side=LEFT)

# Informações do banco de dados
frame_db = Frame(janela, bg=cor_cinza_claro)
frame_db.pack(fill=X, padx=20, pady=10)

texto_db = Label(frame_db, text="Banco de dados:", font=("Arial", 12, "bold"))
texto_db.pack(side=LEFT, padx=(0, 10))

nome_db = Label(frame_db, text=database, font=("Arial", 12))
nome_db.pack(side=LEFT)

# Título Executar Scripts
titulo_executar = Label(janela, text="Execute Scripts", font=("Arial", 14, "bold"))
titulo_executar.pack(pady=10)

# Botões Executar Scripts
frame_botoes = Frame(janela)
frame_botoes.pack(pady=10)

botao_script = ttk.Button(frame_botoes, text="Executar Scripts", command=executar_botao)
botao_script.grid(row=0, column=0, padx=10)

botao_bkp = ttk.Button(frame_botoes, text="Executar Backup", command=execute_backup)
botao_bkp.grid(row=0, column=1, padx=10)

# Título Configure Agendador
titulo_agendador = Label(janela, text="Configure agendador", font=("Arial", 14, "bold"))
titulo_agendador.pack(pady=10)

check_var1 = IntVar()
check_var2 = IntVar()

# Cria os checkboxes
check1 = Checkbutton(janela, text="Agendar Backup", variable=check_var1, font=("Arial", 12))
check1.pack()

if agendar_backup == 1:
    check1.select()
else:
    check1.deselect()


check2 = Checkbutton(janela, text="Agendar Reindex", variable=check_var2, font=("Arial", 12))
check2.pack()

if agendar_reindex == 1:
    check2.select()
else:
    check2.deselect()

# Opção de Dados e Horas
frame_opcao_horas = Frame(janela, bg=cor_cinza_claro)
frame_opcao_horas.pack(fill=X, padx=20, pady=10)

combo_label = Label(frame_opcao_horas, text="Dia de backup:", font=("Arial", 12, "bold"))
combo_label.grid(row=0, column=0, padx=(0, 10))

opcao_dados = '1x dia'

combo = ttk.Combobox(frame_opcao_horas, values=["1x Dia", "1x Semana", "1x Mes"], width=10)
combo.grid(row=0, column=1, padx=(0, 10))
combo.set(opcao_dados)


combo_horas_label = Label(frame_opcao_horas, text="Horas:", font=("Arial", 12, "bold"))
combo_horas_label.grid(row=0, column=2, padx=(0, 10))

combo_horas = ttk.Combobox(frame_opcao_horas, values=[str(h).zfill(2) + ":00" for h in range(24)], width=5)
combo_horas.grid(row=0, column=3, padx=(0, 10))
combo_horas.set(horas)

botao_salvar_agendamento = ttk.Button(frame_opcao_horas, text="Salvar agendamento", command=Salvar_agendamento)
botao_salvar_agendamento.grid(row=0, column=4, padx=(0, 10))


# Grade para exibir os registros
frame_grade = Frame(janela)
frame_grade.pack(fill=BOTH, expand=True, padx=20, pady=10)

grade = Text(frame_grade, font=("Arial", 12), bg=cor_cinza_claro)
grade.pack(fill=BOTH, expand=True)

janela.mainloop()
