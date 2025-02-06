from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Function to run a quantum circuit multiple times and collect statistics
def run_circuit_multiple_times(qc, simulator, shots=1024, num_runs=5):
    all_counts = []
    
    for _ in range(num_runs):
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts(qc)
        all_counts.append(counts)
        
    return all_counts

# Use AerSimulator for simulation
simulator = AerSimulator()

# 1️⃣ Measuring the |0⟩ state
qc_0 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_0.measure(0, 0)  # Measure the qubit and store the result in the classical bit

counts_0 = run_circuit_multiple_times(qc_0, simulator)

# Save histograms for each run
for i, counts in enumerate(counts_0):
    plot_histogram(counts).savefig(f'measurement_results_0_run_{i+1}.png')
    print(f"Measurement results for |0⟩ state, run {i+1}:", counts)


# 2️⃣ Measuring the |1⟩ state
qc_1 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_1.x(0)  # Apply X gate to flip the state to |1⟩
qc_1.measure(0, 0)  # Measure the qubit and store the result in the classical bit

counts_1 = run_circuit_multiple_times(qc_1, simulator)

# Save histograms for each run
for i, counts in enumerate(counts_1):
    plot_histogram(counts).savefig(f'measurement_results_1_run_{i+1}.png')
    print(f"Measurement results for |1⟩ state, run {i+1}:", counts)


# 3️⃣ Measuring the superposition state H|0⟩
qc_superposition = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_superposition.h(0)  # Apply H gate to create superposition state
qc_superposition.measure(0, 0)  # Measure the qubit and store the result in the classical bit

counts_superposition = run_circuit_multiple_times(qc_superposition, simulator)

# Save histograms for each run
for i, counts in enumerate(counts_superposition):
    plot_histogram(counts).savefig(f'measurement_results_superposition_run_{i+1}.png')
    print(f"Measurement results for superposition state H|0⟩, run {i+1}:", counts)
