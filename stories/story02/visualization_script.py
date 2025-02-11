from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Function to measure quantum state and return counts
def measure_state(qc, shots=1024):
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    result = simulator.run(compiled_circuit, shots=shots).result()
    counts = result.get_counts(qc)
    return counts

# Function to plot measurement distribution
def plot_measurement_distribution(counts, title):
    plot_histogram(counts)
    plt.title(title)
    plt.show()

# Create visualization script
def create_visualization_script():
    # 1️⃣ Measuring the |0⟩ state
    qc_0 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
    qc_0.measure(0, 0)  # Measure the qubit and store the result in the classical bit
    counts_0 = measure_state(qc_0)
    print("Measurement results for |0⟩ state:", counts_0)
    plot_measurement_distribution(counts_0, "|0⟩ State Measurement Distribution")

    # 2️⃣ Measuring the |1⟩ state
    qc_1 = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit
    qc_1.x(0)  # Apply X gate to flip the state to |1⟩
    qc_1.measure(0, 0)  # Measure the qubit and store the result in the classical bit
    counts_1 = measure_state(qc_1)
    print("Measurement results for |1⟩ state:", counts_1)
    plot_measurement_distribution(counts_1, "|1⟩ State Measurement Distribution")

# Run the visualization script
create_visualization_script()
