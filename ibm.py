from qiskit import qasm3
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator

from matplotlib import pyplot as plt

 
api_key = "5-DjDUnwlHsXPEFJ-4uu9ofpt7xrh1PVO14g_vrMgRAu"
crn = "crn:v1:bluemix:public:quantum-computing:us-east:a/02824615248c41aea6867b90e0495366:92551145-946f-4bed-bd22-871076719f01::"


QiskitRuntimeService.save_account(
    token=api_key, # Use the 44-character API_KEY you created and saved from the IBM Quantum Platform Home dashboard
    instance=crn, # Optional
    overwrite=True
)

# Run every time you need the service
service = QiskitRuntimeService()
backend = service.least_busy(simulator=False, operational=True)

observables_labels = ["IIIZ", "IIIX", "ZIII", "XIII", "ZZZZ", "XXXX"]
observables = [SparsePauliOp(label) for label in observables_labels]


# Create a new circuit with two qubits
qc = qasm3.load("grovers.qasm")

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)


est = Estimator(mode=backend)
est.options.resilience_level = 1
est.options.default_shots = 1000

mapped_observables = [
    observable.apply_layout(isa_circuit.layout) for observable in observables
]

job = est.run([(isa_circuit, mapped_observables)])

print(f">>> Job ID: {job.job_id()}")


# This is the result of the entire submission.  You submitted one Pub,
# so this contains one inner result (and some metadata of its own).
job_result = job.result()
 
# This is the result from our single pub, which had six observables,
# so contains information on all six.
pub_result = job.result()[0]


# Plot the result
 
values = pub_result.data.evs
 
errors = pub_result.data.stds
 
# plotting graph
plt.plot(observables_labels, values, "-o")
plt.xlabel("Observables")
plt.ylabel("Values")
plt.savefig("./img/ibm_res.png")