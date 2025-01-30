from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

number_of_qbits = 4  # number of quantum bits
qc = QuantumCircuit(number_of_qbits)

# Hadamard gates to create superposition
for i in range(number_of_qbits):
    qc.h(i)

# Entanglement using CNOT gates
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)

# Adding phase shifts for more randomness
qc.s(0)  # S gate (π/2 phase shift)
qc.t(2)  # T gate (π/4 phase shift)

# Measure all qbits
qc.measure_all()

# Run the quantum circuit on a simulator backend
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()

# Get the counts of the result
counts = result.get_counts()

# Get the binary result
quantum_bin = list(counts.keys())[0]

# Print the result
print("Quantum RNG Binary Result:", quantum_bin)
