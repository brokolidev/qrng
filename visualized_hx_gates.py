from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_vector

# Number of qubits
number_of_qbits = 1

# Use the AerSimulator to run the circuit
simulator = AerSimulator()

# 1️⃣ Initial State |0⟩ (default state)
qc_initial = QuantumCircuit(number_of_qbits)
qc_initial.save_statevector()  # Save the initial statevector

# Run simulation for the initial state
compiled_circuit_initial = transpile(qc_initial, simulator)
result_initial = simulator.run(compiled_circuit_initial).result()
statevector_initial = result_initial.get_statevector(0)

# Plot Bloch sphere for the initial state |0⟩ (north pole)
bloch_initial = plot_bloch_vector([0, 0, 1], title="Initial State |0⟩")
bloch_initial.savefig('initial_bloch.png')


# 2️⃣ Apply Hadamard Gate
qc_hadamard = QuantumCircuit(number_of_qbits)
qc_hadamard.h(0)               # Apply Hadamard gate
qc_hadamard.save_statevector() # Save the statevector after Hadamard

# Run simulation after applying the Hadamard gate
compiled_circuit_hadamard = transpile(qc_hadamard, simulator)
result_hadamard = simulator.run(compiled_circuit_hadamard).result()
statevector_hadamard = result_hadamard.get_statevector(0)

# Bloch vector for Hadamard result is [1, 0, 0] (on the X-axis)
bloch_hadamard = plot_bloch_vector([1, 0, 0], title="After Hadamard Gate")
bloch_hadamard.savefig('hadamard_bloch.png')


# 3️⃣ Apply X Gate
qc_x = QuantumCircuit(number_of_qbits)
qc_x.x(0)               # Apply X gate (Pauli-X)
qc_x.save_statevector() # Save the statevector after X gate

# Run simulation after applying the X gate
compiled_circuit_x = transpile(qc_x, simulator)
result_x = simulator.run(compiled_circuit_x).result()
statevector_x = result_x.get_statevector(0)

# Bloch vector for |1⟩ state (after X gate) is [0, 0, -1] (south pole)
bloch_x = plot_bloch_vector([0, 0, -1], title="After X Gate (|1⟩ State)")
bloch_x.savefig('x_gate_bloch.png')


print("Bloch sphere images saved as:")
print("- 'initial_bloch.png' (Initial State |0⟩)")
print("- 'hadamard_bloch.png' (After Hadamard Gate)")
print("- 'x_gate_bloch.png' (After X Gate)")
