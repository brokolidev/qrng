import os
import json
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure log directory exists in the current file's directory
log_dir = os.path.join(current_dir, 'log')
os.makedirs(log_dir, exist_ok=True)

# Ensure image directory exists in the current file's directory
def ensure_image_dir(img_dir_name):
    img_dir = os.path.join(current_dir, img_dir_name)
    os.makedirs(img_dir, exist_ok=True)
    return img_dir

# Function to log measurement results to a file
def log_measurement_results(filename, data):
    filepath = os.path.join(log_dir, filename)
    with open(filepath, 'a') as file:
        json.dump(data, file)
        file.write('\n')

# Function to run a quantum circuit multiple times and collect statistics
def run_circuit_multiple_times(qc, simulator, shots=1024, num_runs=10, log_filename='measurement_log.json'):
    all_counts = []
    
    for run in range(num_runs):
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts(qc)
        all_counts.append(counts)
        
        # Log the measurement results
        log_entry = {
            'run': run + 1,
            'counts': counts
        }
        log_measurement_results(log_filename, log_entry)
        
    return all_counts

# Use AerSimulator for simulation
simulator = AerSimulator()

# 1️⃣ Measuring the |0⟩ state
qc_0 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_0.measure(0, 0)  # Measure the qubit and store the result in the classical bit

counts_0 = run_circuit_multiple_times(qc_0, simulator)

# Save histograms for each run
img_dir_0 = ensure_image_dir('measurement_results_0_img')
for i, counts in enumerate(counts_0):
    plot_histogram(counts).savefig(os.path.join(img_dir_0, f'measurement_results_0_run_{i+1}.png'))
    print(f"Measurement results for |0⟩ state, run {i+1}:", counts)


# 2️⃣ Measuring the |1⟩ state
qc_1 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_1.x(0)  # Apply X gate to flip the state to |1⟩
qc_1.measure(0, 0)  # Measure the qubit and store the result in the classical bit

counts_1 = run_circuit_multiple_times(qc_1, simulator)

# Save histograms for each run
img_dir_1 = ensure_image_dir('measurement_results_1_img')
for i, counts in enumerate(counts_1):
    plot_histogram(counts).savefig(os.path.join(img_dir_1, f'measurement_results_1_run_{i+1}.png'))
    print(f"Measurement results for |1⟩ state, run {i+1}:", counts)


# 3️⃣ Measuring the superposition state H|0⟩
qc_superposition = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
qc_superposition.h(0)  # Apply H gate to create superposition state
qc_superposition.measure(0, 0)  # Measure the qubit and store the result in the classical bit

counts_superposition = run_circuit_multiple_times(qc_superposition, simulator)

# Save histograms for each run
img_dir_superposition = ensure_image_dir('measurement_results_superposition_img')
for i, counts in enumerate(counts_superposition):
    plot_histogram(counts).savefig(os.path.join(img_dir_superposition, f'measurement_results_superposition_run_{i+1}.png'))
    print(f"Measurement results for superposition state H|0⟩, run {i+1}:", counts)
