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
      - Run the circuit with shots=num_bits.
      - Combine the measurement counts into a bitstring (order is not preserved).
      
    Input:
      num_bits (int): Number of bits to generate.
      
    Returns:
      bitstring (str): A string containing the generated '0's and '1's.
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)        # Apply Hadamard gate.
    qc.measure(0, 0)

    simulator = AerSimulator()
    job = simulator.run(qc, shots=num_bits)
    result = job.result()
    counts = result.get_counts(qc)

    # Build the bitstring by concatenating counts (order is not preserved)
    bitstring = "0" * counts.get('0', 0) + "1" * counts.get('1', 0)
    return bitstring

def main():
    """
    Main function for Task 07.01: Basic Interface.
    This function calls the Quantum RNG with parameters and prints the result.
    """
    # Set the number of bits to generate (this parameter can be adjusted)
    num_bits = 1024
    
    print(f"Calling Quantum RNG with num_bits = {num_bits}\n")
    qrng_output = generate_quantum_random_bitstring(num_bits)
    
    print(f"Generated {num_bits} bits:")
    print(qrng_output)

if __name__ == "__main__":
    main()
