from qiskit import QuantumCircuit, transpile
import numpy as np

# ⚙️ Scegli se usare un backend reale IBM Quantum o la simulazione
USE_REAL_BACKEND = False  # Imposta a True per testare su un dispositivo reale

if USE_REAL_BACKEND:
    # Se usi un backend reale, assicurati di avere qiskit-ibm-runtime installato
    from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
    service = QiskitRuntimeService(channel="ibm_quantum")
    backend = service.backend
    # Imposta il numero di shot (ad es. 1024) per il dispositivo reale
    sampler = Sampler(backend=backend, options={"shots": 1024})
else:
    # Simulazione con StatevectorSampler (ideale per debug e sviluppo)
    from qiskit.primitives import StatevectorSampler
    sampler = StatevectorSampler()

# 1️⃣ Imposta il seed per la riproducibilità
np.random.seed(42)

# 2️⃣ Creazione del dataset XOR
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y_train = np.array([0, 1, 1, 0])

# 3️⃣ Creazione del circuito quantistico combinato
num_qubits = 2
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
feature_map = ZZFeatureMap(num_qubits)
ansatz = RealAmplitudes(num_qubits, reps=2)

# Combiniamo feature_map e ansatz in un unico circuito
qc = QuantumCircuit(num_qubits)
qc.append(feature_map, range(num_qubits))
qc.append(ansatz, range(num_qubits))

# Ottimizzazione del circuito tramite transpilation
qc = transpile(qc, optimization_level=3)

# 4️⃣ Definizione della funzione di interpretazione: restituisce il bit di parità
def parity(x):
    return x % 2

# 5️⃣ Creazione della Quantum Neural Network con SamplerQNN
from qiskit_machine_learning.neural_networks import SamplerQNN
qnn = SamplerQNN(
    circuit=qc,                     # Circuito combinato
    sampler=sampler,                # Sampler (simulazione o reale)
    input_params=feature_map.parameters,  # Parametri del feature map
    weight_params=ansatz.parameters,        # Parametri dell'ansatz
    interpret=parity,               # Funzione per interpretare l'output
    output_shape=2                # Dimensione dell'output (per classificazione binaria)
)

# 6️⃣ Creazione del modello quantistico con NeuralNetworkClassifier (senza specificare l'ottimizzatore)
from qiskit_machine_learning.algorithms.classifiers import NeuralNetworkClassifier
classifier = NeuralNetworkClassifier(neural_network=qnn)

# 7️⃣ Addestramento del modello
print("🚀 Addestramento della Quantum Neural Network in corso...")
classifier.fit(X_train, Y_train)

# 8️⃣ Test del modello
predictions = classifier.predict(X_train)
print("✅ Predizioni AI Quantistica:", predictions)
