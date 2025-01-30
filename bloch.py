from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_vector
 
number_of_qbits = 1  # number of quantum bits

# Create a quantum circuit with 1 qubit
qc = QuantumCircuit(number_of_qbits)

# Create the initial state |0⟩ (no need for gate as it's the default state)
initial_state = qc.initialize([1, 0], 0)  # |0⟩ state

# Use the AerSimulator to run the circuit
simulator = AerSimulator()

# Plot the Bloch sphere for the initial state |0⟩
bloch = plot_bloch_vector([0,1,0], title="New Bloch Sphere")
bloch.savefig('new_bloch.png')
