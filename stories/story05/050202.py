from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import math

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
            mapped_dict[mapped_value] = mapped_dict.get(mapped_value, 0) + count
        return mapped_dict
    else:
        raise TypeError("Measurement must be an int or dict.")

def validate_range(mapped_measurement, min_val, max_val):
    """
    Validates that the mapped measurement (integer or dictionary keys) are within the specified range [min_val, max_val].
    
    If the mapped measurement is an integer, raises a ValueError if it is out of range.
    If it is a dictionary, checks every key (which represents a mapped measurement value) 
    and raises a ValueError if any key falls outside the allowed range.
    Returns True if all values are within bounds.
    """
    if isinstance(mapped_measurement, int):
        if not (min_val <= mapped_measurement <= max_val):
            raise ValueError(f"Mapped measurement {mapped_measurement} out of range [{min_val}, {max_val}].")
    elif isinstance(mapped_measurement, dict):
        for key in mapped_measurement.keys():
            if not (min_val <= key <= max_val):
                raise ValueError(f"Mapped measurement key {key} out of range [{min_val}, {max_val}].")
    else:
        raise TypeError("Mapped measurement must be an int or dict.")
    return True

def test_conversions():
    """
    Tests the conversion functions using various inputs and target ranges.
    Also ensures via validate_range that range mapping is correct.
    Raises an assertion error if any test fails.
    """
    num_qubits = 4

    # Test convert_to_binary_string
    result_bin_int = convert_to_binary_string(5, num_qubits)  # Expected "0101"
    assert result_bin_int == "0101", f"Expected '0101', got {result_bin_int}"

    input_dict1 = {"10": 3, "11": 5}
    result_bin_dict = convert_to_binary_string(input_dict1, num_qubits)
    assert result_bin_dict == {"0010": 3, "0011": 5}, f"Unexpected result: {result_bin_dict}"

    # Test convert_to_decimal
    result_dec_int = convert_to_decimal(5, num_qubits)
    assert result_dec_int == 5, f"Expected 5, got {result_dec_int}"
    
    input_dict2 = {"0101": 7}  # "0101" equals 5 in decimal.
    result_dec_dict = convert_to_decimal(input_dict2, num_qubits)
    assert result_dec_dict == {5: 7}, f"Unexpected result: {result_dec_dict}"

    # Test convert_to_range (using target range 0 to 100)
    result_range_max = convert_to_range(15, num_qubits, 0, 100)
    assert result_range_max == 100, f"Expected 100, got {result_range_max}"
    
    result_range_min = convert_to_range(0, num_qubits, 0, 100)
    assert result_range_min == 0, f"Expected 0, got {result_range_min}"
    
    result_range_mid = convert_to_range(7, num_qubits, 10, 20)
    assert result_range_mid == 15, f"Expected 15, got {result_range_mid}"

    input_dict3 = {"0000": 10, "1111": 5}  # "0000" -> 0 and "1111" -> 15
    result_range_dict = convert_to_range(input_dict3, num_qubits, 0, 50)
    assert result_range_dict == {0: 10, 50: 5}, f"Unexpected result: {result_range_dict}"

    # Validate ranges
    validate_range(result_range_max, 0, 100)
    validate_range(result_range_min, 0, 100)
    validate_range(result_range_mid, 10, 20)
    validate_range(result_range_dict, 0, 50)

    print("All conversion and range validation tests passed!")

# --------------------------
# Distribution Testing Functions
# --------------------------

def get_expected_distribution(num_qubits, min_val, max_val):
    """
    Computes the expected probability distribution for the mapped measurement outcomes.
    Under ideal conditions, each computational basis state (0 to 2^num_qubits - 1)
    appears uniformly, so we compute the mapping for each state and accumulate counts.
    Returns a dictionary of {mapped_value: expected_probability}.
    """
    max_possible = 2 ** num_qubits - 1
    count_dict = {}
    for d in range(0, max_possible + 1):
        mapped_value = round(min_val + (d / max_possible) * (max_val - min_val))
        count_dict[mapped_value] = count_dict.get(mapped_value, 0) + 1
    total_count = sum(count_dict.values())
    expected_distribution = {k: v / total_count for k, v in count_dict.items()}
    return expected_distribution

