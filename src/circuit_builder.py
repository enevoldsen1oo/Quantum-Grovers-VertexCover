from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
import math

class VCPQuantumCircuitBuilder:
    def __init__(self, k: int, vertices: list[int], edges: list[tuple[int, int]]):
        self.k = k
        self.vertices = vertices
        self.edges = edges

        self.num_vertices = len(vertices)
        self.num_edges = len(edges)
        self.num_counting_qubits = len(bin(self.num_vertices)[2:])

        self.num_qubits = (
            self.num_vertices + self.num_counting_qubits + self.num_edges + 1
        )  # value qubits + ancilla + counting qubits + edge qubits + phase kickback qubit
        self.iterations = self.calc_iterations(self.num_vertices, k)

    @staticmethod
    def calc_iterations(n, k) -> int:
        N = math.pow(2, n)
        M = math.comb(
            n, k
        )  # over approximate the number of solutions to avoid overshooting the number of iterations
        iterations = math.pi / 4 * math.sqrt(N / M)
        iterations_accurate = math.pi / (4 * math.acos(math.sqrt((N-M)/N))) - 0.5 # use this instead for more accurate number of iterations
        
        
        print(f"N: {N}, M: {M}, iterations: {iterations}, iterations_accurate: {iterations_accurate}")

        return math.floor(
            iterations + 0.5
        )  # add 0.5 to round to nearest int instead of flooring

    def decrement(self, qc: QuantumCircuit, control: int):
        counting_qbits = list(
            range(self.num_vertices, self.num_vertices + self.num_counting_qubits)
        )
        for i in range(len(counting_qbits)):
            qc.append(MCXGate(i + 1), [control] + counting_qbits[: i + 1])

    def increment(self, qc: QuantumCircuit, control: int):
        counting_qbits = list(
            range(self.num_vertices, self.num_vertices + self.num_counting_qubits)
        )
        for i in range(len(counting_qbits)):
            qc.append(
                MCXGate(len(counting_qbits) - i),
                [control] + counting_qbits[: len(counting_qbits) - i],
            )

    def count_constraint(self, qc: QuantumCircuit):
        for i in range(self.num_vertices):
            self.increment(qc, i)

    def reset_counting_qubits(self, qc: QuantumCircuit):
        for i in range(self.num_vertices)[::-1]:
            self.decrement(qc, i)

    def edge_constraint(self, qc: QuantumCircuit):
        vertecies = set()
        for v1, v2 in self.edges:
            qv1 = self.vertices.index(v1)
            qv2 = self.vertices.index(v2)
            vertecies.add(qv1)
            vertecies.add(qv2)

        # set all connected vertecies to 1, so that the counting qubits are only incremented if the edge is not covered
        for v in vertecies:
            qc.x(v)

        for i, (v1, v2) in enumerate(self.edges):
            edge_qubit = self.num_vertices + self.num_counting_qubits + i
            qv1 = self.vertices.index(v1)
            qv2 = self.vertices.index(v2)
            qc.ccx(qv1, qv2, edge_qubit)
            qc.x(edge_qubit)

    def reset_edge_qubits(self, qc: QuantumCircuit):
        for i, (v1, v2) in list(enumerate(self.edges))[::-1]:
            qv1 = self.vertices.index(v1)
            qv2 = self.vertices.index(v2)
            qc.ccx(qv1, qv2, self.num_vertices + self.num_counting_qubits + i)
            qc.x(self.num_vertices + self.num_counting_qubits + i)

        # reset all connected vertecies back to 0
        vertecies = set()
        for v1, v2 in self.edges:
            qv1 = self.vertices.index(v1)
            qv2 = self.vertices.index(v2)
            vertecies.add(qv1)
            vertecies.add(qv2)

        for v in vertecies:
            qc.x(v)

    def phase_kickback(self, qc: QuantumCircuit):
        target_count_bits = bin(
            self.k
        )[
            2:
        ][
            ::-1
        ]  # get binary representation of k and reverse it to match the order of counting qubits
        target_count_bits += "0" * (
            self.num_counting_qubits - len(target_count_bits)
        )  # pad

        flip_qubits = [
            i + self.num_vertices
            for i, bit in enumerate(target_count_bits)
            if bit == "0"
        ]
        for qubit in flip_qubits:
            qc.x(qubit)

        num_control_qubits = self.num_counting_qubits + self.num_edges
        control_qubits = list(
            range(self.num_qubits - num_control_qubits - 1, self.num_qubits - 1)
        )  # counting qubits + edge qubits
        qc.append(MCXGate(num_control_qubits), control_qubits + [self.num_qubits - 1])

        # reset flipped qubits
        for qubit in flip_qubits:
            qc.x(qubit)

    def oracle(self, qc: QuantumCircuit):
        self.count_constraint(qc)
        self.edge_constraint(qc)
        self.phase_kickback(qc)
        self.reset_edge_qubits(qc)
        self.reset_counting_qubits(qc)

    def diffusion(self, qc: QuantumCircuit):
        for i in range(self.num_vertices):
            qc.h(i)
            qc.x(i)

        qc.h(self.num_vertices - 1)
        vertex_qubits = list(range(self.num_vertices))
        qc.append(MCXGate(self.num_vertices - 1), vertex_qubits)
        qc.h(self.num_vertices - 1)

        for i in range(self.num_vertices):
            qc.x(i)
            qc.h(i)

    def build(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.num_qubits, self.num_vertices)
        qc.h(range(self.num_vertices))  # Place input registers into superposition

        # Prepare phase kickback qubit
        qc.x(self.num_qubits - 1)
        qc.h(self.num_qubits - 1)

        print(f"Number of iterations: {self.iterations}")
        for _ in range(self.iterations):
            self.oracle(qc)
            self.diffusion(qc)

        measure_qubits = list(range(self.num_vertices))
        qc.measure(measure_qubits, measure_qubits)
        return qc


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from qiskit import transpile
    from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel
    from qiskit.visualization import plot_histogram
    from qiskit_ibm_runtime.fake_provider import FakeFez


    # builder = VCPQuantumCircuitBuilder(k=2, vertices=[0,1,2], edges=[(0,1), (0,2), (1,2)])
    # builder = VCPQuantumCircuitBuilder(k=1, vertices=[0, 1, 2], edges=[(0, 1), (1, 2)])
    builder = VCPQuantumCircuitBuilder(k=2, vertices=[1, 2, 3, 4], edges=[(1, 2), (1, 3), (2, 3), (2, 4)])
    qc = builder.build()

    print(qc)

    # QiskitRuntimeService.save_account(
    #     channel="ibm_quantum_platform",
    #     token=ibm_token,
    #     instance=crn,
    #     overwrite=True,
    # )
    # service = QiskitRuntimeService(channel="ibm_quantum_platform")
    # backend = service.backend("ibm_marrakesh")

    backend = FakeFez()
    noise_model = NoiseModel.from_backend(backend)
    # sim = AerSimulator(noise_model=noise_model)
    sim = AerSimulator()

    tqc = transpile(
        qc,
        backend=backend,
        optimization_level=3,
        seed_transpiler=42,  # transpiler i stochastic, so we set the seed to ensure compiled circuit is always the same
    )

    print("Original circuit size: " + str(qc.size()))
    print("Original circuit depth: " + str(qc.depth()))
    print("Transpiled circuit size: " + str(tqc.size()))
    print("Transpiled circuit depth: " + str(tqc.depth()))

    job = sim.run(tqc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(counts)

    # sampler = SamplerV2(backend)
    # job = sampler.run([tqc], shots=1000)
    # res = job.result()
    # counts = res[0].data.c.get_counts()

    # Option 1: Save to image file
    plot_histogram(counts)
    plt.savefig("histogram.svg", dpi=150, bbox_inches="tight")
    print("Saved to histogram.svg")
