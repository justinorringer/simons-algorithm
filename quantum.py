from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_textbook.tools import simon_oracle
from qiskit.visualization import plot_histogram

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
qc &= simon_oracle(s)
qc.barrier()
# applying H-gate to qubits of first register
qc.h(qr1)
qc.barrier()
qc.measure(qr1,cr)
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

service = utils.get_service()

# Run on the least-busy backend you have access to
backend = service.least_busy(simulator=False, operational=True)

# Convert to an ISA circuit and layout-mapped observables.
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
 
figure2 = isa_circuit.draw('mpl', idle_wires=False)
figure2.savefig("circuits/simon_sample_circuit_optimized_%s.png" % s)
print("Optimized circuit saved to 'circuits/hello_circuit_optimized_%s.png'" % s)

# using SamplerV2 to measure the bit strings
sampler = Sampler(backend)
sampler.options.dynamical_decoupling.enable = True
sampler.options.dynamical_decoupling.sequence_type = "XY4"
sampler.options.default_shots = 100

job = sampler.run([isa_circuit])
print("Job ID:", job.job_id())
result = job.result(timeout=12000)
print("Result:", result)

pub_result = result[0]
counts = pub_result.data.c0.get_counts()
print(f"Counts for the c0 output register: {counts}")