def test_distribution_uniformity(num_qubits=4, min_val=10, max_val=20, runs=50, shots=1024, tolerance=0.4):
    """
    Tests that the mapped measurement outcomes (aggregated over many runs)
    roughly follow the expected distribution. The expected distribution is derived
    from the ideal uniform behavior of a Hadamard circuit measured on num_qubits.
    
    Parameters:
      - num_qubits: Number of qubits in the circuit.
      - min_val, max_val: Target range for mapping.
      - runs: Number of circuit executions.
      - shots: Number of shots per execution.
      - tolerance: Maximum allowed relative error (fraction) between observed and expected probabilities.
    
    Raises an AssertionError if any mapped value's relative error exceeds the tolerance.
    Prints the observed and expected distributions.
    """
    simulator = AerSimulator()
    
    # Create a 4-qubit circuit with Hadamard gates on all qubits.
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))
    
    # Run the circuit multiple times.
    counts_list = run_circuit_multiple_times(qc, simulator, shots=shots, num_runs=runs)
    
    # Aggregate the mapped measurement counts.
    aggregate_mapped = {}
    for counts in counts_list:
        mapped_counts = convert_to_range(counts, num_qubits, min_val, max_val)
        for key, value in mapped_counts.items():
            aggregate_mapped[key] = aggregate_mapped.get(key, 0) + value
            
    # Total number of shots executed.
    total_shots = shots * runs

    # Compute observed distribution (probabilities).
    observed_distribution = {k: v / total_shots for k, v in aggregate_mapped.items()}
    
    # Get expected distribution based on ideal mapping.
    expected_distribution = get_expected_distribution(num_qubits, min_val, max_val)
    
    print("\nObserved Distribution:")
    for key in sorted(observed_distribution.keys()):
        print(f"  {key}: {observed_distribution[key]:.3f}")
    
    print("\nExpected Distribution (by mapping basis states):")
    for key in sorted(expected_distribution.keys()):
        print(f"  {key}: {expected_distribution[key]:.3f}")
    
    # Compare the observed vs. expected for each key.
    for key, expected_prob in expected_distribution.items():
        observed_prob = observed_distribution.get(key, 0)
        # To avoid division by zero (although expected_prob should be > 0), we do:
        rel_error = abs(observed_prob - expected_prob) / (expected_prob if expected_prob != 0 else 1)
        assert rel_error <= tolerance, (
            f"Relative error for mapped value {key} too high: "
            f"observed {observed_prob:.3f}, expected {expected_prob:.3f}, relative error {rel_error:.2f}"
        )
    
    print("\nDistribution uniformity test passed! The observed distribution is roughly consistent with expectations.")

# --------------------------
# Main Demonstration
# --------------------------

if __name__ == "__main__":
    # First, run conversion and range validation tests.
    test_conversions()

    # Test the distribution uniformity.
    # For a 4-qubit circuit mapping outcomes to the range [10, 20],
    # we expect that the aggregated mapped results roughly follow the expected distribution.
    test_distribution_uniformity(num_qubits=4, min_val=10, max_val=20, runs=50, shots=1024, tolerance=0.4)

    # For a demonstration, run the circuit a few times and print the results.
    simulator = AerSimulator()
    num_qubits = 4
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))
    
    counts_list = run_circuit_multiple_times(qc, simulator)
    target_min = 10
    target_max = 20
    
    for run_number, counts in enumerate(counts_list, start=1):
        binary_counts = convert_to_binary_string(counts, num_qubits)
        decimal_counts = convert_to_decimal(counts, num_qubits)
        range_counts = convert_to_range(counts, num_qubits, target_min, target_max)
        validate_range(range_counts, target_min, target_max)
        
        print(f"\nRun {run_number} results:")
        print(f" - Binary: {binary_counts}")
        print(f" - Decimal: {decimal_counts}")
        print(f" - Mapped to range [{target_min}, {target_max}]: {range_counts}")
