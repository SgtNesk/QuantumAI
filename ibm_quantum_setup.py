from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera il token dalla variabile IBM_API_TOKEN
IBM_API_TOKEN = os.environ.get("IBM_API_TOKEN")
if IBM_API_TOKEN is None:
    raise ValueError("IBM_API_TOKEN non trovato nel file .env!")

# Importa il servizio IBM Quantum Runtime e Sampler
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit import QuantumCircuit, transpile

# Connettiti al servizio IBM Quantum usando il token e il canale 'ibm_quantum'
service = QiskitRuntimeService(token=IBM_API_TOKEN, channel="ibm_quantum")

# Seleziona esplicitamente il backend "ibm_kyiv"
backend = service.backend(name="ibm_kyiv")
print(f"Utilizzando il backend: {backend.name}")

# Crea un circuito quantistico semplice:
# - 1 qubit e 1 bit classico
# - Applica la porta Hadamard per creare la superposizione
# - Misura il qubit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
print("Circuito quantistico:")
print(qc.draw())

# Ottimizza il circuito tramite transpilation per il backend selezionato
qc_optimized = transpile(qc, backend=backend, optimization_level=3)

# Crea il Sampler specificando il backend e le opzioni (shots)
sampler = Sampler(backend=backend, options={"shots": 1024})

# Esegui il circuito (non è necessario specificare nuovamente il backend)
job = sampler.run(circuits=[qc_optimized])
result = job.result()

# Ottieni i conteggi dei risultati
counts = result.get_counts()
print("Risultati dell'esecuzione:")
print(counts)