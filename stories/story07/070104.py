import math
import random
import sys
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_quantum_random_bitstring(num_bits):
    """
    Generates a quantum random bitstring using Qiskit's AerSimulator.
    
    Process:
      - Creates a 1-qubit circuit with 1 classical bit.
      - Applies a Hadamard gate to place the qubit into equal superposition.
      - Measures the qubit.
      - Runs the circuit with shots=num_bits.
      - Combines the measurement counts into a bitstring.
        (Note: The original order of individual measurements is not preserved.)
    
    Input:
      num_bits (int): Number of bits (shots) to generate.
      
    Returns:
      str: Generated bitstring, or None if an error occurs.
      
    Example:
      >>> bitstring = generate_quantum_random_bitstring(16)
      >>> print("Quantum Bitstring:", bitstring) 
    """
    try:
        qc = QuantumCircuit(1, 1)
        qc.h(0)          # Apply Hadamard gate.
        qc.measure(0, 0) # Measure the qubit.

        simulator = AerSimulator()
        job = simulator.run(qc, shots=num_bits)
        result = job.result()
        counts = result.get_counts(qc)

        # Build bitstring from counts (note: order is lost)
        bitstring = "0" * counts.get('0', 0) + "1" * counts.get('1', 0)
        return bitstring
    except Exception as e:
        print("Error generating quantum random bitstring:", e)
        return None

def generate_classical_random_bitstring(num_bits):
    """
    Generates a classical random bitstring using Python's random module.
    
    Input:
      num_bits (int): Number of bits to generate.
      
    Returns:
      str: Generated bitstring, or None if an error occurs.
      
    Example:
      >>> bitstring = generate_classical_random_bitstring(16)
      >>> print("Classical Bitstring:", bitstring)
    """
    try:
        return ''.join(random.choice("01") for _ in range(num_bits))
    except Exception as e:
        print("Error generating classical random bitstring:", e)
        return None

def frequency_test(bitstring):
    """
    Performs the Frequency (monobit) test on a given bitstring.
    
    Process:
      - Counts the number of '0's and '1's.
      - Computes the normalized difference.
      - Calculates the p-value via the complementary error function.
    
    Input:
      bitstring (str): A string of '0's and '1's.
      
    Returns:
      float: p-value indicating randomness, or None if an error occurs.
      
    Example:
      >>> p_val = frequency_test("01010101")
      >>> print("Frequency test p-value:", p_val)
    """
    try:
        n = len(bitstring)
        if n == 0:
            raise ValueError("The bitstring is empty.")
    
        ones = bitstring.count("1")
        zeros = bitstring.count("0")
        s = ones - zeros
        s_obs = abs(s) / math.sqrt(n)
        p_value = math.erfc(s_obs / math.sqrt(2))
        return p_value
    except Exception as e:
        print("Error performing frequency test:", e)
        return None

def usage_examples():
    """
    Demonstrates usage examples for the Quantum and Classical RNG functions.
    
    Examples:
      1. Generate a 16-bit quantum random bitstring and run a frequency test.
      2. Generate a 16-bit classical random bitstring.
      
    These examples illustrate how to call the functions with parameters and handle their output.
    """
    print("=" * 50)
    print("USAGE EXAMPLES")
    print("=" * 50)

    # Example 1: Quantum RNG and frequency test
    print("\nExample 1: Quantum RNG (16 bits)")
    demo_qrng = generate_quantum_random_bitstring(16)
    if demo_qrng is not None:
        print("Quantum Bitstring:", demo_qrng)
        p_val_q = frequency_test(demo_qrng)
        print("Frequency Test p-value (Quantum RNG):", p_val_q)
    else:
        print("Quantum RNG example failed.")

    # Example 2: Classical RNG
    print("\nExample 2: Classical RNG (16 bits)")
    demo_crng = generate_classical_random_bitstring(16)
    if demo_crng is not None:
        print("Classical Bitstring:", demo_crng)
    else:
        print("Classical RNG example failed.")
        
    print("=" * 50)
    print("END OF USAGE EXAMPLES")
    print("=" * 50)

def main():
    """
    Main function for the basic interface.
    
    This function:
      - Prompts the user for the number of bits to generate.
      - Validates that the input is a positive integer.
      - Calls both Quantum RNG and Classical RNG generators.
      - Performs the frequency test (for the quantum RNG output).
      - Provides clear error messages upon failure.
      
    Usage:
      Run this module directly and follow the prompts.
    """
    # Input validation: prompt until a valid positive integer is entered.
    while True:
        user_input = input("Enter the number of bits to generate (positive integer): ")
        try:
            num_bits = int(user_input)
            if num_bits < 1:
                print("Error: Please enter a positive integer greater than zero.")
            else:
                break
        except ValueError:
            print("Error: Invalid input. Please enter a valid integer.")

    # Quantum RNG section
    try:
        print(f"\nCalling Quantum RNG with num_bits = {num_bits}...")
        qrng_output = generate_quantum_random_bitstring(num_bits)
        if qrng_output is None:
            raise Exception("Quantum RNG failed to generate a bitstring.")
        print(f"\nGenerated {num_bits} quantum bits:")
        print(qrng_output)
    except Exception as e:
        print("Quantum RNG Error:", e)

    # Classical RNG section
    try:
        print(f"\nCalling Classical RNG with num_bits = {num_bits}...")
        crng_output = generate_classical_random_bitstring(num_bits)
        if crng_output is None:
            raise Exception("Classical RNG failed to generate a bitstring.")
        print(f"\nGenerated {num_bits} classical bits:")
        print(crng_output)
    except Exception as e:
        print("Classical RNG Error:", e)

    # Frequency test on Quantum RNG output
    try:
        print("\nPerforming Frequency Test on Quantum RNG output...")
        freq_p = frequency_test(qrng_output)
        if freq_p is None:
            print("Frequency test could not be completed for quantum RNG output.")
        else:
            print(f"Frequency Test p-value (Quantum RNG): {freq_p:.4f}")
    except Exception as e:
        print("Error in Frequency Test for quantum RNG:", e)

if __name__ == "__main__":
    # If the script is run with the command-line argument "example",
    # execute the usage_examples function; otherwise, run main().
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("example", "examples"):
        usage_examples()
    else:
        main()
