import pyautogui
import time
from tkinter import *
from tkinter import ttk
import pywhatkit as kt 
import keyboard
from datetime import datetime

iniciar_macro = ''
t_fisgar = ''
t_vara = ''
t_inventario = ''
t_camera = ''
t_long = 0

with open("tecla_config.txt", "r") as arquivo:
    teclas = arquivo.readlines()
    cont = 1
    for lista_teclas in teclas:
        if cont ==5:
            t_long = lista_teclas
        cont += 1            

def BuscaForcaVara(forca):
    global t_long
    t_long = float(forca)
    with open("tecla_config.txt", "w") as arquivo:
        arquivo.write(t_fisgar+'\n'+t_vara+'\n'+ t_inventario+'\n'+t_camera+'\n'+str(t_long))    
       


def SalvarTeclas():
    global t_fisgar
    global t_vara
    global t_inventario
    global t_camera
    global iniciar_macro    
    global t_long
    t_fisgar = cb_tecla_fisgar.get()
    t_vara = cb_tecla_vara.get()
    t_inventario = cb_tecla_inv.get()
    t_camera = cb_tecla_cam.get()
    with open("tecla_config.txt", "w") as arquivo:
        arquivo.write(t_fisgar+'\n'+t_vara+'\n'+ t_inventario+'\n'+t_camera+'\n'+str(t_long))    

def Macro():

    if (t_fisgar == '') or (tecla_vara == '') or (tecla_inv =='') or (cb_tecla_cam == ''):
        text_msg["text"] += ('\n''ATENÇÃO!!! FAVOR VERIFICAR TECLAS EM BRANCO')
    else: 
        text_msg["text"] += ('\n''Iniciando Macro') 
        iniciar_macro = True  
        position = None
        contador_pescando = 0 
        img_pescar = 'img_fisgando.png'
        contador_sem_pesca_whats = 0

        pyautogui.keyDown('alt')
        pyautogui.press(['tab'])
        pyautogui.keyUp('alt')

        time.sleep(1)
        pyautogui.keyDown(t_fisgar)
        time.sleep(t_long)
        pyautogui.keyUp(t_fisgar)
        ativo  = 'sem_peixe' 

  
        while iniciar_macro == True and t_fisgar != '':
            pyautogui.keyDown(t_camera)

            while (position == None) and (contador_pescando <=35):
                img = 'img_cap.png'
                position = pyautogui.locateCenterOnScreen(img, confidence=0.8)
                contador_pescando += 1
                print('tentando dar a fisgada', 'posição', contador_pescando)
            if (position != None):
                    print('encontrado a imagem de fisgada')
                    for cont in range (0, 12):
                        print('entrou no click for')
                        pyautogui.press(['n'])             
                    ativo = 'fisgou'
                    position = None
                    contador_pescando = 0
                    
            if ativo == 'fisgou':

                for contador_pescando in range (0, 11):
                        print('posição do for', contador_pescando)
                        position_primeiro = pyautogui.locateCenterOnScreen(img_pescar, confidence=0.8)
                        print ('tentando pescar na primeira imagem')
                        if position_primeiro != None:
                            pyautogui.keyDown(t_fisgar)
                            time.sleep(2)
                            pyautogui.keyUp(t_fisgar)
                            print('pego o peixe na primeira imagem') 
                        if position_primeiro == None:
                            segundo_img = 'img_fisgando2.png'
                            print('tentando pescar na segunda imagem')
                            position_segundo = pyautogui.locateCenterOnScreen(segundo_img, confidence=0.8)
                            if position_segundo != None: 
                                print('pego o peixe na segunda imagem')
                                pyautogui.keyDown(t_fisgar)
                                time.sleep(2)
                                pyautogui.keyUp(t_fisgar)       
                        time.sleep(2)   
                        if contador_pescando >= 10: 
                            ativo = 'pescou'
                            contador_pescando = 110

            if contador_pescando >= 35:
                    pyautogui.keyUp(t_camera)
                    pyautogui.press([t_inventario])
                    print('clicou no primeiro i')
                    time.sleep(2)
                    img_reparar = 'reparar_arma.png'
                    position_reparar = pyautogui.locateCenterOnScreen(img_reparar, confidence= 0.5)
                    contador_sem_pesca_whats +=1
                    print('CONTADOR DO WHATS', contador_sem_pesca_whats)
                    if contador_sem_pesca_whats >=1:
                        contatos = 'DZrbv4Bw4Vt0paTKvxzcTx' 
                        kt.sendwhatmsg_to_group(contatos,str(contador_sem_pesca_whats) + " tentativa sem conseguir pescar, favor verificar o macro",datetime.now().hour,datetime.now().minute + 1)
                        time.sleep(10)
                        keyboard.press_and_release('ctrl + w')     
                        time.sleep(2)                    
                    if position_reparar != None:
                        time.sleep(0.3)
                        pyautogui.mouseDown(position_reparar)
                        time.sleep(1)
                        pyautogui.mouseUp()
                        pyautogui.keyDown('r')
                        pyautogui.mouseDown()
                        time.sleep(1)
                        pyautogui.mouseUp()
                        pyautogui.keyUp('r')
                        time.sleep(1)
                        
                        pyautogui.press(['e'])  
                    pyautogui.press(t_inventario)
                    print('clicou no segundo i')
                    time.sleep(1)
                    pyautogui.press(t_vara)
                    pyautogui.keyDown('a')
                    time.sleep(0.1)
                    pyautogui.keyUp('a')
                    pyautogui.keyDown('d')
                    time.sleep(0.2)
                    pyautogui.keyUp('d')
                    time.sleep(1)        
                    pyautogui.keyDown(t_fisgar)
                    time.sleep(round(t_long,2))
                    pyautogui.keyUp(t_fisgar)
                    contador_pescando = 0
                   
