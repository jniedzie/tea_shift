from shift_paths import histograms_path

def get_file_name(process):
    return f"{histograms_path.replace('histograms_', '')}_{process.replace('pythia', '')}"


def get_file_name(process, variant):
    histograms_path = "histograms_" + variant
    return f"{histograms_path.replace('histograms_', '')}_{process.replace('pythia', '')}"
