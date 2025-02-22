import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import time
import concurrent.futures
import threading
import sys
import PyPDF2
import pytesseract
from pdf2image import convert_from_path

# Flag per controllare la chiusura
running = True

# Funzione per ottenere il contenuto di una pagina
def get_page_content(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException:
        return None
    return None

# Funzione per estrarre i link interni dal menu di navigazione
def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    nav_menu = soup.find("nav") or soup  # Cerca il menu di navigazione
    for link in nav_menu.find_all("a", href=True):
        href = link["href"].split("#")[0]  # Rimuove ancore
        if href.startswith("http") and base_url in href:
            links.add(href)
        elif href.startswith("/"):
            links.add(base_url + href)
    return links

# Funzione per analizzare il contenuto della pagina
def parse_content(html):
    soup = BeautifulSoup(html, "html.parser")
    data = []
    main_content = soup.find("main") or soup  # Cerca il contenuto principale
    sections = main_content.find_all(["section", "article", "div"], recursive=True)
    
    for section in sections:
        title = section.find(["h1", "h2", "h3"])
        title_text = title.get_text(strip=True) if title else "Senza titolo"
        paragraphs = section.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        if content:
            data.append({"Titolo": title_text, "Contenuto": content})
    
    return data

# Funzione per effettuare lo scraping di una singola pagina
def scrape_page(url):
    if not running:
        return [], set()
    html_content = get_page_content(url)
    if html_content:
        data = parse_content(html_content)
        new_links = extract_links(html_content, url)
        return data, new_links
    return [], set()

# Funzione per eseguire lo scraping su tutto il sito
def scrape_website(start_url, max_pages=200):
    visited = set()
    to_visit = {start_url}
    all_data = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        while to_visit and len(visited) < max_pages and running:
            futures = {executor.submit(scrape_page, url): url for url in to_visit}
            to_visit.clear()
            
            for future in concurrent.futures.as_completed(futures):
                url = futures[future]
                if url in visited or not running:
                    continue
                try:
                    data, new_links = future.result()
                    all_data.extend(data)
                    to_visit.update(new_links - visited)
                except Exception:
                    continue
                visited.add(url)
            time.sleep(1)
    
    return all_data

# Funzione per estrarre testo da PDF con OCR se necessario
def extract_text_from_pdf(pdf_path):
    extracted_data = []
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text and text.strip():
                extracted_data.append({"Pagina": page_num + 1, "Contenuto": text.strip()})
            else:
                # Se non c'è testo, usa OCR
                images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
                for image in images:
                    ocr_text = pytesseract.image_to_string(image, lang="eng")
                    if ocr_text.strip():
                        extracted_data.append({"Pagina": page_num + 1, "Contenuto": ocr_text.strip()})
    return extracted_data

# Funzione per selezionare e processare un PDF
def process_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        data = extract_text_from_pdf(file_path)
        save_to_json(data)

# Funzione per salvare i dati in JSON
def save_to_json(data):
    if not data:
        if root.winfo_exists():
            messagebox.showwarning("Nessun dato", "Nessun contenuto valido trovato!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        if root.winfo_exists():
            messagebox.showinfo("Salvato", f"Dati salvati in {file_path}")

# Funzione per avviare lo scraping in un thread separato
def start_scraping():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Attenzione", "Inserisci un URL valido!")
        return
    
    thread = threading.Thread(target=lambda: save_to_json(scrape_website(url)))
    thread.daemon = True
    thread.start()

# Funzione per gestire la chiusura della finestra
def on_closing():
    global running
    running = False  # Blocca i thread di scraping
    root.quit()
    root.destroy()
    sys.exit()

# Creazione dell'interfaccia grafica
root = tk.Tk()
root.title("Web Scraper & PDF Extractor")
root.geometry("400x250")
root.protocol("WM_DELETE_WINDOW", on_closing)  # Chiude correttamente la finestra

tk.Label(root, text="Inserisci URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Avvia Scraping", command=start_scraping)
scrape_button.pack(pady=10)

pdf_button = tk.Button(root, text="Estrarre testo da PDF", command=process_pdf)
pdf_button.pack(pady=10)

root.mainloop()
