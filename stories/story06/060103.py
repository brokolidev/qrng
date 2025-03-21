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
      - Create a quantum circuit with 1 qubit and 1 classical bit.
      - Apply a Hadamard gate to put the qubit into an equal superposition state.
      - Measure the qubit.
      - Execute the circuit with shots=num_bits, ensuring we obtain num_bits results.
      - Combine the counts into a simple bitstring.
    
    Input:
      num_bits (int): The desired number of bits to generate.
      
    Returns:
      bitstring (str): A string of '0's and '1's representing the generated random bit sequence.
    """
    # Create a quantum circuit with 1 qubit and 1 classical bit.
    qc = QuantumCircuit(1, 1)
    qc.h(0)            # Apply the Hadamard gate to create a superposition.
    qc.measure(0, 0)   # Measure the qubit.
    
    # Execute the circuit using the AerSimulator.
    simulator = AerSimulator()
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Construct the bitstring by concatenating '0's and '1's based on the measurement counts.
    bitstring = "0" * counts.get('0', 0) + "1" * counts.get('1', 0)
    return bitstring

def generate_classical_random_bitstring(num_bits):
    """
    Generates a classical random bitstring of length num_bits using Python's random module.
    
    Input:
      num_bits (int): The desired number of bits to generate.
      
    Returns:
      bitstring (str): A string of '0's and '1's representing the generated random bit sequence.
    """
    # Option 1: Using random.getrandbits ensures we get a fixed-width binary string with leading zeros.
    # return format(random.getrandbits(num_bits), f'0{num_bits}b')
    
    # Option 2: Using random.choice to build the bitstring directly.
    return ''.join(random.choice('01') for _ in range(num_bits))

def frequency_test(bitstring):
    """
    Conducts the frequency (monobit) test on a given bitstring.
    
    Process:
      - Computes the difference between the number of 1's and 0's.
      - Normalizes the observed difference.
      - Computes the p-value using the complementary error function.
    
    Input:
      bitstring (str): A string made up of '0's and '1's.
      
    Returns:
      p_value (float): The p-value reflecting the randomness of the bit sequence.
    """
    n = len(bitstring)
    if n == 0:
        raise ValueError("The input bitstring is empty.")
    
    ones = bitstring.count('1')
    zeros = bitstring.count('0')
    s = ones - zeros
    
    # Normalize the observed difference.
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def detect_patterns(bitstring, min_length=2, max_length=6, significance_level=0.05):
    """
    Detects potential patterns in the bitstring by examining the frequency distribution
    of all overlapping bit patterns of varying lengths using a chi-squared test.
    
    For each pattern length L from min_length to max_length:
      - Slide a window of length L and count occurrences of each pattern.
      - Compute the expected frequency for each pattern when distribution is uniform:
            expected = (n - L + 1) / (2^L),
        where n is the length of the bitstring.
      - Calculate the chi-squared statistic:
            chi2_stat = sum((observed - expected)^2 / expected) for all patterns.
      - With degrees of freedom (df = 2^L - 1), compute the p-value.
      - Flag the distribution as non-uniform if p-value < significance_level.
    
    Input:
      bitstring (str): A string of '0's and '1's.
      min_length (int): Minimum pattern length to examine.
      max_length (int): Maximum pattern length to examine.
      significance_level (float): Threshold for flagging non-uniformity.
      
    Returns:
      results (dict): A dictionary where keys are pattern lengths and values are
                      dictionaries containing:
                        'counts'      : observed frequency counts of patterns,
                        'chi2_stat'   : computed chi-squared statistic,
                        'p_value'     : p-value of the test,
                        'non_random'  : Boolean flag indicating non-uniform distribution.
    """
    n = len(bitstring)
    results = {}
    
    # Iterate over each pattern length L.
    for L in range(min_length, max_length + 1):
        total_windows = n - L + 1  # Number of overlapping windows.
        counts = {}
        for i in range(total_windows):
            pattern = bitstring[i:i+L]
            counts[pattern] = counts.get(pattern, 0) + 1
        
        num_patterns = 2 ** L
        expected = total_windows / num_patterns  # Expected frequency per pattern.
        
        # Compute the chi-squared statistic.
        chi2_stat = 0
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
    Compares Quantum RNG and Classical RNG by generating random bitstrings, 
    applying the frequency test and pattern detection tests.
    
    Input:
      num_bits (int): Number of bits to generate.
      pattern_min_length (int): Minimum pattern length for detection.
      pattern_max_length (int): Maximum pattern length for detection.
      significance_level (float): Significance level for tests.
    
    Returns:
      comparison (dict): Dictionary containing metrics for both RNGs.
    """
    # Generate quantum and classical random bitstrings.
    quantum_bitstring = generate_quantum_random_bitstring(num_bits)
    classical_bitstring = generate_classical_random_bitstring(num_bits)
    
    # Perform frequency tests.
    freq_p_quantum = frequency_test(quantum_bitstring)
    freq_p_classical = frequency_test(classical_bitstring)
    
    # Perform pattern detection tests.
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

def main():
    num_bits = 1024  # Number of bits to generate (adjust as needed).
    
    print("Comparing Quantum RNG and Classical RNG:")
    comparison = compare_rngs(num_bits=num_bits,
                              pattern_min_length=2,
                              pattern_max_length=6,
                              significance_level=0.05)
    
    # Display Quantum RNG results.
    quantum = comparison['quantum']
    print("\n--- Quantum RNG Results ---")
    print(f"Generated {num_bits} bits: 1's -> {quantum['ones_count']}, 0's -> {quantum['zeros_count']}")
    print(f"Frequency test p-value: {quantum['frequency_p_value']:.4f}")
    print("Pattern detection results:")
    for L in range(2, 7):
        res = quantum['pattern_detection'][L]
        print(f"\nPattern Length = {L}")
        print(f"Chi-squared Statistic = {res['chi2_stat']:.4f}")
        print(f"P-value = {res['p_value']:.4f}")
        if res['non_random']:
            print("=> Non-uniform pattern distribution detected (potential non-randomness).")
        else:
            print("=> No significant deviation from uniform distribution detected.")
    
    # Display Classical RNG results.
    classical = comparison['classical']
    print("\n--- Classical RNG Results ---")
    print(f"Generated {num_bits} bits: 1's -> {classical['ones_count']}, 0's -> {classical['zeros_count']}")
    print(f"Frequency test p-value: {classical['frequency_p_value']:.4f}")
    print("Pattern detection results:")
    for L in range(2, 7):
        res = classical['pattern_detection'][L]
        print(f"\nPattern Length = {L}")
        print(f"Chi-squared Statistic = {res['chi2_stat']:.4f}")
        print(f"P-value = {res['p_value']:.4f}")
        if res['non_random']:
            print("=> Non-uniform pattern distribution detected (potential non-randomness).")
        else:
            print("=> No significant deviation from a uniform distribution detected.")
    
if __name__ == "__main__":
    main()