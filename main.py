import tkinter as tk
from tkinter import filedialog
import pandas as pd
import chardet

def get_csv_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def dividir_arquivo(input_path, chunk_size, entry_path_label, success_label):
    try:
        encoding = get_csv_encoding(input_path)
        df = pd.read_csv(input_path, delimiter=';', encoding=encoding)

        chunk_size = 5999
        chunks = [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

        for i, chunk in enumerate(chunks):
            chunk.to_csv(f'Arquivo_formatado_{i + 1}.csv', index=False, sep=';')

        entry_path_label.config(text="", fg="black")
        success_message = f'{len(chunks)} arquivos criados com sucesso.'
        print("Concluído")
        success_label.config(text=success_message, fg="green")
    except pd.errors.ParserError as e:
        with open(input_path, 'r', encoding='utf-16') as file:
            lines = file.readlines()
            print(lines)
        entry_path_label.config(text="ERRO: Não foi possível determinar a codificação correta do arquivo.", fg="red")
        print("Aqui")
        success_label.config(text="", fg="black")

def selecionar_arquivo(entry_path_label, success_label):
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    entry_path_label.config(text="")
    entry_path_label.delete(0, tk.END)
    entry_path_label.insert(0, file_path)
    success_label.config(text="", fg="black")

def criar_app():
    app = tk.Tk()
    app.title("Divisor de Arquivos CSV - Importador de Histórico")
    label_instrucoes = tk.Label(app, text="Selecione o arquivo CSV a ser dividido:")
    label_instrucoes.pack(pady=10)
    entry_path = tk.Entry(app, width=50)
    entry_path.pack(pady=10)
    qtd_row = tk.Label(app, text="Tamanho do Arquivo csv: 5999")
    qtd_row.pack(pady=5)
    success_label = tk.Label(app, text="", fg="green")
    success_label.pack(pady=5)
    btn_selecionar = tk.Button(app, text="Selecionar Arquivo", command=lambda: selecionar_arquivo(entry_path, success_label))
    btn_selecionar.pack(pady=10)
    btn_dividir = tk.Button(app, text="Dividir Arquivo", command=lambda: dividir_arquivo(entry_path.get(), 5999, qtd_row, success_label))
    btn_dividir.pack(pady=10)
    app.mainloop()

criar_app()
