import math
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_quantum_random_bitstring(num_bits):
    """
    Generates a quantum random bitstring using Qiskit's AerSimulator.
    
    Process:
      - Create a quantum circuit with 1 qubit and 1 classical bit.
      - Apply a Hadamard gate to produce an equal superposition.
      - Measure the qubit.
      - Run the circuit with shots=num_bits.
      - Build a bitstring by combining the counts of '0's and '1's.
        (Note: the measurement order is not preserved.)
    
    Input:
      num_bits (int): Number of bits to generate.
    
    Returns:
      str: The generated bitstring or None if an error occurred.
    """
    try:
        qc = QuantumCircuit(1, 1)
        qc.h(0)          # Apply Hadamard gate.
        qc.measure(0, 0) # Perform measurement.
    
        simulator = AerSimulator()
        job = simulator.run(qc, shots=num_bits)
        result = job.result()
        counts = result.get_counts(qc)
    
        # Build a bitstring from the measurement counts (order is lost).
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
      str: The generated bitstring or None if an error occurred.
    """
    try:
        return ''.join(random.choice("01") for _ in range(num_bits))
    except Exception as e:
        print("Error generating classical random bitstring:", e)
        return None

def frequency_test(bitstring):
    """
    Performs the Frequency (monobit) test on the given bitstring.
    
    Process:
      - Counts the number of '1's and '0's.
      - Computes the normalized difference.
      - Calculates the p-value via the complementary error function.
    
    Input:
      bitstring (str): A string of '0's and '1's.
      
    Returns:
      float: The p-value from the test or None if an error occurred.
    """
    try:
        n = len(bitstring)
        if n == 0:
            raise ValueError("The bitstring is empty.")
    
        ones = bitstring.count('1')
        zeros = bitstring.count('0')
        s = ones - zeros
    
        s_obs = abs(s) / math.sqrt(n)
        p_value = math.erfc(s_obs / math.sqrt(2))
        return p_value
    except Exception as e:
        print("Error performing frequency test:", e)
        return None

def main():
    """
    Main function for Task 07.01: Basic Interface.
    
    This function:
      - Prompts the user to enter the number of bits to generate.
      - Validates and handles input errors.
      - Calls both Quantum RNG and Classical RNG generators.
      - Performs the frequency test on the generated quantum RNG output.
      - Provides clear error messages for any failures.
    """
    # Prompt the user until a valid positive integer is entered.
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

    # Generate and display Quantum RNG output.
    try:
        print(f"\nCalling Quantum RNG with num_bits = {num_bits}...")
        qrng_output = generate_quantum_random_bitstring(num_bits)
        if qrng_output is None:
            raise Exception("Quantum RNG failed to generate a bitstring.")
        print(f"\nGenerated {num_bits} quantum bits:")
        print(qrng_output)
    except Exception as e:
        print("Quantum RNG Error:", e)

    # Generate and display Classical RNG output.
    try:
        print(f"\nCalling Classical RNG with num_bits = {num_bits}...")
        crng_output = generate_classical_random_bitstring(num_bits)
        if crng_output is None:
            raise Exception("Classical RNG failed to generate a bitstring.")
        print(f"\nGenerated {num_bits} classical bits:")
        print(crng_output)
    except Exception as e:
        print("Classical RNG Error:", e)

    # Perform and display frequency test on Quantum RNG output.
    try:
        print("\nPerforming Frequency Test on quantum RNG output...")
        freq_p = frequency_test(qrng_output)
        if freq_p is None:
            print("Frequency test could not be completed for quantum RNG output.")
        else:
            print(f"Frequency Test p-value (quantum RNG): {freq_p:.4f}")
    except Exception as e:
        print("Error in Frequency Test for quantum RNG:", e)

if __name__ == "__main__":
    main()
