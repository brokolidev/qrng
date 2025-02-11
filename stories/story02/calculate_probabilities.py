import numpy as np

# Sample measurements
measurements = [1, 2, 2, 3, 4, 4, 4, 5, 5]

# Calculate the probability distribution
unique, counts = np.unique(measurements, return_counts=True)
probabilities = counts / counts.sum()

# Print the results
for value, prob in zip(unique, probabilities):
    print(f"Value: {value}, Probability: {prob}")
