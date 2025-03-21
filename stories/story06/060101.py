import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_quantum_random_bitstring(num_bits):
    """
    Generates a quantum random bitstring using Qiskit's AerSimulator.
    
    Process:
      - Create a quantum circuit with 1 qubit and 1 classical bit.
      - Apply a Hadamard gate to put the qubit into an equal superposition state.
      - Measure the qubit.
      - Execute the circuit with shots=num_bits, ensuring we obtain num_bits results.
      - For the frequency test, the sequence order is not important, so we combine
        the counts into a simple string.
    
    Input:
      num_bits (int): The desired number of bits to generate.
      
    Returns:
      bitstring (str): A string of '0's and '1's representing the random bit sequence.
    """
    # Create a quantum circuit with 1 qubit and 1 classical bit.
    qc = QuantumCircuit(1, 1)
    qc.h(0)            # Apply the Hadamard gate to create superposition.
    qc.measure(0, 0)   # Measure the qubit.
    
    # Use the AerSimulator backend to execute the circuit.
    simulator = AerSimulator()
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Example of counts: {'0': count0, '1': count1}
    # Since the frequency test only needs the counts of 0s and 1s, we create the bitstring
    # by repeating '0' and '1' according to their counts.
    bitstring = "0" * counts.get('0', 0) + "1" * counts.get('1', 0)
    return bitstring

def frequency_test(bitstring):
    """
    Conducts the frequency (monobit) test on the given bitstring.
    
    The test:
      - Computes the difference between the number of 1s and 0s.
      - Normalizes the observed sum.
      - Computes the p-value based on the complementary error function.
    
    Input:
      bitstring (str): A string consisting solely of '0's and '1's.
      
    Returns:
      p_value (float): The p-value reflecting the randomness of the bit sequence.
    """
    n = len(bitstring)
    if n == 0:
        raise ValueError("The input bitstring is empty.")
    
    # Count the number of ones and zeros, then calculate the difference.
    ones = bitstring.count('1')
    zeros = bitstring.count('0')
    s = ones - zeros
    
    # Normalize by computing the absolute sum divided by the square root of n.
    s_obs = abs(s) / math.sqrt(n)
    
    # Calculate the p-value using the complementary error function (erfc).
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def main():
    num_bits = 1024  # Number of bits to generate (adjust as needed).
    
    print("Generating quantum random bitstring using Qiskit's AerSimulator...")
    bitstring = generate_quantum_random_bitstring(num_bits)
    
    # Debug: Print the counts of 0s and 1s.
    ones = bitstring.count('1')
    zeros = bitstring.count('0')
    print(f"Generated {num_bits} bits: 1's -> {ones} count, 0's -> {zeros} count")
    
    # Perform the frequency (monobit) test and obtain the p-value.
    p_val = frequency_test(bitstring)
    print(f"Frequency test p-value: {p_val:.4f}")
    
    # Check the randomness against a significance level (e.g., alpha = 0.01).
    alpha = 0.01
    if p_val < alpha:
        print("=> The bitstring is deemed non-random (reject the null hypothesis).")
    else:
        print("=> The bitstring is considered random (fail to reject the null hypothesis).")

if __name__ == "__main__":
    main()