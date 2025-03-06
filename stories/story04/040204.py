import os
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

# Get the current directory of the executing file and set up the "result" folder path
base_dir = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.join(base_dir, "result")

# Function to create a quantum circuit with n qubits in a given initial state.
# initial_state should be a string of length n, e.g., "000" or "111".
def create_quantum_circuit(n, initial_state):
    qc = QuantumCircuit(n, n)  # n qubits, n classical bits
    # Apply X gate to qubits where the corresponding character is '1'
    for i, state in enumerate(initial_state):
        if state == '1':
            qc.x(i)
    qc.measure(range(n), range(n))  # Measure all qubits into classical bits
    return qc

# Helper function to save histogram plots into a designated folder
def save_histogram_plot(plot_obj, folder_name, run_number, prefix=""):
    folder = os.path.join(result_dir, folder_name)
    os.makedirs(folder, exist_ok=True)  # Create the folder if it doesn't exist
    filename = f"{prefix}run_{run_number}.png" if prefix else f"run_{run_number}.png"
    file_path = os.path.join(folder, filename)
    plot_obj.savefig(file_path)
    print(f"Saved: {file_path}")

# Example usage: Create circuits for n qubits
n = 3  # Number of qubits

# 04.02.01: Basic circuit creation with initial states "000" and "111"
initial_states = ['0' * n, '1' * n]
for state in initial_states:
    qc = create_quantum_circuit(n, state)
    counts = run_circuit_multiple_times(qc, simulator)
    for i, counts_run in enumerate(counts, start=1):
        # Save to folder: result/measurement_results_<state>/
        save_histogram_plot(
            plot_histogram(counts_run),
            folder_name=f"measurement_results_{state}",
            run_number=i
        )
        print(f"Measurement results for initial state {state}, run {i}: {counts_run}")

# 04.02.02: Implement parallel gates – Applying Hadamard gates to all qubits in parallel
qc_parallel = QuantumCircuit(n, n)
qc_parallel.h(range(n))  # Apply H gate in parallel to all qubits
qc_parallel.measure(range(n), range(n))
counts_parallel = run_circuit_multiple_times(qc_parallel, simulator)
for i, counts_run in enumerate(counts_parallel, start=1):
    # Save to folder: result/parallel_hadamard/
    save_histogram_plot(
        plot_histogram(counts_run),
        folder_name="parallel_hadamard",
        run_number=i
    )
    print(f"Measurement results for parallel Hadamard gates, run {i}: {counts_run}")

# 04.02.03: Add multi-qubit measurement - Measure all qubits simultaneously
# Example: Apply X gate to qubit 0 and H gate to remaining qubits to create diverse states
qc_multi = QuantumCircuit(n, n)
qc_multi.x(0)
if n > 1:
    qc_multi.h(range(1, n))
qc_multi.measure(range(n), range(n))
counts_multi = run_circuit_multiple_times(qc_multi, simulator)
for i, counts_run in enumerate(counts_multi, start=1):
    # Save to folder: result/multi_qubit_measurement/
    save_histogram_plot(
        plot_histogram(counts_run),
        folder_name="multi_qubit_measurement",
        run_number=i
    )
    print(f"Measurement results for multi-qubit measurement, run {i}: {counts_run}")

# 04.02.04: Test multi-qubit output - Success: Generate numbers larger than 1 bit
# Create a circuit with more than one qubit (e.g., 4 qubits) to demonstrate multi-bit measurement output.
n_multi = 4  # Using 4 qubits for a multi-bit output
qc_multi_output = QuantumCircuit(n_multi, n_multi)
qc_multi_output.h(range(n_multi))  # Apply Hadamard gates to all qubits to create a superposition
qc_multi_output.measure(range(n_multi), range(n_multi))
counts_multi_output = run_circuit_multiple_times(qc_multi_output, simulator)
for i, counts_run in enumerate(counts_multi_output, start=1):
    # Save to folder: result/multi_qubit_output/
    save_histogram_plot(
        plot_histogram(counts_run),
        folder_name="multi_qubit_output",
        run_number=i
    )
    print(f"Measurement results for multi-qubit output, run {i}: {counts_run}")
