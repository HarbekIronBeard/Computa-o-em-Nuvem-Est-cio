import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file'] 

def authenticate():
    """Autentica o usuário e retorna o serviço do Google Drive"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(service, file_path):
    """Faz o upload de um arquivo para o Google Drive"""
    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path, resumable=True)
    
    file_metadata = {'name': file_name}
    
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'Arquivo {file_name} enviado com sucesso, ID: {file.get("id")}')
    return file_name

def select_files():
    """Função para selecionar arquivos usando a interface do Tkinter"""
    files = filedialog.askopenfilenames(title="Selecione os arquivos")
    if files:
        service = authenticate()
        for file in files:
            uploaded_file = upload_file(service, file)
            messagebox.showinfo("Sucesso", f"Arquivo '{uploaded_file}' enviado com sucesso!")

root = tk.Tk()
root.title("Upload para o Google Drive")

canvas = tk.Canvas(root, height=300, width=400)
canvas.pack()

label = tk.Label(root, text="Selecione os arquivos para enviar ao Google Drive", font=('Helvetica', 12))
label.pack(pady=20)

select_button = tk.Button(root, text="Selecionar Arquivos", padx=10, pady=5, fg="white", bg="blue", command=select_files)
select_button.pack()

root.mainloop()
