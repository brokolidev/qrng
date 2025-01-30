from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_state

number_of_qbits = 1  # number of quantum bits

# Create a quantum circuit with 1 qubit and 1 classical bit for measurement
qc = QuantumCircuit(number_of_qbits, 1)

# Plot the initial state (|0⟩ state) on the Bloch sphere
initial_state = qc.initialize([1, 0], 0)  # |0⟩ state initialization
plot_bloch_state(initial_state)

# Apply the X gate to the qubit
qc.x(0)

# Apply the Hadamard gate to the qubit
qc.h(0)

# Measure the qubit
qc.measure(0, 0)

# Use the AerSimulator to run the circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)

# Execute the circuit
job = simulator.run(compiled_circuit)
result = job.result()

# Get the measurement counts
counts = result.get_counts()
print(counts)

# Draw the circuit
print(qc.draw())
