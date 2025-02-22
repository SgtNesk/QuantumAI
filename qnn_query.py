import numpy as np
from preprocessore import process_json
from qnn_model import classifier

# Funzione per interrogare la QNN
def query_qnn(text_input):
    # Converte il testo in un array per il modello
    X_query = process_json("data.json")  # Usa il dataset esistente
    if len(X_query) == 0:
        print("❌ Nessun dato valido trovato!")
        return
    
    # Espandiamo il vettore di input per sfruttare più feature
    if len(X_query) < 20:
        X_query = np.pad(X_query, ((0, 20 - len(X_query)), (0, 0)), mode='constant')
    
    # Predizione della QNN
    prediction = classifier.predict([X_query[0]])  # Usa il primo vettore correttamente dimensionato
    return prediction

if __name__ == "__main__":
    while True:
        user_input = input("📝 Inserisci una frase (o 'exit' per uscire): ")
        if user_input.lower() == "exit":
            break
        result = query_qnn(user_input)
        print("🔍 Risultato della QNN:", result)
