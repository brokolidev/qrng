from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Function to run a quantum circuit multiple times and return a list of count dictionaries.
def run_circuit_multiple_times(qc, simulator, shots=1024, num_runs=5):
    """
    Runs the quantum circuit multiple times with the specified number of shots.
    Returns a list of measurement count dictionaries.
    """
    all_counts = []
    for _ in range(num_runs):
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=shots).result()
        counts = result.get_counts(qc)
        all_counts.append(counts)
    return all_counts

# Function to create a quantum circuit with n qubits initialized to a given binary state.
def create_quantum_circuit(n, initial_state):
    """
    Creates a quantum circuit with n qubits.
    The qubits are initialized based on the provided binary string 
    (e.g., "000" or "101") and then measured.
    """
    qc = QuantumCircuit(n, n)
    for i, bit in enumerate(initial_state):
        if bit == '1':
            qc.x(i)  # Apply X gate for qubit initialization to state |1>
    qc.measure(range(n), range(n))
    return qc

# Function to convert measurement results into fixed-length binary string representations.
def convert_to_binary_string(measurement, num_qubits):
    """
    Converts a measurement result into its binary string representation with fixed length.

    If 'measurement' is an integer, returns a binary string padded with zeros to match num_qubits.
    If 'measurement' is a dictionary (counts), returns a dictionary with keys zero-padded to num_qubits.
    """
    if isinstance(measurement, int):
        return format(measurement, f"0{num_qubits}b")
    elif isinstance(measurement, dict):
        return {key.zfill(num_qubits): count for key, count in measurement.items()}
    else:
        raise TypeError("Measurement must be an int or dict.")

# New function: convert measurement results from binary to decimal.
def convert_to_decimal(measurement, num_qubits):
    """
    Converts a measurement result into its decimal representation.

    If 'measurement' is an integer, it converts it from its padded binary form to a decimal integer.
    If 'measurement' is a dictionary (counts), it returns a dictionary with keys converted from binary to decimal.
    """
    if isinstance(measurement, int):
        # Convert integer to a padded binary string and then to decimal
        binary_str = format(measurement, f"0{num_qubits}b")
        return int(binary_str, 2)
    elif isinstance(measurement, dict):
        # Convert each key from binary to integer
        return {int(key, 2): count for key, count in measurement.items()}
    else:
        raise TypeError("Measurement must be an int or dict.")

# Main demonstration of both binary and decimal conversion.
if __name__ == "__main__":
    simulator = AerSimulator()

    # Example: Create a 4-qubit circuit with Hadamard gates to generate a superposition state.
    num_qubits = 4
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))  # Apply Hadamard gate in parallel to all qubits
    qc.measure(range(num_qubits), range(num_qubits))

    # Run the circuit multiple times to collect measurement results.
    counts_list = run_circuit_multiple_times(qc, simulator)

    # For each run, convert and print both the binary and decimal representations.
    for run_number, counts in enumerate(counts_list, start=1):
        binary_counts = convert_to_binary_string(counts, num_qubits)
        decimal_counts = convert_to_decimal(counts, num_qubits)
        print(f"Run {run_number} binary measurement results: {binary_counts}")
        print(f"Run {run_number} decimal measurement results: {decimal_counts}")
