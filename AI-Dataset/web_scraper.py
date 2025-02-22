import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import urllib3

# Disabilita i warning SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_page_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    response = requests.get(url, headers=headers, verify=False)  # Disabilita verifica SSL
    if response.status_code == 200:
        return response.text
    else:
        messagebox.showerror("Errore", f"Errore {response.status_code} nel recupero della pagina")
        return None

def parse_content(html):
    soup = BeautifulSoup(html, "html.parser")
    data = []
    articles = soup.find_all(["article", "div", "section"])  # Cattura più elementi
    
    for article in articles:
        title = article.find("h2").get_text(strip=True) if article.find("h2") else "Senza titolo"
        content = article.find("p").get_text(strip=True) if article.find("p") else "Nessun contenuto"
        data.append({"Titolo": title, "Contenuto": content})
    
    return data

def save_to_json(data):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Salvato", f"Dati salvati in {file_path}")

def start_scraping():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Attenzione", "Inserisci un URL valido!")
        return
    
    html_content = get_page_content(url)
    if html_content:
        extracted_data = parse_content(html_content)
        save_to_json(extracted_data)

# Creazione dell'interfaccia grafica
root = tk.Tk()
root.title("Web Scraper GUI")
root.geometry("400x200")

tk.Label(root, text="Inserisci URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Avvia Scraping", command=start_scraping)
scrape_button.pack(pady=20)

root.mainloop()
