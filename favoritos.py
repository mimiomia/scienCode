import tkinter as tk
from PIL import Image, ImageTk
from pymongo import MongoClient
import json

#Criando conexao com bando de dados
client = MongoClient(f'mongodb+srv://marcelly1210:Celiana123@cluster0.qwzodtn.mongodb.net/?retryWrites=true&w=majority')
db = client["db_scien"]
col_favorito = db["favoritos"]

#Definindo funcoes
def desfavoritar(botao, id_item, id_user):
    favoritos_user = col_favorito.find_one({"id_user": id_user})

    if favoritos_user:
        lista_favoritos = favoritos_user["lista_favoritos"]
        lista_favoritos.remove(id_item)
        col_favorito.update_one({"id_user": id_user}, {"$set": {"lista_favoritos": lista_favoritos}})

    botao.destroy()


def deslogar(w):
    w.destroy()
    dados = {
        "online": False,
        "id_user": ""
    }

    with open('persistencia.json', 'w') as arquivo_json:
        json.dump(dados, arquivo_json)

#Centralizando as colunas definindo o valor 0 como inicial
def centralizar_horizontalmente(widget, colunas):
    widget.grid(column=0, row=0, columnspan=colunas)


def voltar(window, windowAtual, metodo, id_user):
    metodo(windowAtual, id_user)


def abrir_tela_favoritos(window, id_user, metodo_reconstroi):
    # Ocultar a janela anterior
    window.destroy()

    # Criar uma nova janela para o catálogo em tela cheia
    janela_favoritos = tk.Toplevel()
    janela_favoritos.title("Página de Favoritos")
    janela_favoritos.configure(bg="#0d071a")
    janela_favoritos.attributes("-fullscreen", True)
    janela_favoritos.overrideredirect(True)

    #Adicionando imagem para os botões
    frame = tk.Frame(janela_favoritos)
    frame.place(relx=0.5, rely=0, anchor="n")
    frame.configure(bg="#0d071a")

    imagem_catalogo = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame0\image_catalogo.png")
    imagem_catalogo = ImageTk.PhotoImage(imagem_catalogo)

    imagem_favoritos = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame0\\button_favoritos.png")
    imagem_favoritos = ImageTk.PhotoImage(imagem_favoritos)

    imagem_sair = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame0\\button_sair.png")
    imagem_sair = ImageTk.PhotoImage(imagem_sair)

    imagem_item1 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\itens\item1.PNG")
    imagem_item1 = ImageTk.PhotoImage(imagem_item1)

    imagem_item2 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\itens\item2.PNG")
    imagem_item2 = ImageTk.PhotoImage(imagem_item2)

    imagem_item3 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\itens\item3.PNG")
    imagem_item3 = ImageTk.PhotoImage(imagem_item3)

    # Adiciona uma referência à imagem para evitar a coleta de lixo
    janela_favoritos.imagem_catalogo = imagem_catalogo
    janela_favoritos.imagem_favoritos = imagem_favoritos
    janela_favoritos.imagem_sair = imagem_sair

    janela_favoritos.imagem_item1 = imagem_item1
    janela_favoritos.imagem_item2 = imagem_item2
    janela_favoritos.imagem_item3 = imagem_item3

    #Criação e configuração dos botões de navegação, além de consulta com o MongoDB para realizar logout.
    btct = tk.Button(frame, image=imagem_catalogo, bd=0, bg="#0d071a", cursor="hand2")
    centralizar_horizontalmente(btct, 1)
    btct.grid(column=0, row=1, columnspan=3)
    btct.configure(
        command=lambda p1=window, p2=janela_favoritos, p3=metodo_reconstroi, p4=id_user: voltar(p1, p2, p3, p4))

    tk.Button(frame, image=imagem_favoritos, bd=0, bg="#0d071a", cursor="hand2").grid(column=0, row=2, columnspan=3)
    tk.Button(frame, image=imagem_sair, bd=0, command=lambda p1=janela_favoritos: deslogar(p1), bg="#0d071a",
              cursor="hand2").grid(column=0, row=3, columnspan=3)

    user = col_favorito.find_one({'id_user': id_user})

    #Criando botões e definindo variáveis de interação dos itens favoritados, como desfavoritar
    if user:
        for i in user.get('lista_favoritos'):
            if i == 1:
                item1 = tk.Button(frame, image=imagem_item1, bd=0, bg="#0d071a", cursor="hand2")
                item1.configure(command=lambda botao=item1, p1=1, p2=id_user: desfavoritar(botao, p1, p2))
                item1.grid(column=0, row=4,  padx=10)
            elif i == 2:
                item2 = tk.Button(frame, image=imagem_item2, bd=0, bg="#0d071a", cursor="hand2")
                item2.configure(command=lambda botao=item2, p1=2, p2=id_user: desfavoritar(botao, p1, p2))
                item2.grid(column=1, row=4,  padx=10)
            elif i == 3:
                item3 = tk.Button(frame, image=imagem_item3, bd=0, bg="#0d071a", cursor="hand2")
                item3.configure(command=lambda botao=item3, p1=3, p2=id_user: desfavoritar(botao, p1, p2))
                item3.grid(column=2, row=4,  padx=10)
