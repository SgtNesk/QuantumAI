from qiskit import IBMQ

# Salva il tuo API Token (solo la prima volta)
IBMQ.save_account('c796dc87928c597dbfb2983b67ac4250e6d07f887580bc64009f52a11a153ed6ff13640175b43c8040c0a022b498760ec86cc8dcc2a79cc017a4caa034a17c95')

# Carico L'account IBM Quantum? 
IBMQ.load_account()

# Ottieni il provider IBM Quantum