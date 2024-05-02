from shift_paths import histograms_path

def get_file_name(process):
    return f"{histograms_path.replace('histograms_', '')}_{process.replace('pythia', '')}"