janela = Tk()
janela.title('Macro new world')
janela.geometry('350x580')
tecla_fisgar = "Tab"
tecla_vara = "Tab"
tecla_inv = "Tab"
tecla_cam = "Tab"
long_linha = 1.0
cont_t = 1

with open("tecla_config.txt", "r") as arquivo:
    teclas = arquivo.readlines()

    for lista_teclas in teclas:
        if cont_t == 1:
            tecla_fisgar = lista_teclas
            print('posiçao 1', tecla_fisgar)
        if cont_t == 2:
            tecla_vara = lista_teclas
            print('posição 2', tecla_vara)
        if cont_t == 3:
            tecla_inv = lista_teclas
            print('posição 3', tecla_inv)
        if cont_t == 4:
            tecla_cam = lista_teclas
            print('[posição 4', tecla_cam)
        if cont_t == 5:
            long_linha = float(lista_teclas)
            print('[posição 4', long_linha)  
            print(type(long_linha))
                    
        cont_t += 1            
       
ListTeclas = ["Tab","b","n","j","i","6","7","8","9","0"]

quadro_teclas =Frame(janela, borderwidth=2, relief="raised")
#relief (flat,raised, sunken, solid)
quadro_teclas.place(x=10,y=10,width=325,height=150)


text_ = Label(quadro_teclas, text="Tecla de fisgar")
text_.grid(column=1, row= 0)

cb_tecla_fisgar =ttk.Combobox(quadro_teclas,values = ListTeclas)
cb_tecla_fisgar.set(tecla_fisgar.strip())
cb_tecla_fisgar.grid(column=1, row= 1, padx=3, pady=3)

text_ = Label(quadro_teclas, text="Tecla da vara")
text_.grid(column=1, row= 2)

cb_tecla_vara =ttk.Combobox(quadro_teclas,values = ListTeclas)
cb_tecla_vara.set(tecla_vara.strip())
cb_tecla_vara.grid(column=1, row= 3, padx=3, pady=3)


text_ = Label(quadro_teclas, text="Tecla inventário")
text_.grid(column=2, row= 0)

cb_tecla_inv =ttk.Combobox(quadro_teclas,values = ListTeclas)
cb_tecla_inv.set(tecla_inv.strip())
cb_tecla_inv.grid(column=2, row= 1, padx=15, pady=8)


text_ = Label(quadro_teclas, text="Tecla camera fixa")
text_.grid(column=2, row= 2)

cb_tecla_cam =ttk.Combobox(quadro_teclas,values = ListTeclas)
cb_tecla_cam.set(tecla_cam.strip())
cb_tecla_cam.grid(column=2, row= 3, padx=25, pady=8)

botao_salvar = Button(quadro_teclas, text='Salvar teclas', command=SalvarTeclas)
botao_salvar.grid(column=1, row=4, padx= 0, pady= 0)

quadro_varinha =Frame(janela, borderwidth=2, relief="flat")
#relief (flat,raised, sunken, solid)
quadro_varinha.place(x=10,y=180,width=150,height=130)

text_long_desc = Label(quadro_varinha, text="Força da varinha")
text_long_desc.grid(column=1, row= 2)

escala_long = Scale(quadro_varinha, from_= 1, to = 2.0,  orient=HORIZONTAL, resolution=0.1, command=BuscaForcaVara)
escala_long.set(long_linha)
escala_long.grid(column=1, row=3)

botao_iniciar = Button(quadro_varinha, text='Iniciar', command=Macro)
botao_iniciar.grid(column=1, row= 4,padx=50, pady=20)

quadro_historico =Frame(janela, borderwidth=2, relief="raised")
#relief (flat,raised, sunken, solid)
quadro_historico.place(x=10,y=310,width=325,height=250)

text_ = Label(quadro_historico, text="Histórico")
text_.grid(column=1, row= 30)

quadro_historico_msg =Frame(quadro_historico, borderwidth=2, relief="sunken", background="#D3D3D3")
#relief (flat,raised, sunken, solid)
quadro_historico_msg.place(x=5,y=80,width=300,height=100)

text_msg = Label(quadro_historico_msg, text="")
text_msg.grid(column=1, row= 1)

SalvarTeclas()
janela.mainloop()






