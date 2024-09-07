import customtkinter as ctk
from tkinter import filedialog, messagebox
import gzip
import os
import webbrowser

# Inicializa a aplicação CustomTkinter
ctk.set_appearance_mode("System")  # Alterna entre 'Light', 'Dark', ou 'System'
ctk.set_default_color_theme("blue")  # Altere para 'dark-blue', 'green', etc.

# Dicionário para mapear o ano selecionado ao valor de "Version="
year_to_version = {
    "2024": "42",
    "2023": "41",
    "2022": "40",
    "2021": "39",
    "2020": "38",
    "2019": "37",
    "2018": "36"
}

def process_file():
    file_path = filedialog.askopenfilename(filetypes=[("Premiere Project Files", "*.prproj")])
    if not file_path:
        return

    selected_year = year_var.get()
    new_version_value = year_to_version[selected_year]

    base_name = os.path.basename(file_path)
    new_file_name = base_name.replace('.prproj', f'_{selected_year}.prproj')
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

    file_counter = 1
    while os.path.exists(new_file_path):
        new_file_name = base_name.replace('.prproj', f'_{selected_year}_{file_counter}.prproj')
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        file_counter += 1

    try:
        with gzip.open(file_path, 'rb') as f_in:
            xml_content = f_in.read().decode('utf-8')

        lines = xml_content.splitlines()
        if len(lines) >= 4:
            version_prefix = 'Version="'
            start_index = lines[3].find(version_prefix)
            if start_index != -1:
                end_index = lines[3].find('"', start_index + len(version_prefix))
                current_version_value = lines[3][start_index + len(version_prefix):end_index]
                lines[3] = lines[3].replace(f'{version_prefix}{current_version_value}"', f'{version_prefix}{new_version_value}"')

        modified_xml_content = "\n".join(lines)

        with gzip.open(new_file_path, 'wb') as f_out:
            f_out.write(modified_xml_content.encode('utf-8'))

        messagebox.showinfo("Sucesso", f"Arquivo processado e salvo como {new_file_name}")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def open_linkedin(event):
    webbrowser.open_new("https://www.linkedin.com/in/lohan-costa/")

# Cria a interface gráfica usando CustomTkinter
root = ctk.CTk()
root.title("Modificador de Arquivos .prproj")
root.geometry("400x350")

# Título da aplicação
label_title = ctk.CTkLabel(root, text="Modificador de Arquivos .prproj", font=ctk.CTkFont(size=18, weight="bold"))
label_title.pack(pady=20)

# Cria uma variável para armazenar o ano selecionado
year_var = ctk.StringVar(value="2024")

# Rótulo e lista suspensa com os anos
label_year = ctk.CTkLabel(root, text="Selecione o ano:")
label_year.pack(pady=10)

year_menu = ctk.CTkOptionMenu(root, variable=year_var, values=["2024", "2023", "2022", "2021", "2020", "2019", "2018"])
year_menu.pack(pady=10)

# Botão para processar o arquivo
process_button = ctk.CTkButton(root, text="Selecionar Arquivo", command=process_file)
process_button.pack(pady=20)

# Assinatura com link para o LinkedIn
signature_label = ctk.CTkLabel(root, text="Desenvolvido por Lohan Costa, edt.", text_color="blue", cursor="hand2")
signature_label.pack(side="bottom", pady=10)

# Bind do clique para abrir o link do LinkedIn
signature_label.bind("<Button-1>", open_linkedin)

root.mainloop()
