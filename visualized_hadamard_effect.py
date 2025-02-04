from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_vector
import numpy as np

# Number of qubits
number_of_qbits = 1

# Use the AerSimulator to run the circuit
simulator = AerSimulator()

# 1️⃣ Initial State |0⟩ (default state, no gate needed)
qc_initial = QuantumCircuit(number_of_qbits)
qc_initial.save_statevector()  # Save the initial statevector

# Run simulation to get the statevector for the initial state
compiled_circuit_initial = transpile(qc_initial, simulator)
result_initial = simulator.run(compiled_circuit_initial).result()
statevector_initial = result_initial.get_statevector(0)  # Specify the first result

# Plot Bloch sphere for the initial state
bloch_initial = plot_bloch_vector([0, 0, 1], title="Initial State |0⟩")
bloch_initial.savefig('initial_bloch.png')  # Save the initial Bloch sphere


# 2️⃣ Apply Hadamard Gate
qc_hadamard = QuantumCircuit(number_of_qbits)
qc_hadamard.h(0)               # Apply Hadamard gate
qc_hadamard.save_statevector() # Save the statevector after Hadamard

# Run simulation after applying the Hadamard gate
compiled_circuit_hadamard = transpile(qc_hadamard, simulator)
result_hadamard = simulator.run(compiled_circuit_hadamard).result()
statevector_hadamard = result_hadamard.get_statevector(0)  # Specify the first result

# Plot Bloch sphere after Hadamard gate
bloch_hadamard = plot_bloch_vector([1, 0, 0], title="After Hadamard Gate")
bloch_hadamard.savefig('hadamard_bloch.png')  # Save the Bloch sphere after Hadamard

print("Bloch sphere images saved as 'initial_bloch.png' and 'hadamard_bloch.png'")
