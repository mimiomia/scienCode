# Importando as bibliotecas
from tkinter import Tk, Label, Entry, Button, PhotoImage
from pymongo import MongoClient
from catalogo import abrir_tela_catalogo  # função abrir_tela_catalogo
from bson.objectid import ObjectId
import json

# Conectando ao banco de dados MongoDB
client = MongoClient(f'mongodb+srv://marcelly1210:Celiana123@cluster0.qwzodtn.mongodb.net/?retryWrites=true&w=majority')
db = client['db_scien']
col_users = db['users']

# Função para cadastrar um novo usuário
def cadastrar():
    # Obtendo o email e senha inseridos pelo usuário
    email = entry_email.get()
    senha = entry_senha.get()

    # Verificando se foram preenchidos
    if email != "" and senha != "":
        # Gerando um novo ID para o usuário
        novo_id = str(ObjectId())
        
        # Inserindo os dados do novo usuário no banco de dados
        col_users.insert_one({
            "_id": novo_id,
            "email": email,
            "senha": senha
        })
        
        # Abrindo a tela de catálogo com o novo ID do usuário
        abrir_tela_catalogo(window, novo_id)

# Função para realizar o login
def login():
    # Obtendo o email e senha inseridos pelo usuário
    email = entry_email.get()
    senha = entry_senha.get()

    # Verificando se existe um usuário com o email fornecido
    if user := col_users.find_one({"email": email}):
        # Verificando se a senha inserida coincide com a senha do usuário no banco de dados
        if user["senha"] == senha:
            # Persistência de dados (usuário online)
            dados = {
              "online": True,
              "id_user": user['_id']
            }

            # Salvando os dados no arquivo de persistência JSON
            with open('persistencia.json', 'w') as arquivo_json:
                json.dump(dados, arquivo_json)
            
            # Abrindo a tela de catálogo com o ID do usuário autenticado
            abrir_tela_catalogo(window, user["_id"])

# Configuração da janela principal
window = Tk()
window.title("Página de Login")
window.geometry("400x300")
window.configure(bg="#221834")
window.attributes("-fullscreen", True)
window.overrideredirect(True)

# Verificando se o usuário já está online (persistência de dados)
with open('persistencia.json', 'r') as arquivo_json:
    dados_lidos = json.load(arquivo_json)

    # Se o usuário estiver online, abrir a tela de catálogo
    if dados_lidos.get('online'):
        abrir_tela_catalogo(window, dados_lidos.get('id_user'))

# Adicionando o logo à janela principal
logo_image = PhotoImage(file="C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame1\\image_2.png")
logo_label = Label(window, image=logo_image, bg="#221834")
logo_label.pack(pady=20)

# Campos de Email e Senha
label_email = Label(window, text="Email:", font=("Arial", 12), bg="#221834", fg="white")
label_email.pack()
entry_email = Entry(window, font=("Arial", 12))
entry_email.pack(pady=10)

label_senha = Label(window, text="Senha:", font=("Arial", 12), bg="#221834", fg="white")
label_senha.pack()
entry_senha = Entry(window, show="*", font=("Arial", 12))
entry_senha.pack(pady=10)

# Botões de Login e Cadastro
button_login_image = PhotoImage(file="C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame3\\button_login.png")
button_login = Button(window, image=button_login_image, command=login, bd=0, bg="#221834", cursor="hand2")
button_login.pack(pady=20)

button_cadastro_image = PhotoImage(file="C:\\Users\\Guifo\\Downloads\\catalogoTkinter-main\\catalogoTkinter-main\\scienCode\\build\\assets\\frame3\\button_cadastro.png")
button_cadastro = Button(window, image=button_cadastro_image, command=cadastrar, bd=0, bg="#221834", cursor="hand2")
button_cadastro.pack(pady=20)

# Iniciando o loop principal da aplicação
window.mainloop()