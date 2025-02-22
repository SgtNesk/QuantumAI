import numpy as np
from qiskit_machine_learning.algorithms.classifiers import NeuralNetworkClassifier
from preprocessore import process_json
from quantum_neural_network import qnn  # Importa il modello QNN
import joblib

MODEL_PATH = "qnn_model.pkl"  # Percorso per salvare il modello

# Controlla se il modello è già stato salvato
try:
    classifier = joblib.load(MODEL_PATH)
    print("✅ Modello QNN caricato con successo!")
except FileNotFoundError:
    print("🚀 Addestramento della Quantum Neural Network in corso...")
    classifier = NeuralNetworkClassifier(neural_network=qnn)
    X_train = process_json("data.json")  # Usa i dati preprocessati
  
    # Generiamo Y_train e Z_train per allenare la QNN su più assi
    Y_train = np.random.randint(0, 2, size=len(X_train))
    Z_train = np.random.randint(0, 2, size=len(X_train))
    
    # Ripeti l'addestramento più volte per migliorare la convergenza
    for _ in range(20):
        classifier.fit(X_train, Y_train)  # Addestriamo su asse Y
        classifier.fit(X_train, Z_train)  # Addestriamo su asse Z
    
    joblib.dump(classifier, MODEL_PATH)  # Salva il modello addestrato
    print("✅ Modello QNN salvato con successo!")

if __name__ == "__main__":
    print("✅ Modello pronto per l'inferenza.")
