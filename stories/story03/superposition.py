from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


# Create a Quantum Circuit with 1 qubit
qc = QuantumCircuit(1)

# Apply Hadamard gate to create superposition
qc.h(0)

# Visualize the circuit
qc.draw('mpl')

# Use Aer's qasm_simulator
simulator = AerSimulator()

# Transpile the circuit for the simulator
compiled_circuit = transpile(qc, simulator)

# Execute the circuit on the qasm simulator
job = simulator.run(compiled_circuit)

# Grab results from the job
result = job.result()

# Check if the job resulted in counts
if 'counts' in result.data():
    # Returns counts
    counts = result.get_counts(compiled_circuit)
    print("\nTotal count for 0 and 1 are:", counts)

    # Visualize the results
    histogram = plot_histogram(counts)

    # Save the histogram to a file
    histogram.savefig('histogram.png')
else:
    print("\nNo counts returned from the experiment")