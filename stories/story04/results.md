04.02.01 – Basic Circuit Creation and Measurement: This code creates quantum circuits using a specified initial state (either "000" or "111") for n qubits. Each circuit measures all its qubits, collects the results, and then saves the histogram plots. Meaning: It serves as a fundamental test to ensure that quantum circuits function correctly based on different initial states. The measurement results validate the circuit's behavior and correctness.

04.02.02 – Implement Parallel Gates: In this section, Hadamard gates are applied simultaneously (in parallel) to all qubits to create a superposition state, and then the circuit is measured. The resulting histograms show the distribution of outcomes from the superposition. Meaning: This test demonstrates the ability to apply gates in parallel to all qubits, verifying that all qubits change simultaneously. It shows the effect of parallel gate operations on the quantum circuit's performance and output.

04.02.03 – Add Multi-Qubit Measurement: Here, the circuit is enhanced to perform a multi-qubit measurement by, for example, applying an X gate to the first qubit and Hadamard gates to the remaining qubits, then measuring all qubits simultaneously. This allows for obtaining outputs that are the result of combined qubit states. Meaning: It confirms that multiple qubits can be measured at once, and their combined outputs can generate complex multi-bit results. This section verifies the simultaneous measurement of multiple qubits and the formation of composite outputs.

04.02.04 – Test Multi-Qubit Output: This section creates a circuit with four qubits, applies Hadamard gates to all of them, and then measures the qubits. The measurement output is a multi-bit binary string (e.g., "1010"), which demonstrates that the circuit generates numbers larger than a single bit. Meaning: This test ensures that the quantum circuit can produce multi-bit results by measuring multiple qubits simultaneously. It confirms that the circuit's output provides comprehensive information (more than one bit), which is essential for multi-qubit computations.

Traditional methods of random number generation typically use algorithm-based Pseudo-Random Number Generators (PRNGs). These generators are not considered truly random for the following reasons:

Deterministic Algorithms: PRNGs generate sequences of numbers using mathematical algorithms. Given the same initial seed, they will always reproduce the same sequence, which highlights the deterministic nature of the algorithm.

Predictability: If the structure of the algorithm and the initial seed are known, it becomes possible to predict subsequent numbers in the sequence. Therefore, the true unpredictability (or true randomness) is not guaranteed.

Limitations and Patterns: Most PRNGs have a limited internal state and inherent algorithmic constraints, which can lead to periodic behavior over long sequences. This means that the same pattern may eventually repeat over time.

In contrast, quantum random number generators leverage the inherent probabilistic nature of quantum mechanics, producing outcomes at the time of measurement that are fundamentally unpredictable. As a result, quantum random number generators are considered to provide genuine randomness.

In summary, while traditional methods rely on deterministic algorithms and cannot guarantee absolute randomness, quantum methods exploit the inherent uncertainty present in quantum systems before measurement to achieve true randomness.
