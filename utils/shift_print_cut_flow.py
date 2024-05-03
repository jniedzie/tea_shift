import ROOT
from collections import OrderedDict

from Logger import info, error

from shift_paths import luminosity, crossSections, nGenEvents, base_path, processes, skim, variant

def print_table(process_data):
    """
    Prints a table where each row corresponds to a selection, each column corresponds to a process,
    and each cell shows the ratio of events remaining after a selection compared to the previous selection.
    
    Parameters:
    - process_data: A dictionary where keys are process names, and values are dictionaries
                    mapping selection names to the number of events after the selection.
    """
    # Get a list of unique selections and processes
    selections = set()
    for process, sel_data in process_data.items():
        selections.update(sel_data.keys())

    selections = sorted(selections)  # Sort selections alphabetically for consistency
    processes = sorted(process_data.keys())  # Sort processes alphabetically

    # Define column widths
    col_width_sel = 20
    col_width_proc = 15

    # Print header row
    header = f"Selection".ljust(col_width_sel) + "|" + "".join(f"{process}".ljust(col_width_proc) + "|" for process in processes)
    print(header)
    print("=" * len(header))

    # Go through each selection, skipping the first for ratio purposes
    for i in range(1, len(selections)):
        sel = selections[i]
        row = sel.ljust(col_width_sel) + "|"

        for process in processes:
            prev_sel = selections[i - 1]
            prev_events = process_data.get(process, {}).get(prev_sel, None)
            curr_events = process_data.get(process, {}).get(sel, None)
            
            if prev_events is not None and curr_events is not None and prev_events != 0:
                ratio = curr_events / prev_events
                row += f"{ratio:.3f}".ljust(col_width_proc) + "|"
            elif curr_events is not None:
                row += f"{curr_events}".ljust(col_width_proc) + "|"
            else:
                row += "N/A".ljust(col_width_proc) + "|"

        print(row)

    # Adding a row for total efficiency
    row = "Total Efficiency".ljust(col_width_sel) + "|"
    for process in processes:
        first_events = process_data.get(process, {}).get(selections[0], None)
        last_events = process_data.get(process, {}).get(selections[-1], None)
        
        if first_events is not None and last_events is not None and first_events != 0:
            total_efficiency = last_events / first_events
            row += f"{total_efficiency:.3f}".ljust(col_width_proc) + "|"
        else:
            row += "N/A".ljust(col_width_proc) + "|"

    print(row)

        

def get_nice_name(process):
    # process is given in the form: "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"
    # remove "pythia_", replace mZprime with m_Z, remove mDQ-1 completely:
    process = process.replace("pythia_", "")
    process = process.replace("mZprime-", "m_Z=")
    process = process.replace("_mDH-", ", m_D=")
    process = process.replace("_mDQ-1", "")
    process = process.replace("_tau-", ", c#tau=")
    process = process.replace("1em", "10^-")
    process = process.replace("1e", "10^")
    
    return process
    

def main():
    ROOT.gROOT.SetBatch(True)

    cut_flow_per_process = {}
    scaled_cut_flow_per_process = {}

    for process in processes:
        input_path = f"{base_path}/{process}/merged_{skim}.root"
        print(f"Analyzing file: {input_path}")

        

        file = ROOT.TFile(input_path, "READ")
        dir = file.Get("CutFlow")
        
        if type(dir) != ROOT.TDirectoryFile:
            error(f"Could not find CutFlow directory in file {input_path}")
            continue
        
        keys = dir.GetListOfKeys()
        hist_dict = OrderedDict()

        for key in keys:
            hist = dir.Get(key.GetName())
            hist_dict[key.GetName()] = hist.GetBinContent(1)

        hist_dict = OrderedDict(
            sorted(hist_dict.items(), key=lambda x: int(x[0].split("_")[0])))

        scale = luminosity*crossSections[process]
        scale /= nGenEvents[process]

        cut_flow_per_process[get_nice_name(process)] = hist_dict
        
        scaled_cut_flow_per_process[get_nice_name(process)] = {
            key: value*scale for key, value in hist_dict.items()}

        print("CutFlow:")
        for key, value in hist_dict.items():
            print(f"{key:30}: {value:10}\t\t{value*scale:.4f}")

    print_table(cut_flow_per_process)


if __name__ == "__main__":
    main()
