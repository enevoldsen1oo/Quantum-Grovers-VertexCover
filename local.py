from qiskit import qasm3
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator, SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeOslo
from matplotlib import pyplot as plt
import numpy as np

# Run every time you need the service
backend = FakeOslo()

# Create a new circuit with two qubits and compile
qc = qasm3.load("grov_gen.qasm")
num_qubits = qc.num_qubits

observables_labels = [
    f'{"".join('I' for _ in range(num_qubits-1))}Z', 
    f'{"".join('I' for _ in range(num_qubits-1))}X',
    f'Z{"".join('I' for _ in range(num_qubits-1))}', 
    f'X{"".join('I' for _ in range(num_qubits-1))}', 
    f'{"".join('Z' for _ in range(num_qubits))}', 
    f'{"".join('X' for _ in range(num_qubits))}']
observables = [SparsePauliOp(label) for label in observables_labels]

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
fig = isa_circuit.draw("mpl")
fig.savefig("./img/splash.png")
plt.close(fig)
#
#param_values = np.random.rand(qc.num_parameters)
#est = Estimator(mode=backend)
#est.options.default_shots = 1000
#
#mapped_observables = [
#    observable.apply_layout(isa_circuit.layout) for observable in observables
#]
#
#job = sampler.run([(isa_circuit, param_values)])
#print(f">>> Job ID: {job.job_id()}")
#print(f">>> Job Status: {job.status()}")
#
#result = job.result()
# 
## Get results for the first (and only) PUB
#pub_result = result[0]
#counts = pub_result.data.c.get_counts()  # {'0101': 42, '1010': 58, ...}
#
#plt.figure(figsize=(10, 5))
#plt.bar(counts.keys(), counts.values())
#plt.xlabel("Bitstring")
#plt.ylabel("Counts")
#plt.title("Grover's Algorithm Measurement Results")
#plt.xticks(rotation=45, ha='right')
#plt.tight_layout()
#plt.savefig("./img/local_res.png")
