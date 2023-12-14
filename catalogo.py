# Importando as bibliotecas
import tkinter as tk  # Tkinter para criar interfaces gráficas
from PIL import Image, ImageTk  # Pillow é uma biblioteca para manipulação de imagens
from pymongo import MongoClient  # pymongo é uma biblioteca para interagir com o MongoDB
from favoritos import abrir_tela_favoritos  # Importando função específica
import json  # Json para manipular dados e o estado do usuário

# Conectando ao servidor MongoDB usando a URL de conexão
client = MongoClient(
    f"mongodb+srv://marcelly1210:Celiana123@cluster0.qwzodtn.mongodb.net/?retryWrites=true&w=majority"
)
db = client["db_scien"]
col_favorito = db["favoritos"]


# Função para favoritar um item
def favoritar(botao, image, id_item, id_user):
    favoritos_user = col_favorito.find_one({"id_user": id_user})

    botao.configure(image=image)

    if favoritos_user:
        lista_favoritos = favoritos_user["lista_favoritos"]

        if id_item not in lista_favoritos:
            lista_favoritos.append(id_item)
            col_favorito.update_one(
                {"id_user": id_user}, {"$set": {"lista_favoritos": lista_favoritos}}
            )
    else:
        col_favorito.insert_one({"id_user": id_user, "lista_favoritos": [id_item]})


# Função para deslogar
def deslogar(w):
    w.destroy()
    dados = {"online": False, "id_user": ""}

    with open("persistencia.json", "w") as arquivo_json:
        json.dump(dados, arquivo_json)


# Função para abrir a tela de catálogo
def abrir_tela_catalogo(window, id_user):
    # Ocultar nossa janela anterior
    window.withdraw()

    # Criar uma nova janela para o catálogo em tela cheia
    janela_catalogo = tk.Toplevel()
    janela_catalogo.title("Página de Catálogo")
    janela_catalogo.configure(bg="#0d071a")
    janela_catalogo.attributes("-fullscreen", True)
    janela_catalogo.overrideredirect(True)

    # Carregando imagens para botões e elementos gráficos
    imagem_catalogo = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame0\image_catalogo.png"
    )
    imagem_catalogo = ImageTk.PhotoImage(imagem_catalogo)

    imagem_favoritos = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame0\\button_favoritos.png"
    )
    imagem_favoritos = ImageTk.PhotoImage(imagem_favoritos)

    imagem_sair = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame0\\button_sair.png"
    )
    imagem_sair = ImageTk.PhotoImage(imagem_sair)

    imagem_favorito1 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\favoritos\desfavorito1.png"
    )
    imagem_favorito1 = ImageTk.PhotoImage(imagem_favorito1)

    imagem_favorito2 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\favoritos\desfavorito2.png"
    )
    imagem_favorito2 = ImageTk.PhotoImage(imagem_favorito2)

    imagem_favorito3 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\favoritos\desfavorito3.png"
    )
    imagem_favorito3 = ImageTk.PhotoImage(imagem_favorito3)

    imagem_favoritado1 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\favoritos\\favorito1.PNG"
    )
    imagem_favoritado1 = ImageTk.PhotoImage(imagem_favoritado1)

    imagem_favoritado2 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\favoritos\\favorito2.PNG"
    )
    imagem_favoritado2 = ImageTk.PhotoImage(imagem_favoritado2)

    imagem_favoritado3 = Image.open(
        "C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\favoritos\\favorito3.PNG"
    )
    imagem_favoritado3 = ImageTk.PhotoImage(imagem_favoritado3)

    # Adiciona uma referência à imagem para evitar coleta de lixo
    janela_catalogo.imagem_catalogo = imagem_catalogo
    janela_catalogo.imagem_favoritos = imagem_favoritos
    janela_catalogo.imagem_sair = imagem_sair

    janela_catalogo.imagem_favorito1 = imagem_favorito1
    janela_catalogo.imagem_favorito2 = imagem_favorito2
    janela_catalogo.imagem_favorito3 = imagem_favorito3

    janela_catalogo.imagem_favoritado1 = imagem_favoritado1
    janela_catalogo.imagem_favoritado2 = imagem_favoritado2
    janela_catalogo.imagem_favoritado3 = imagem_favoritado3

    tk.Button(
        janela_catalogo, image=imagem_catalogo, bd=0, bg="#0d071a", cursor="hand2"
    ).grid(column=0, row=1)

    btfv = tk.Button(
        janela_catalogo, image=imagem_favoritos, bd=0, bg="#0d071a", cursor="hand2"
    )
    btfv.grid(column=0, row=2)
    btfv.configure(
        command=lambda p1=janela_catalogo, p2=id_user, p3=abrir_tela_catalogo: abrir_tela_favoritos(
            p1, p2, p3
        )
    )

    tk.Button(
        janela_catalogo,
        image=imagem_sair,
        bd=0,
        command=lambda p1=janela_catalogo: deslogar(p1),
        bg="#0d071a",
        cursor="hand2",
    ).grid(column=0, row=3)

    favoritos1 = tk.Button(
        janela_catalogo, image=imagem_favorito1, bd=0, bg="#0d071a", cursor="hand2"
    )
    favoritos1.configure(
        command=lambda botao=favoritos1, image=imagem_favoritado1, p1=1, p2=id_user: favoritar(
            botao, image, p1, p2
        )
    )
    favoritos1.grid(column=0, row=4, pady=10, padx=10)

    favoritos2 = tk.Button(
        janela_catalogo, image=imagem_favorito2, bd=0, bg="#0d071a", cursor="hand2"
    )
    favoritos2.configure(
        command=lambda botao=favoritos2, image=imagem_favoritado2, p1=2, p2=id_user: favoritar(
            botao, image, p1, p2
        )
    )
    favoritos2.grid(column=0, row=5, pady=10, padx=10)

    favoritos3 = tk.Button(
        janela_catalogo, image=imagem_favorito3, bd=0, bg="#0d071a", cursor="hand2"
    )
    favoritos3.configure(
        command=lambda botao=favoritos3, image=imagem_favoritado3, p1=3, p2=id_user: favoritar(
            botao, image, p1, p2
        )
    )
    favoritos3.grid(column=0, row=6, pady=10, padx=10)
