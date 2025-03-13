import warnings
# ignore DeprecationWarning: Instruction.condition
warnings.filterwarnings("ignore", category=DeprecationWarning)

import unittest
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
    For dictionaries, returns a dictionary with mapped keys (accumulating counts if collisions occur).
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
    If it is a dictionary, checks every key and raises a ValueError if any key falls outside the allowed range.
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

def get_expected_distribution(num_qubits, min_val, max_val):
    """
    Computes the expected probability distribution for the mapped measurement outcomes.
    Under ideal conditions, each computational basis state (0 to 2^num_qubits - 1) is equally likely,
    so we compute the mapping for each state and accumulate counts.
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

# --------------------------
# Automated Validation Suite (using unittest)
# --------------------------

class TestConversionFunctions(unittest.TestCase):
    def setUp(self):
        self.num_qubits = 4

    def test_convert_to_binary_string_int(self):
        result = convert_to_binary_string(5, self.num_qubits)  # 5 -> "0101" for 4 qubits
        self.assertEqual(result, "0101")

    def test_convert_to_binary_string_dict(self):
        input_dict = {"10": 3, "11": 5}
        expected = {"0010": 3, "0011": 5}
        self.assertEqual(convert_to_binary_string(input_dict, self.num_qubits), expected)

    def test_convert_to_decimal_int(self):
        result = convert_to_decimal(5, self.num_qubits)
        self.assertEqual(result, 5)

    def test_convert_to_decimal_dict(self):
        input_dict = {"0101": 7}  # "0101" binary equals 5 in decimal.
        expected = {5: 7}
        self.assertEqual(convert_to_decimal(input_dict, self.num_qubits), expected)

    def test_convert_to_range_int(self):
        # For int conversion tests
        self.assertEqual(convert_to_range(15, self.num_qubits, 0, 100), 100)
        self.assertEqual(convert_to_range(0, self.num_qubits, 0, 100), 0)
        # For measurement 7 in target range [10, 20]:
        self.assertEqual(convert_to_range(7, self.num_qubits, 10, 20), 15)

    def test_convert_to_range_dict(self):
        input_dict = {"0000": 10, "1111": 5}  # "0000" -> 0 and "1111" -> 15
        expected = {0: 10, 50: 5}  # For target range [0, 50]
        self.assertEqual(convert_to_range(input_dict, self.num_qubits, 0, 50), expected)

    def test_validate_range_int(self):
        # Valid integer in range
        self.assertTrue(validate_range(15, 10, 20))
        # Out of range should raise ValueError
        with self.assertRaises(ValueError):
            validate_range(25, 10, 20)

    def test_validate_range_dict(self):
        # Valid dictionary
        self.assertTrue(validate_range({15: 7, 10: 3}, 10, 20))
        # Invalid dictionary should raise ValueError
        with self.assertRaises(ValueError):
            validate_range({25: 7, 10: 3}, 10, 20)

class TestDistributionUniformity(unittest.TestCase):
    def test_distribution_uniformity(self):
        """
        Tests that aggregate mapped measurement outcomes (over many runs)
        follow the expected distribution within a specified tolerance.
        """
        num_qubits = 4
        target_min = 10
        target_max = 20
        runs = 50
        shots = 1024
        tolerance = 0.4  # allowed relative error

        simulator = AerSimulator()
        # Create a circuit with Hadamard on all qubits giving uniform superposition.
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.h(range(num_qubits))
        qc.measure(range(num_qubits), range(num_qubits))

        counts_list = run_circuit_multiple_times(qc, simulator, shots=shots, num_runs=runs)

        # Aggregate mapped measurement counts from all runs.
        aggregate_mapped = {}
        for counts in counts_list:
            mapped_counts = convert_to_range(counts, num_qubits, target_min, target_max)
            for key, count in mapped_counts.items():
                aggregate_mapped[key] = aggregate_mapped.get(key, 0) + count

        total_shots = runs * shots
        observed_distribution = {k: v / total_shots for k, v in aggregate_mapped.items()}
        expected_distribution = get_expected_distribution(num_qubits, target_min, target_max)

        # Print distributions for inspection (optional)
        print("\n--- Observed Distribution ---")
        for key in sorted(observed_distribution.keys()):
            print(f"{key}: {observed_distribution[key]:.3f}")
        print("\n--- Expected Distribution ---")
        for key in sorted(expected_distribution.keys()):
            print(f"{key}: {expected_distribution[key]:.3f}")

        # Validate that each mapped value's relative error is within tolerance.
        for key, expected_prob in expected_distribution.items():
            observed_prob = observed_distribution.get(key, 0)
            rel_error = abs(observed_prob - expected_prob) / (expected_prob if expected_prob != 0 else 1)
            self.assertLessEqual(rel_error, tolerance,
                                 f"Relative error for mapped value {key} is too high: "
                                 f"observed {observed_prob:.3f}, expected {expected_prob:.3f}")

# --------------------------
# Run the Validation Suite
# --------------------------

if __name__ == "__main__":
    unittest.main()
