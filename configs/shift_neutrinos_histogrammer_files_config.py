from shift_neutrinos_paths import processes, base_path, variant

samples = processes
sample_path = ""

input_directory = f"{base_path}/{sample_path}/initial/"
output_trees_dir = f"{base_path}/{sample_path}/{variant}/neutrinos_trees/"
output_hists_dir = f"{base_path}/{sample_path}/{variant}/neutrinos_histograms/"

extra_args = {}
