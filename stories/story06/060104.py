import math
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from itertools import product
from scipy.stats import chi2

def generate_quantum_random_bitstring(num_bits):
    """
    Generates a quantum random bitstring using Qiskit's AerSimulator.
    
    Process:
      - Creates a quantum circuit with 1 qubit and 1 classical bit.
      - Applies a Hadamard gate to produce an equal superposition.
      - Measures the qubit.
      - Runs the circuit with shots=num_bits.
      - Constructs a bitstring by concatenating '0's and '1's based on measurement counts.
      
    Input:
      num_bits (int): Number of bits to generate.
      
    Returns:
      bitstring (str): A string of '0's and '1's.
      
    Note:
      The measurement results' order is not preserved here; the generated bitstring
      is simply '0'*count0 + '1'*count1.
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)            # Create equal superposition.
    qc.measure(0, 0)   # Measure the qubit.
    
    simulator = AerSimulator()
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Construct bitstring from counts; order is lost.
    bitstring = "0" * counts.get('0', 0) + "1" * counts.get('1', 0)
    return bitstring

def generate_classical_random_bitstring(num_bits):
    """
    Generates a classical random bitstring using Python's random module.
    
    Input:
      num_bits (int): Number of bits to generate.
      
    Returns:
      bitstring (str): A string of '0's and '1's.
    """
    return ''.join(random.choice('01') for _ in range(num_bits))

def frequency_test(bitstring):
    """
    Performs the Frequency (monobit) test on the provided bitstring.
    
    The test:
      - Counts the number of 1's and 0's.
      - Calculates the normalized difference.
      - Computes the p-value using the complementary error function.
    
    Input:
      bitstring (str): A string consisting of '0's and '1's.
      
    Returns:
      p_value (float): The p-value indicating the randomness of the bitstring.
    """
    n = len(bitstring)
    if n == 0:
        raise ValueError("The input bitstring is empty.")
        
    ones = bitstring.count('1')
    zeros = bitstring.count('0')
    s = ones - zeros
    s_obs = abs(s) / math.sqrt(n)
    
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def detect_patterns(bitstring, min_length=2, max_length=6, significance_level=0.05):
    """
    Detects potential patterns in the bitstring by performing chi-squared tests on 
    overlapping bit patterns of lengths from min_length to max_length.
    
    For each pattern length L:
      - Slides a window over the bitstring to count occurrences of each L-bit pattern.
      - Calculates the expected frequency assuming a uniform distribution:
            expected = (n - L + 1) / (2^L)
      - Computes the chi-squared statistic:
            chi2_stat = sum((observed - expected)^2 / expected) for all possible patterns.
      - Determines the p-value using the chi-squared survival function with df = 2^L - 1.
      - Flags the distribution as non-uniform if p-value < significance_level.
      
    Input:
      bitstring (str): A string of '0's and '1's.
      min_length (int): Minimum pattern length to test.
      max_length (int): Maximum pattern length to test.
      significance_level (float): Threshold for non-uniformity detection.
      
    Returns:
      results (dict): A dictionary mapping each pattern length L to a dictionary with:
                       'counts', 'chi2_stat', 'p_value', 'non_random'.
    """
    n = len(bitstring)
    results = {}
    
    for L in range(min_length, max_length + 1):
        total_windows = n - L + 1  # Total number of overlapping windows.
        counts = {}
        # Count all L-bit patterns using a sliding window.
        for i in range(total_windows):
            pattern = bitstring[i:i+L]
            counts[pattern] = counts.get(pattern, 0) + 1
        
        num_patterns = 2 ** L               # Total possible patterns.
        expected = total_windows / num_patterns  # Expected frequency per pattern.
        
        chi2_stat = 0
        # Iterate over every possible L-bit pattern.
        for pattern in product('01', repeat=L):
            pattern_str = ''.join(pattern)
            observed = counts.get(pattern_str, 0)
            chi2_stat += ((observed - expected) ** 2) / expected
        
        df = num_patterns - 1  # Degrees of freedom.
        p_value = chi2.sf(chi2_stat, df)
        non_random = p_value < significance_level
        
        results[L] = {
            'counts': counts,
            'chi2_stat': chi2_stat,
            'p_value': p_value,
            'non_random': non_random
        }
    return results

def compare_rngs(num_bits=1024, pattern_min_length=2, pattern_max_length=6, significance_level=0.05):
    """
    Generates random bitstrings from both Quantum RNG and Classical RNG,
    performs Frequency tests and pattern detection tests, and returns the results.
    
    Input:
      num_bits (int): Number of bits to generate.
      pattern_min_length (int): Minimum pattern length for detection.
      pattern_max_length (int): Maximum pattern length for detection.
      significance_level (float): Significance level for statistical tests.
      
    Returns:
      comparison (dict): Results for both 'quantum' and 'classical' RNGs.
    """
    quantum_bitstring = generate_quantum_random_bitstring(num_bits)
    classical_bitstring = generate_classical_random_bitstring(num_bits)
    
    freq_p_quantum = frequency_test(quantum_bitstring)
    freq_p_classical = frequency_test(classical_bitstring)
    
    pattern_results_quantum = detect_patterns(quantum_bitstring,
                                              min_length=pattern_min_length,
                                              max_length=pattern_max_length,
                                              significance_level=significance_level)
    pattern_results_classical = detect_patterns(classical_bitstring,
                                              min_length=pattern_min_length,
                                              max_length=pattern_max_length,
                                              significance_level=significance_level)
    
    comparison = {
        'quantum': {
            'bitstring': quantum_bitstring,
            'ones_count': quantum_bitstring.count('1'),
            'zeros_count': quantum_bitstring.count('0'),
            'frequency_p_value': freq_p_quantum,
            'pattern_detection': pattern_results_quantum
        },
        'classical': {
            'bitstring': classical_bitstring,
            'ones_count': classical_bitstring.count('1'),
            'zeros_count': classical_bitstring.count('0'),
            'frequency_p_value': freq_p_classical,
            'pattern_detection': pattern_results_classical
        }
    }
    return comparison

def document_test_results(num_bits=1024, pattern_min_length=2, pattern_max_length=6, significance_level=0.05):
    """
    Generates a comprehensive, clear report of the statistical properties from both
    Quantum RNG and Classical RNG tests.
    
    The report includes:
      - Total bits generated and counts of 0's and 1's.
      - Frequency test p-value.
      - For each tested pattern length: chi-squared statistic, p-value, and interpretation.
    
    The report is printed to the console.
    """
    comparison = compare_rngs(num_bits, pattern_min_length, pattern_max_length, significance_level)
    
    report_lines = []
    report_lines.append("="*50)
    report_lines.append("STATISTICAL PROPERTIES REPORT")
    report_lines.append("="*50)
    
    # Document Quantum RNG results.
    quantum = comparison['quantum']
    report_lines.append("\n-- Quantum RNG Results --")
    report_lines.append(f"Total Bits Generated  : {num_bits}")
    report_lines.append(f"Count of 1's          : {quantum['ones_count']}")
    report_lines.append(f"Count of 0's          : {quantum['zeros_count']}")
    report_lines.append(f"Frequency Test p-value: {quantum['frequency_p_value']:.4f}")
    
    report_lines.append("\nPattern Detection Results (Quantum RNG):")
    for L in range(pattern_min_length, pattern_max_length + 1):
        res = quantum['pattern_detection'][L]
        report_lines.append(f"\nPattern Length = {L}:")
        report_lines.append(f"  Chi-squared Statistic: {res['chi2_stat']:.4f}")
        report_lines.append(f"  P-value              : {res['p_value']:.4f}")
        if res['non_random']:
            report_lines.append("  --> Non-uniform pattern distribution detected (potential non-randomness).")
        else:
            report_lines.append("  --> Uniform distribution (no significant deviation detected).")
    
    # Document Classical RNG results.
    classical = comparison['classical']
    report_lines.append("\n-- Classical RNG Results --")
    report_lines.append(f"Total Bits Generated  : {num_bits}")
    report_lines.append(f"Count of 1's          : {classical['ones_count']}")
    report_lines.append(f"Count of 0's          : {classical['zeros_count']}")
    report_lines.append(f"Frequency Test p-value: {classical['frequency_p_value']:.4f}")
    
    report_lines.append("\nPattern Detection Results (Classical RNG):")
    for L in range(pattern_min_length, pattern_max_length + 1):
        res = classical['pattern_detection'][L]
        report_lines.append(f"\nPattern Length = {L}:")
        report_lines.append(f"  Chi-squared Statistic: {res['chi2_stat']:.4f}")
        report_lines.append(f"  P-value              : {res['p_value']:.4f}")
        if res['non_random']:
            report_lines.append("  --> Non-uniform pattern distribution detected (potential non-randomness).")
        else:
            report_lines.append("  --> Uniform distribution (no significant deviation detected).")
    
    report_lines.append("="*50)
    report_lines.append("END OF REPORT")
    report_lines.append("="*50)
    
    # Print the full report.
    report = "\n".join(report_lines)
    print(report)
    
def main():
    # 설정: 생성할 비트 수, 패턴 길이 범위, 유의수준
    num_bits = 1024
    pattern_min_length = 2
    pattern_max_length = 6
    significance_level = 0.05
    
    print("Documenting test results for Quantum RNG and Classical RNG.\n")
    document_test_results(num_bits, pattern_min_length, pattern_max_length, significance_level)

if __name__ == "__main__":
    main()