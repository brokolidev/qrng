import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_quantum_random_bitstring(num_bits):
    """
    Generates a quantum random bitstring using Qiskit's AerSimulator.
    
    Process:
      - Create a quantum circuit with 1 qubit and 1 classical bit.
      - Apply a Hadamard gate to produce an equal superposition.
      - Measure the qubit.
      - Execute the circuit with shots=num_bits.
      - Construct a bitstring by combining the counts of '0's and '1's.
        (Note: The original order of measurements is not preserved.)
      
    Input:
      num_bits (int): Number of bits/shots to generate.
      
    Returns:
      str: The generated bitstring.
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)        # Apply Hadamard gate.
    qc.measure(0, 0)

    simulator = AerSimulator()
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)

    # Build bitstring from measurement counts (order is lost)
    return "0" * counts.get('0', 0) + "1" * counts.get('1', 0)

def main():
    """
    Main function for Task 07.01: Basic Interface.
    
    This function:
      - Prompts the user to enter the number of bits to generate.
      - Validates the input for a positive integer.
      - Calls the QRNG with the valid parameter.
      - Prints the generated bitstring.
    """
    # Prompt the user until a valid input is provided.
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

    print(f"\nCalling Quantum RNG with num_bits = {num_bits}...\n")
    qrng_output = generate_quantum_random_bitstring(num_bits)
    
    print(f"Generated {num_bits} bits:")
    print(qrng_output)

if __name__ == "__main__":
    main()
