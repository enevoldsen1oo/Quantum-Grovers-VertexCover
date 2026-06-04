from matplotlib import pyplot as plt
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit.circuit.library import C3XGate, MCXGate
from qiskit.visualization import plot_histogram
from math import sqrt, pi, floor, comb
import qiskit.qasm3

ancilla = QuantumRegister(1, 'anc')
counter = QuantumRegister(3, 'cnt')
vertex  = QuantumRegister(3, 'v')
edge    = QuantumRegister(3, 'e')
solution = QuantumRegister(1, 'sol')
classical = ClassicalRegister(3, 'c')

qc = QuantumCircuit(ancilla, counter, vertex, edge, solution, classical)

def counter(qc, n):
    qc.cx(n, 0)
    qc.append(C3XGate(), [0, 1, 2, 3])
    qc.ccx(0, 1, 2)
    qc.cx(0, 1)
    qc.cx(n, 0)
    qc.cx(3, 0)
    qc.cx(0, 1)
    qc.ccx(0, 1, 2)
    qc.append(C3XGate(), [0, 1, 2, 3])
    qc.reset(0)

def rev_counter(qc, n):
    qc.reset(0)
    qc.append(C3XGate(), [0, 1, 2, 3])
    qc.ccx(0, 1, 2)
    qc.cx(0, 1)
    qc.cx(3, 0)
    qc.cx(n, 0)
    qc.cx(0, 1)
    qc.ccx(0, 1, 2)
    qc.append(C3XGate(), [0, 1, 2, 3])
    qc.cx(n, 0)


def oracle(qc):
    # Counter pattern for i
    for i in range(4,7):
        counter(qc, i)
    
    qc.barrier()
    #Affected vertexes from e1
    qc.x([4,5,6])

    qc.ccx(5, 6, 7)
    qc.x(7)

    # Affected vertexes from e2
    qc.ccx(4, 6, 8)
    qc.x(8)

    # Affected vertexes from e3
    qc.ccx(4, 5, 9)
    qc.x(9)

    qc.barrier()
    # Phase kickback
    qc.x(1)
    qc.append(MCXGate(5), [1, 2, 7, 8, 9, 10])
    qc.x(1)
    qc.barrier()
    # Reverse system    
    qc.x(9)
    qc.ccx(4, 5, 9)

    qc.x(8)
    qc.ccx(4, 6, 8)

    qc.x(7)
    qc.ccx(5, 6, 7)
    qc.x([4,5,6])

    qc.barrier()
    for i in range(6,3, -1):
        rev_counter(qc, i)


def diffusion(qc):
    qc.barrier()
    qc.h([4, 5, 6])
    qc.x([4, 5, 6])
    qc.ccz(4, 5, 6)
    qc.x([4, 5, 6])
    qc.h([4, 5, 6])
    qc.barrier()

qc.x(10)
qc.h(10)

qc.h([4,5,6])

n = 3 # Num of vertices
k = 2 # Num of used vertices in vertex cover
N = pow(2, n) # number of possible inputs
M = comb(n, k) # over approximate the number of solutions to avoid overshooting the number of iterations
print(f"N: {N}, M: {M}")
# M = 2
iterations = floor(pi / 4 * sqrt(N / M))
print("Iterations: ", iterations)

for i in range(iterations):
    oracle(qc)
    diffusion(qc)

qc.h(10)
qc.x(10)

qc.measure([4,5,6], [0,1,2])

fig = qc.draw('mpl')
fig.savefig('circuit_ver.png', dpi=150, bbox_inches="tight")

#qc = qiskit.qasm3.load("vertex_cover.qasm")

service = QiskitRuntimeService(channel="ibm_quantum_platform")
backend = service.backend("ibm_fez")
#noise_model = NoiseModel.from_backend(backend)
#sim = AerSimulator(noise_model=noise_model)
sim = AerSimulator()

tqc = transpile(qc, backend=sim, optimization_level=3)
job = sim.run(tqc, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)

# Option 1: Save to image file
plot_histogram(counts)
plt.savefig("histogram.png", dpi=150, bbox_inches="tight")
print("Saved to histogram.png")
