from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --------------------------
# Conversion and Circuit Functions
# --------------------------

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

def create_quantum_circuit(n, initial_state):
    """
    Creates a quantum circuit with n qubits.
    The qubits are initialized based on the provided binary string 
    (e.g., "000" or "101") and then measured.
    """
    qc = QuantumCircuit(n, n)
    for i, bit in enumerate(initial_state):
        if bit == '1':
            qc.x(i)  # Apply X gate to set qubit i to state |1>
    qc.measure(range(n), range(n))
    return qc

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

def convert_to_decimal(measurement, num_qubits):
    """
    Converts a measurement result (integer or dictionary) into its decimal representation.
    
    For an integer, it first pads the binary representation and then converts it to decimal.
    For a dictionary, each binary key is converted to an integer.
    """
    if isinstance(measurement, int):
        binary_str = format(measurement, f"0{num_qubits}b")
        return int(binary_str, 2)
    elif isinstance(measurement, dict):
        return {int(key, 2): count for key, count in measurement.items()}
    else:
        raise TypeError("Measurement must be an int or dict.")

def convert_to_range(measurement, num_qubits, min_val, max_val):
    """
    Maps the measurement result to a specified target range [min_val, max_val].

    The measurement is first interpreted as a decimal number in the range [0, 2^num_qubits - 1].
    It then scales the value linearly using the transformation:
    
         mapped_value = min_val + (decimal_value / (2^num_qubits - 1)) * (max_val - min_val)
    
    For integers, returns a single mapped value (rounded to the nearest integer).
    For dictionaries, returns a dictionary with mapped keys.
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

# --------------------------
# Testing the Conversion Functions
# --------------------------

def test_conversions():
    """
    Tests the conversion functions using various inputs and target ranges.
    Raises an assertion error if any test fails.
    """
    num_qubits = 4

    # --- Test convert_to_binary_string ---
    # For integer input:
    result_bin_int = convert_to_binary_string(5, num_qubits)  # 5 in 4-bit is "0101"
    expected_bin_int = "0101"
    assert result_bin_int == expected_bin_int, (
        f"convert_to_binary_string(5, {num_qubits}) should be '{expected_bin_int}', got '{result_bin_int}'"
    )

    # For dictionary input:
    input_dict1 = {"10": 3, "11": 5}
    result_bin_dict = convert_to_binary_string(input_dict1, num_qubits)
    expected_bin_dict = {"0010": 3, "0011": 5}
    assert result_bin_dict == expected_bin_dict, (
        f"Expected convert_to_binary_string({input_dict1}, {num_qubits}) to be {expected_bin_dict}, got {result_bin_dict}"
    )

    # --- Test convert_to_decimal ---
    # For integer input:
    result_dec_int = convert_to_decimal(5, num_qubits)
    expected_dec_int = 5
    assert result_dec_int == expected_dec_int, (
        f"convert_to_decimal(5, {num_qubits}) should be {expected_dec_int}, got {result_dec_int}"
    )
    # For dictionary input:
    input_dict2 = {"0101": 7}  # "0101" in binary equals 5
    result_dec_dict = convert_to_decimal(input_dict2, num_qubits)
    expected_dec_dict = {5: 7}
    assert result_dec_dict == expected_dec_dict, (
        f"Expected convert_to_decimal({input_dict2}, {num_qubits}) to be {expected_dec_dict}, got {result_dec_dict}"
    )

    # --- Test convert_to_range ---
    # For integer input: test lower and upper bounds
    # For measurement 15 ("1111") in 4 qubits and range [0, 100]:
    result_range_max = convert_to_range(15, num_qubits, 0, 100)
    assert result_range_max == 100, (
        f"convert_to_range(15, {num_qubits}, 0, 100) should be 100, got {result_range_max}"
    )
    # For measurement 0 ("0000"):
    result_range_min = convert_to_range(0, num_qubits, 0, 100)
    assert result_range_min == 0, (
        f"convert_to_range(0, {num_qubits}, 0, 100) should be 0, got {result_range_min}"
    )
    # For a mid-value: measurement 7 in range [10, 20]:
    # Calculation: 10 + (7/15)*10 ≈ 10 + 4.67 = 14.67 rounds to 15.
    result_range_mid = convert_to_range(7, num_qubits, 10, 20)
    assert result_range_mid == 15, (
        f"convert_to_range(7, {num_qubits}, 10, 20) should be 15, got {result_range_mid}"
    )
    
    # For dictionary input:
    input_dict3 = {"0000": 10, "1111": 5}  # "0000" -> 0 and "1111" -> 15
    result_range_dict = convert_to_range(input_dict3, num_qubits, 0, 50)
    expected_range_dict = {0: 10, 50: 5}
    assert result_range_dict == expected_range_dict, (
        f"Expected convert_to_range({input_dict3}, {num_qubits}, 0, 50) to be {expected_range_dict}, got {result_range_dict}"
    )

    print("All conversion tests passed!")

# --------------------------
# Main Demonstration with Quantum Circuit
# --------------------------

if __name__ == "__main__":
    # First, run the conversion tests.
    test_conversions()

    # Set up simulator and create a simple 4-qubit circuit.
    simulator = AerSimulator()
    num_qubits = 4
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))  # Apply Hadamard gate to put qubits in superposition
    qc.measure(range(num_qubits), range(num_qubits))

    # Run the circuit multiple times to collect measurement results.
    counts_list = run_circuit_multiple_times(qc, simulator)

    # Define a target range for mapping. For example, numbers from 10 to 20.
    target_min = 10
    target_max = 20

    # For each run, convert and print the results in binary, decimal,
    # and with the results mapped into the specified range.
    for run_number, counts in enumerate(counts_list, start=1):
        binary_counts = convert_to_binary_string(counts, num_qubits)
        decimal_counts = convert_to_decimal(counts, num_qubits)
        range_counts = convert_to_range(counts, num_qubits, target_min, target_max)
        print(f"\nRun {run_number} results:")
        print(f" - Binary: {binary_counts}")
        print(f" - Decimal: {decimal_counts}")
        print(f" - Mapped to range {target_min}-{target_max}: {range_counts}")
