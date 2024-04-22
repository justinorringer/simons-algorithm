import os
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2 as Estimator
from qiskit.visualization import plot_histogram

import config as cfg
import utils

# Largely used the tutorial hello world example from Qiskit
# https://docs.quantum.ibm.com/start/hello-world
#
# Changes to run quickly:
# - Lowered the number of shots to 100
#
# Ran in 4 seconds, estimator stated 1.5 minutes
# "hallmark of quantum entanglement"

qr = QuantumRegister(2)
cr = ClassicalRegister(2)
# Create a new circuit with two qubits
qc = QuantumCircuit(qr, cr)

# Add a Hadamard gate to qubit 0
qc.h(0)
 
# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(qr[0], qr[1])

qc.measure(qr, cr)

# Return a drawing of the circuit using MatPlotLib ("mpl"). This is the
# last line of the cell, so the drawing appears in the cell output.
# Remove the "mpl" argument to get a text drawing.
figure1 = qc.draw("mpl", cregbundle=False, initial_state=True)

# Save the figure to a file
figure1.savefig("circuits/hello_circuit_basic.png")
print("Circuit saved to 'circuits/hello_circuit.png'")

# Set up six different observables.
observables_labels = ["ZZ", "ZI", "IZ", "XX", "XI"]
observables = [SparsePauliOp(label) for label in observables_labels]

service = utils.get_service()

if cfg.MOCK:
    _, counts = utils.mock(qc)

    utils.save_mock_counts(counts)
    exit(0)

service = utils.get_service()

# Run on the least-busy backend you have access to
backend = service.least_busy(simulator=False, operational=True)

# Convert to an ISA circuit and layout-mapped observables.
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
 
figure2 = isa_circuit.draw('mpl', idle_wires=False)
figure2.savefig("circuits/hello_circuit_optimized.png")
print("Optimized circuit saved to 'circuits/hello_circuit_optimized.png'")

# Construct the Estimator instance we want to use.

estimator = Estimator(backend)
estimator.options.resilience_level = 1
estimator.options.default_shots = 100
 
observables = [
    observable.apply_layout(isa_circuit.layout) for observable in observables
]
 
# One pub, with one circuit to run against five different observables.
job = estimator.run([(isa_circuit, observables)])
 
# This is the result of the entire submission.  We submitted one Pub,
# so this contains one inner result (and some metadata of its own).
job_result = job.result()
 
# This is the result from our single pub, which had five observables,
# so contains information on all five.
pub_result = job.result()[0]

# print the job id
print("JOB ID:", job.id)
