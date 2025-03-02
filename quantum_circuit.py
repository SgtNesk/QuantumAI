from qiskit import IBMQ

# Salva il tuo API Token (solo la prima volta)
IBMQ.save_account('')

# Carico L'account IBM Quantum? 
IBMQ.load_account()

# Ottieni il provider IBM Quantum
