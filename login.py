from flask import Flask, render_template, request, redirect, url_for
import os
import tkinter as tk
from tkinter import messagebox
from dash import html
import subprocess

app = Flask(__name__)

# Dados de usuário fictícios (substitua por um banco de dados na prática)
usuarios = {'usuario1': 'senha123', 'usuario2': 'senha456'}

@app.route('/')
def home():
    return render_template('login.html')

def exibir_mensagem(mensagem):
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    # Exibe uma janela de mensagem
    messagebox.showinfo('Mensagem', mensagem)

    # Destroi a janela após exibir a mensagem
    root.destroy()

@app.route('/login', methods=['POST'])
def login():
    usuario_digitado = request.form['usuario']
    senha_digitada = request.form['senha']

    # Verifica se o usuário existe e a senha está correta
    if usuario_digitado in usuarios and senha_digitada == '123':
        # Se o login for bem-sucedido, execute o DashBoard.py
        subprocess.Popen(['python', 'DashBoard/DashBoard.py'])
        return redirect(url_for('dashboard'))
    else:
        return 'Credenciais inválidas. Tente novamente.'

        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Substitua 'DashBoard.py' pelo caminho correto do seu arquivo
    caminho_dashboard = os.path.join(os.path.dirname(__file__), 'DashBoard.py')
    
    # Execute o arquivo DashBoard.py
    os.system(f'python {caminho_dashboard}')

    return 'Dashboard em execução.'

if __name__ == '__main__':
    app.run(debug=True)
