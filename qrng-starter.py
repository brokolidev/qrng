from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

number_of_qbits = 4  # number of quantum bits
qc = QuantumCircuit(number_of_qbits)

# H gate implementation
for i in range(number_of_qbits):
    qc.h(i)

# Measure all qbits
qc.measure_all()

# Run the quantum circuit on a simulator backend
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()

# Get the counts of the result
counts = result.get_counts()
quantum_bin = list(counts.keys())[0]  # 랜덤 비트 결과
print("Quantum RNG Binary Result:", quantum_bin)
