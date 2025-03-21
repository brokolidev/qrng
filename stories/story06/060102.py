import math
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
      - For our tests, combine the counts into a simple bitstring.
    
    Input:
      num_bits (int): The desired number of bits to generate.
      
    Returns:
      bitstring (str): A string of '0's and '1's representing the generated random bit sequence.
    """
    # Create quantum circuit with 1 qubit and 1 classical bit.
    qc = QuantumCircuit(1, 1)
    qc.h(0)            # Apply Hadamard gate to create superposition.
    qc.measure(0, 0)   # Measure the qubit.
    
    # Execute using AerSimulator.
    simulator = AerSimulator()
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Construct a bitstring from the measurement counts.
    bitstring = "0" * counts.get('0', 0) + "1" * counts.get('1', 0)
    return bitstring

def frequency_test(bitstring):
    """
    Conducts the frequency (monobit) test on a given bitstring.

    The test:
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
    
    # Count the number of 1's and 0's.
    ones = bitstring.count('1')
    zeros = bitstring.count('0')
    s = ones - zeros
    
    # Normalize the difference.
    s_obs = abs(s) / math.sqrt(n)
    
    # Compute the p-value using the complementary error function.
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def detect_patterns(bitstring, min_length=2, max_length=6, significance_level=0.05):
    """
    Detects potential patterns in the bitstring by examining the frequency distribution
    of all overlapping bit patterns of varying lengths using a chi-squared test.
    
    For each pattern length L from min_length to max_length:
      - Slide a window of length L and count occurrences of each pattern.
      - Compute the expected frequency assuming a uniform distribution:
            expected = (n - L + 1) / (2^L),
        where n is the total length of the bitstring.
      - Calculate the chi-squared statistic:
            chi2_stat = sum((observed - expected)^2 / expected) over all possible patterns.
      - Set degrees of freedom, df = 2^L - 1.
      - Compute the p-value using the chi-squared survival function.
      - Flag the pattern distribution as non-uniform if p-value < significance_level.
    
    Input:
      bitstring (str): A string consisting solely of '0's and '1's.
      min_length (int): Minimum pattern length to search for.
      max_length (int): Maximum pattern length to search for.
      significance_level (float): The threshold p-value for flagging non-uniform patterns.
    
    Returns:
      results (dict): A dictionary where keys are pattern lengths and values are dictionaries containing:
        - 'counts': The observed frequency counts of patterns.
        - 'chi2_stat': The computed chi-squared statistic.
        - 'p_value': The p-value from the chi-squared test.
        - 'non_random': Boolean flag (True if the pattern distribution is non-uniform at the given significance level).
    """
    n = len(bitstring)
    results = {}
    
    # Iterate over each pattern length L from min_length to max_length.
    for L in range(min_length, max_length + 1):
        # Calculate the number of overlapping windows.
        total_windows = n - L + 1
        
        # Count occurrences of each pattern using a sliding window.
        counts = {}
        for i in range(total_windows):
            pattern = bitstring[i:i+L]
            counts[pattern] = counts.get(pattern, 0) + 1
        
        # Total number of possible patterns for length L is 2^L.
        num_patterns = 2 ** L
        expected = total_windows / num_patterns  # Expected frequency per pattern.
        
        # Compute the chi-squared statistic across all possible patterns.
        chi2_stat = 0
        for pattern in product('01', repeat=L):
            pattern_str = ''.join(pattern)
            observed = counts.get(pattern_str, 0)
            chi2_stat += ((observed - expected) ** 2) / expected
        
        # Degrees of freedom: number of possible patterns minus one.
        df = num_patterns - 1
        
        # Calculate the p-value from the chi-squared statistic.
        p_value = chi2.sf(chi2_stat, df)
        
        # Determine if the pattern distribution deviates significantly from uniformity.
        non_random = p_value < significance_level
        
        results[L] = {
            'counts': counts,
            'chi2_stat': chi2_stat,
            'p_value': p_value,
            'non_random': non_random
        }
    return results

def main():
    num_bits = 1024  # Number of bits to generate (adjust as needed).
    
    print("Generating quantum random bitstring using Qiskit's AerSimulator...")
    bitstring = generate_quantum_random_bitstring(num_bits)
    
    # Display the counts of 0's and 1's in the generated bitstring.
    ones = bitstring.count('1')
    zeros = bitstring.count('0')
    print(f"Generated {num_bits} bits: 1's -> {ones}, 0's -> {zeros}")
    
    # Perform the frequency (monobit) test.
    p_val_frequency = frequency_test(bitstring)
    print(f"Frequency test p-value: {p_val_frequency:.4f}")
    
    alpha = 0.01
    if p_val_frequency < alpha:
        print("=> The bitstring is deemed non-random based on frequency test (reject null hypothesis).")
    else:
        print("=> The bitstring is considered random based on frequency test (fail to reject null hypothesis).")
    
    # Perform pattern detection on the bitstring.
    print("\nPerforming pattern detection...")
    pattern_results = detect_patterns(bitstring, min_length=2, max_length=6, significance_level=0.05)
    
    # Print the pattern detection results for each pattern length.
    for L in range(2, 7):
        res = pattern_results[L]
        print(f"\nPattern Length = {L}")
        print(f"Chi-squared Statistic = {res['chi2_stat']:.4f}")
        print(f"P-value = {res['p_value']:.4f}")
        if res['non_random']:
            print("=> Non-uniform pattern distribution detected (potential non-randomness).")
        else:
            print("=> No significant deviation from a uniform distribution detected.")
    
if __name__ == "__main__":
    main()