from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Create a quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Initialize the simulator
simulator = AerSimulator()

# Transpile the circuit for the simulator
compiled_circuit = transpile(qc, simulator)

# Execute the circuit on the simulator
result = simulator.run(compiled_circuit).result()

# Retrieve and print the results
counts = result.get_counts()
print(counts)
