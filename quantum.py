from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_textbook.tools import simon_oracle

import config as cfg
from utils.mock import mock, save_mock_counts
from utils.algebra import sdotx
import utils

# This article was very helpful
# https://medium.com/codex/implementing-simons-algorithm-in-qiskit-9155ce6a9527

s = cfg.SIMON_SECRET
n = cfg.N_BITS

print("Secret string s:" + s)
print("Number of bits n:" + str(n))

# creating two quantum register of ’n’ qubits and 1 classical register of ’n’ qubits
qr1 = QuantumRegister(n)
qr2 = QuantumRegister(n)
cr = ClassicalRegister(n)
qc = QuantumCircuit(qr1, qr2, cr)
# applying H-gate on qubits of first register
qc.h(qr1)
qc.barrier()
# manual attempt at making the oracle
# applying bit wise X-OR from register 1 to register 2 where qubits of first register is 1
# for index, i in enumerate(s):
#     if i == '1':
#         qc.cx(qr1[0], qr2[index])
qc &= simon_oracle(s)
qc.barrier()
# measuring qubits of second register
qc.measure(qr2,cr)
qc.barrier()
# applying H-gate to qubits of first register
qc.h(qr1)
qc.barrier()
qc.measure(qr1,cr)
# measuring qubits of fir
figure1 = qc.draw("mpl", cregbundle=False, initial_state=True)

# Save the figure to a file
figure1.savefig("circuits/simon_sample_circuit_%s.png" % s)
print("Circuit saved to 'circuits/simon_sample_circuit_%s.png'" % s)

if cfg.MOCK:
    # Simulate the quantum circuit
    result, counts = mock(qc)
    save_mock_counts(counts)

    # validate by printing out the dot products
    error = False
    for x in counts.keys():
        dot = sdotx(s, x)
        if dot != 0:
            error = True
        print( '{}.{} = {} (mod 2)'.format(s, x, sdotx(s,x)) )
    
    if error:
        print("Error in dot products")
        exit(1)
    exit(0)

# Set up six different observables.
observables_labels = ["Z" * n * 2, "X" * n * 2, "Y" * n * 2, "I" * n * 2]
observables = [SparsePauliOp(label) for label in observables_labels]

service = utils.get_service()

# Run on the least-busy backend you have access to
backend = service.least_busy(simulator=False, operational=True)

# Convert to an ISA circuit and layout-mapped observables.
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
 
figure2 = isa_circuit.draw('mpl', idle_wires=False)
figure2.savefig("circuits/simon_sample_circuit_optimized_%s.png" % s)
print("Optimized circuit saved to 'circuits/hello_circuit_optimized_%s.png'" % s)

# Construct the Estimator instance we want to use.

estimator = Estimator(backend)
estimator.options.resilience_level = 1
estimator.options.default_shots = 500
 
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
