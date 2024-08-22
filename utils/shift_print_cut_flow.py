import ROOT
from collections import OrderedDict
from decimal import Decimal, getcontext

from Logger import info, error

from shift_paths import luminosity, luminosity_err, crossSections, base_path, processes, variant

def format_number(number, significant_digits=1):
    if number == 0:
        return 0
    
    format_string = f".{significant_digits}g"
    formatted_number = format(number, format_string)

    return formatted_number

def print_table(process_data):
    # sort processes by c#tau value taking anything that comes after "tau-"
    processes = sorted(process_data.keys(), key=lambda x: float(x.split("ctau-")[1]) if "ctau-" in x else 0)
    
    # Get a list of unique selections and processes
    selections = set()
    for process, sel_data in process_data.items():
        selections.update(sel_data.keys())

    selections = sorted(selections)  # Sort selections alphabetically for consistency
    # processes = sorted(process_data.keys())  # Sort processes alphabetically

    # Define column widths
    col_width_sel = 35
    col_width_proc = 35

    # Print header row
    header = f"Selection".ljust(col_width_sel) + "|" + "".join(f"{process}".ljust(col_width_proc) + "|" for process in processes)
    print(header)
    print("=" * len(header))

    # Go through each selection, skipping the first for ratio purposes
    for i in range(1, len(selections)):
        sel = selections[i]
        
        if sel == "3_intersectingDetector":
            continue
        
        row = sel.ljust(col_width_sel) + "|"

        

        for process in processes:
            prev_sel = selections[i - 1]
            
            if sel == "4_beforeDetector":
                prev_sel = selections[i - 2]
            
            prev_events = process_data.get(process, {}).get(prev_sel, [])
            curr_events = process_data.get(process, {}).get(sel, [])
            
            if prev_events is not None and curr_events is not None and prev_events != 0:
                ratio = curr_events / prev_events
                if curr_events == 0:
                    ratio_err = 0
                else:
                    ratio_err = ratio * (1/curr_events + 1/prev_events)**0.5
                row += f"{format_number(ratio)} +/- {format_number(ratio_err)}".ljust(col_width_proc) + "|"
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
            if last_events == 0:
                total_efficiency_err = 0
            else:
                total_efficiency_err = total_efficiency * (1/last_events + 1/first_events)**0.5
            
            # print enough decimal places to display the first digit that's not zero
        
            row += f"{format_number(total_efficiency)} +/- {format_number(total_efficiency_err)}".ljust(col_width_proc) + "|"
        else:
            row += "N/A".ljust(col_width_proc) + "|"

    print(row)

        

def get_nice_name(process):
    # process is given in the form: "pythia_mZprime-100_mDH-20_mDQ-1_tau-1em7"
    # remove "pythia_", replace mZprime with m_Z, remove mDQ-1 completely:
    process = process.replace("pythia_", "")
    process = process.replace("pythiaCollider_", "")
    process = process.replace("mZprime-", "m_{Z'}=")
    process = process.replace("_mDH-", ", m_{DH}=")
    process = process.replace("mDarkPhoton-", "m_{A'}=")
    process = process.replace("_mDQ-1", "")
    process = process.replace("_tau-", ", c#tau=")
    process = process.replace("_ctau-", ", c#tau=")
    process = process.replace("1em", "1e-")
    process = process.replace("1e", "1e")
    
    return process
    
def get_cut_flow_dict_from_file(process):
    input_path = f"{base_path}/{process}/merged_{variant}_histograms.root"
    print(f"Analyzing file: {input_path}")

    file = ROOT.TFile(input_path, "READ")
    hist = file.Get("cutFlow")
    
    if type(hist) != ROOT.TH1D:
        error(f"Could not find CutFlow in file {input_path}")
        return None
    
    hist_dict = {}
    
    for i in range(1, hist.GetNbinsX() + 1):
        # get bin label and use it as a key
        key = hist.GetXaxis().GetBinLabel(i)
        hist_dict[key] = hist.GetBinContent(i)

    hist_dict = OrderedDict(
        sorted(hist_dict.items(), key=lambda x: int(x[0].split("_")[0])))
    
    return hist_dict

def get_scale(process, hist_dict):
    key = process
    if key not in crossSections:
        key = key.replace("Collider", "")

    sigma = crossSections[key]
    n_initial = hist_dict["0_initial"]
    
    scale = luminosity*sigma
    info(f"{luminosity=}")
    info(f"{sigma=}")
    info(f"{scale=}")
    
    scale /= n_initial
    
    info(f"{scale=}")
    
    return scale

def main():
    ROOT.gROOT.SetBatch(True)

    cut_flow_per_process = {}
    scaled_cut_flow_per_process = {}

    for process in processes:
        print("\n\n")
        
        hist_dict = get_cut_flow_dict_from_file(process)
        if not hist_dict:
            continue

        scale = get_scale(process, hist_dict)
        cut_flow_per_process[get_nice_name(process)] = hist_dict
        
        scaled_cut_flow_per_process[get_nice_name(process)] = {}

        print("CutFlow:")
        for key, value in hist_dict.items():
            
            n_initial = hist_dict["0_initial"]
            
            process_key = process
            if process_key not in crossSections:
                process_key = process_key.replace("Collider", "")
            
            sigma = crossSections[process_key]
            
            n_raw = value
            n_raw_err = n_raw**0.5
            
            n_scaled = value*scale
            n_scaled_err = sigma/n_initial * (luminosity**2*n_raw + n_raw**2*luminosity**2/n_initial + n_raw**2*luminosity_err**2)**0.5
            
            print(f"{key:30}: {n_raw:.2f} +/- {n_raw_err:.2f}\t\t{n_scaled:.2e} +/- {n_scaled_err:.2e}")
            
            scaled_cut_flow_per_process[get_nice_name(process)][key] = (n_scaled, n_scaled_err)
            
        print("\n\n")
            
    print("\n\n")
    print_table(cut_flow_per_process)
    print("\n\n")


if __name__ == "__main__":
    main()
