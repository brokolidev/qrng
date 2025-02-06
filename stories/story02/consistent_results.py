from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Use AerSimulator for simulation
simulator = AerSimulator()

# 1️⃣ Measuring the |0⟩ state
qc_0 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_0.measure(0, 0)  # Measure the qubit and store the result in the classical bit

# Compile and run the circuit
compiled_circuit_0 = transpile(qc_0, simulator)
result_0 = simulator.run(compiled_circuit_0, shots=1024).result()

# Get the measurement result counts
counts_0 = result_0.get_counts(qc_0)
print("Measurement results for |0⟩ state:", counts_0)

# Plot the histogram for |0⟩ state
plot_histogram(counts_0).savefig('consistent_result0.png')


# 2️⃣ Measuring the |1⟩ state
qc_1 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_1.x(0)  # Apply X gate to flip the state to |1⟩
qc_1.measure(0, 0)  # Measure the qubit and store the result in the classical bit

# Compile and run the circuit
compiled_circuit_1 = transpile(qc_1, simulator)
result_1 = simulator.run(compiled_circuit_1, shots=1024).result()

# Get the measurement result counts
counts_1 = result_1.get_counts(qc_1)
print("Measurement results for |1⟩ state:", counts_1)

# Plot the histogram for |1⟩ state
plot_histogram(counts_1).savefig('consistent_result1.png')
