import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def clean_text(text):
    """Pulisce il testo rimuovendo caratteri speciali e normalizzando gli spazi."""
    text = text.lower()  # Converte in minuscolo
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Rimuove caratteri speciali
    text = re.sub(r"\s+", " ", text).strip()  # Rimuove spazi extra
    return text

# Carica i dati estratti (web scraping + PDF)
def load_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [entry["Contenuto"] for entry in data]

# Trasforma il testo in vettori numerici per la QNN
def preprocess_text(data):
    vectorizer = TfidfVectorizer(max_features=2)# Limitiamo a 10 feature per semplicità(ora 2)
    data = [clean_text(text) for text in data]  # Pulisce i testi
    X = vectorizer.fit_transform(data).toarray()

    return X

# Esegui il preprocessamento
def process_json(json_path):
    data = load_data(json_path)
    return preprocess_text(data)

if __name__ == "__main__":
    json_file = "data.json"  # Cambia con il tuo file JSON
    X_processed = process_json(json_file)
    print("✅ Dati preprocessati:", X_processed)
