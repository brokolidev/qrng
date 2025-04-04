# Quantum Random Bit Generator

## User Guide

Welcome to the Quantum Random Bit Generator! This guide will help you understand and use all features of this program which combines quantum computing principles with classical methods to generate random bitstrings.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Program Features](#program-features)
4. [Usage Modes](#usage-modes)
5. [Understanding Your Results](#understanding-your-results)
6. [Troubleshooting](#troubleshooting)
7. [Glossary](#glossary)

## Introduction

This program allows you to generate random bitstrings (sequences of 0s and 1s) using two different methods:

- **Quantum Random Number Generation**: Uses quantum computing principles to generate truly random bits
- **Classical Random Number Generation**: Uses traditional computer algorithms to generate pseudo-random bits

It also includes a statistical test to verify the randomness quality of the quantum generation.

## Getting Started

### System Requirements

- Python 3.6 or higher
- Qiskit and Qiskit Aer packages
- Standard Python libraries: math, random, sys

### Installation

1. Ensure Python is installed on your system
2. Install the required Qiskit packages:

```sh
   pip install qiskit qiskit_aer
```

3. Save the program file as `quantum_random.py`

### Running the Program

You can run the program in two different ways:

- **Standard Mode**: `python quantum_random.py`
- **Example Mode**: `python quantum_random.py example`

## Program Features

### 1. Quantum Random Bit Generation

This feature uses quantum computing principles to generate truly random bits:

- Creates a quantum circuit with one qubit
- Places the qubit in a superposition state (using Hadamard gate)
- Measures the qubit multiple times
- Converts measurements into a bitstring

**Why use Quantum Generation?** Quantum randomness is based on fundamental quantum mechanical principles and provides true randomness rather than algorithmic pseudo-randomness.

### 2. Classical Random Bit Generation

This feature uses Python's built-in random module to generate pseudo-random bits:

- Uses Python's random.choice() method
- Selects either '0' or '1' for each bit position
- Combines individual bits into a complete bitstring

**Why use Classical Generation?** It's faster and doesn't require quantum computing resources, suitable for non-critical applications.

### 3. Randomness Quality Testing

The program includes the Frequency (monobit) test to check the randomness quality:

- Counts the occurrences of '0's and '1's
- Calculates statistical p-value
- Higher p-values (closer to 1.0) indicate better randomness
- P-values below 0.01 might suggest non-random patterns

### 4. User Input Handling

The program safely processes user input:

- Validates that input is a positive integer
- Provides clear error messages for invalid inputs
- Continues prompting until valid input is received

## Usage Modes

### Interactive Mode

When you run the program without arguments (`python quantum_random.py`):

1. You'll be prompted to enter the number of bits to generate
2. The program will generate both quantum and classical random bitstrings
3. A statistical test will be performed on the quantum results
4. All results will be displayed in the console

**Example interaction:**

```sh
Enter the number of bits to generate (positive integer): 16

Calling Quantum RNG with num_bits = 16...

Generated 16 quantum bits:
0111010110010011

Calling Classical RNG with num_bits = 16...

Generated 16 classical bits:
1010110001110010

Performing Frequency Test on Quantum RNG output...
Frequency Test p-value (Quantum RNG): 0.6547
```

### Example Mode

When you run the program with the "example" argument (`python quantum_random.py example`):

1. The program will automatically run pre-configured examples
2. It will display the results of generating 16-bit strings
3. No user input is required

This mode is perfect for:

- Learning how the program works
- Testing that your installation is correct
- Seeing expected output formats

## Understanding Your Results

### Reading Bitstrings

The bitstrings are exactly what they look like - sequences of 0s and 1s that represent random binary values.

### Understanding p-values

The p-value from the frequency test indicates the probability that a truly random string would deviate from expected values at least as much as observed.

- p-value > 0.01: The bit sequence is likely random
- p-value < 0.01: The bit sequence may not be random

Note that for very short sequences (under 100 bits), p-values should be interpreted cautiously.

### Comparing Quantum vs. Classical Output

While both methods produce strings of 0s and 1s, there are important differences:

- The quantum-generated bits are based on true quantum randomness
- The classical bits use algorithmic methods and are not truly random

For most casual applications, both will appear equally random.

## Troubleshooting

### Common Issues

#### "Error generating quantum random bitstring"

This usually indicates a problem with the Qiskit installation or simulator access. Try:

- Reinstalling Qiskit: `pip install --upgrade qiskit qiskit_aer`
- Checking your internet connection (if using a remote simulator)
- Reducing the number of bits requested

#### Invalid Input Messages

If you see messages about invalid input:

- Make sure you're entering a positive whole number
- Don't include any letters, spaces or special characters
- Try a smaller number if you get errors with very large values

### Getting Help

If you continue experiencing problems:

- Check the Qiskit documentation: <https://qiskit.org/documentation/>
- Look for error messages that might provide more specific information

## Glossary

- **Bitstring**: A sequence of binary digits (0s and 1s)
- **Quantum Superposition**: A quantum state where a particle exists in multiple states simultaneously
- **Hadamard Gate**: A quantum gate that puts a qubit into superposition
- **p-value**: A statistical measure used to test hypotheses about randomness
- **QRNG**: Quantum Random Number Generator
- **CRNG**: Classical Random Number Generator
- **Frequency Test**: A statistical test that checks if the number of 0s and 1s in a sequence is approximately equal
