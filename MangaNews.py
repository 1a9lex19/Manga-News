import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def search_manga():
    manga_name = entry_name.get().strip()
    lang = lang_var.get()
    
    if not manga_name:
        messagebox.showwarning("Erreur", "Veuillez entrer un nom de manga.")
        return

    try:
        # Recherche du manga
        search_url = f"https://api.mangadex.org/manga?title={manga_name}&limit=1"
        search_resp = requests.get(search_url)
        search_data = search_resp.json()
        
        if not search_data.get('data'):
            results_var.set("Manga non trouvé.")
            return
        
        manga_id = search_data['data'][0]['id']
        manga_title = search_data['data'][0]['attributes']['title'].get('en', manga_name)

        # Récupérer le dernier chapitre
        chapter_url = f"https://api.mangadex.org/chapter?manga={manga_id}&translatedLanguage[]={lang}&order[chapter]=desc&limit=1"
        chapter_resp = requests.get(chapter_url)
        chapter_data = chapter_resp.json()

        if not chapter_data.get('data'):
            results_var.set("Aucun chapitre trouvé pour cette langue.")
            return

        chapter = chapter_data['data'][0]['attributes']
        chapter_number = chapter.get('chapter', "Special/Extra")
        publish_date = datetime.fromisoformat(chapter['publishAt'].replace('Z', '+00:00')).strftime('%d/%m/%Y')

        results_var.set(f"{manga_title}\nDernier chapitre ({'VF' if lang=='fr' else 'VA'}): {chapter_number}\nSorti le: {publish_date}")

        # Notification simple (Tkinter messagebox)
        messagebox.showinfo("Manga News", f"Dernier chapitre de {manga_title} : {chapter_number} ({'VF' if lang=='fr' else 'VA'})")

    except Exception as e:
        results_var.set("Erreur lors de la récupération des données.")
        print(e)

# Interface Tkinter
root = tk.Tk()
root.title("Manga News")
root.geometry("400x250")

tk.Label(root, text="Nom du manga:").pack(pady=5)
entry_name = tk.Entry(root, width=40)
entry_name.pack(pady=5)

tk.Label(root, text="Langue:").pack(pady=5)
lang_var = tk.StringVar(value="en")
lang_menu = ttk.Combobox(root, textvariable=lang_var, values=["en", "fr"], state="readonly")
lang_menu.pack(pady=5)

tk.Button(root, text="Rechercher", command=search_manga).pack(pady=10)

results_var = tk.StringVar()
tk.Label(root, textvariable=results_var, justify="left").pack(pady=10)

root.mainloop()