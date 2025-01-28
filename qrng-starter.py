from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

number_of_qbits = 4  # 큐비트 수
qc = QuantumCircuit(number_of_qbits)

# Hadamard 게이트로 중첩 상태 생성
for i in range(number_of_qbits):
    qc.h(i)

qc.measure_all()  # 측정

simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()

counts = result.get_counts()
quantum_bin = list(counts.keys())[0]  # 랜덤 비트 결과
print("Quantum RNG Binary Result:", quantum_bin)
