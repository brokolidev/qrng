from qiskit import QuantumCircuit

# 1 qubit, 1 classical bit
circuit = QuantumCircuit(1, 1)

# Apply Hadamard gate to create superposition
circuit.h(0)

# Draw the circuit
print(circuit.draw())
