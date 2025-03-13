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
    Converts a measurement result into its binary string representation with a fixed length.

    If 'measurement' is an integer, returns a binary string padded with zeros.
    If 'measurement' is a dictionary (counts), returns a dictionary with keys zero-padded.
    """
    if isinstance(measurement, int):
        return format(measurement, f"0{num_qubits}b")
    elif isinstance(measurement, dict):
        return {key.zfill(num_qubits): count for key, count in measurement.items()}
    else:
        raise TypeError("Measurement must be an int or dict.")

# Function to convert measurement results into decimal numbers.
def convert_to_decimal(measurement, num_qubits):
    """
    Converts a measurement result (integer or dictionary) into its decimal representation.
    
    For dictionaries, each binary key is converted to an integer.
    """
    if isinstance(measurement, int):
        binary_str = format(measurement, f"0{num_qubits}b")
        return int(binary_str, 2)
    elif isinstance(measurement, dict):
        return {int(key, 2): count for key, count in measurement.items()}
    else:
        raise TypeError("Measurement must be an int or dict.")

# New Function: Convert measurement results into numbers mapped to a specified range.
def convert_to_range(measurement, num_qubits, min_val, max_val):
    """
    Converts a measurement result (integer or dictionary) into a number (or numbers) mapped to the specified range [min_val, max_val].

    The measurement is first interpreted as a decimal number in the range [0, 2^num_qubits - 1].
    It then scales the value to the target range using the transformation:
    
         mapped_value = min_val + (decimal_value / (2^num_qubits - 1)) * (max_val - min_val)
    
    The result is rounded to the nearest integer.
    
    If 'measurement' is an integer, returns a single mapped value.
    If 'measurement' is a dictionary, returns a dictionary with mapped keys.
    """
    max_possible = 2 ** num_qubits - 1
    if isinstance(measurement, int):
        decimal_value = int(format(measurement, f"0{num_qubits}b"), 2)
        mapped_value = round(min_val + (decimal_value / max_possible) * (max_val - min_val))
        return mapped_value
    elif isinstance(measurement, dict):
        mapped_dict = {}
        for binary_key, count in measurement.items():
            decimal_value = int(binary_key, 2)
            mapped_value = round(min_val + (decimal_value / max_possible) * (max_val - min_val))
            mapped_dict[mapped_value] = count
        return mapped_dict
    else:
        raise TypeError("Measurement must be an int or dict.")

# Main demonstration of binary, decimal, and range mapping conversions.
if __name__ == "__main__":
    simulator = AerSimulator()

    # Example: Create a 4-qubit circuit with Hadamard gates to generate a superposition state.
    num_qubits = 4
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))  # Creating a superposition over all qubits
    qc.measure(range(num_qubits), range(num_qubits))

    # Run the circuit multiple times to collect measurement results.
    counts_list = run_circuit_multiple_times(qc, simulator)

    # Define the target range for mapping, for example, numbers from 10 to 20.
    target_min = 10
    target_max = 20

    # For each run, convert and print the results in binary, decimal,
    # and with the numbers mapped to the specified range.
    for run_number, counts in enumerate(counts_list, start=1):
        binary_counts = convert_to_binary_string(counts, num_qubits)
        decimal_counts = convert_to_decimal(counts, num_qubits)
        range_counts = convert_to_range(counts, num_qubits, target_min, target_max)
        print(f"Run {run_number} binary measurement results: {binary_counts}")
        print(f"Run {run_number} decimal measurement results: {decimal_counts}")
        print(f"Run {run_number} mapped measurement results (range {target_min}-{target_max}): {range_counts}")
