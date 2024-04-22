from utils import get_service, get_job, get_export_path

service = get_service()
job = service.job(get_job())
job_result = job.result()

for idx, pub_result in enumerate(job_result):
    print(f"Expectation values for pub {idx}: {pub_result.data.evs}")

# graph the result
import matplotlib.pyplot as plt

data = observables_labels = ["ZZ", "ZI", "IZ", "XX", "XI"]
values = pub_result.data.evs

errors = pub_result.data.ensemble_standard_error

plt.errorbar(observables_labels, values, yerr=errors, fmt="o")
plt.xlabel('Observables')
plt.ylabel('Expectation Value')
plt.title('Expectation values for each observable')
plt.grid()

# Save the figure to a file
plt.savefig(get_export_path())
print(f"Graph saved to {get_export_path()}")
