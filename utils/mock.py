from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def mock(qc):
    aersim = AerSimulator()
    result_ideal = aersim.run(qc).result()
    print('Result(ideal):', result_ideal)
    counts_ideal = result_ideal.get_counts(0)
    print('Counts(ideal):', counts_ideal)

    return result_ideal, counts_ideal

def save_mock_counts(counts_ideal, path="results/counts_histogram.png"):
    # Plot a histogram of the counts
    figure = plot_histogram(counts_ideal)

    # Save the figure to a file
    figure.savefig(path)
    print("Graph saved to " + path)
