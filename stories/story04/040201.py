from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Function to run a quantum circuit multiple times and collect statistics
def run_circuit_multiple_times(qc, simulator, shots=1024, num_runs=5):
    """Run a quantum circuit multiple times and collect counts statistics."""
    all_counts = []
    for _ in range(num_runs):
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts(qc)
        all_counts.append(counts)
    return all_counts

# Use AerSimulator for simulation
simulator = AerSimulator()

# Function to create a quantum circuit with n qubits in a given initial state.
# initial_state should be a string of length n, e.g., "000" or "111".
def create_quantum_circuit(n, initial_state='0' * 3):
    qc = QuantumCircuit(n, n)  # n qubits, n classical bits
    # Apply X gate to qubits where the corresponding character is '1'
    for i, state in enumerate(initial_state):
        if state == '1':
            qc.x(i)
    qc.measure(range(n), range(n))  # Measure all qubits into classical bits
    return qc

# Example usage: Create circuits for n qubits
n = 3  # Number of qubits

# Create and run quantum circuits for the specified initial states '000' and '111'
initial_states = ['0' * n, '1' * n]
for state in initial_states:
    qc = create_quantum_circuit(n, state)
    counts = run_circuit_multiple_times(qc, simulator)
    for i, counts_run in enumerate(counts):
        # Save histogram plot for each run
        filename = f"measurement_results_{state}_run_{i+1}.png"
        plot_histogram(counts_run).savefig(filename)
        print(f"Measurement results for initial state {state}, run {i+1}: {counts_run}")

# Create and run a quantum circuit for the superposition state H|0⟩ (Hadamard on all qubits)
qc_superposition = QuantumCircuit(n, n)
qc_superposition.h(range(n))  # Apply H gate on all qubits to create superposition
qc_superposition.measure(range(n), range(n))  # Measure all qubits
counts_superposition = run_circuit_multiple_times(qc_superposition, simulator)
for i, counts_run in enumerate(counts_superposition):
    filename = f"measurement_results_superposition_run_{i+1}.png"
    plot_histogram(counts_run).savefig(filename)
    print(f"Measurement results for superposition state, run {i+1}: {counts_run}")
