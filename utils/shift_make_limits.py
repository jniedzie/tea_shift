import os, subprocess
import concurrent.futures

from shift_paths import processes, base_datacard_name
from shift_utils import get_file_name
from Logger import info

cmssw_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_11_3_4/src"
config_path = "./shift_datacards_config.py"

base_config_name = "shift_datacards_config_{}.py"
base_combine_output_name = "output_{}.txt"


# variants = ["cms"]
variants = ["shift160m"]

# variants = ["shift30m", "shift50m", "shift80m", "shift120m", "shift140m", "shift160m", "shift200m", "shift250m", "shift270m", "shift300m"]

histogram_name = "MuonsHittingDetectorPair_mass"
# histogram_name = "PtMuonsHittingDetectorPair_mass"
# histogram_name = "MuonsHittingDetectorPair_massCtauGt1cm"
# histogram_name = "MuonsHittingDetectorSameVertexPair_mass"

# variable = "mZprime"
# variable = "mDH"
# variable = "mDQ"
variable = "ctau"
# variable = "mDarkPhoton"
# variable = "2d"

# variable = "distance"

suffix = "_"

skip_combine = True

for part in processes[0].split("_"):
    if variable in part:
        suffix += part.split("-")[0] + "-X_"
    elif variable == "ctau" and "tau" in part:
        suffix += part.split("-")[0] + "-X_"
    else:
        suffix += part + "_"

# if suffix ends with "_", remove it
if suffix[-1] == "_":
    suffix = suffix[:-1]

if variable == "2d":
    suffix = "_2d"
    
if variable == "distance":
    suffix += "_distance"

# suffix = ""
# suffix = processes[0]

def run_commands_in_parallel(commands):
    info("Running all processes...") 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_command, cmd) for cmd in commands]

        # Wait for all commands to complete
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
    info("All processes completed.")

def prepare_datacards():
    commands = []
    
    for variant in variants:
        for process in processes:
            if "mZprime" not in process and "mDarkPhoton" not in process:
                continue
            
            with open(config_path, "r") as config_file:
                config = config_file.read()
                config = config.replace("signal_name = \"dummy_value\"", f"signal_name = \"{process}\"")
                config = config.replace("variant_name = \"dummy_value\"", f"variant_name = \"{variant}\"")
                config = config.replace("Histogram(name=\"dummy_value\"", f"Histogram(name=\"{histogram_name}\"")
            
                new_config_name = base_config_name.format(get_file_name(process, variant))
                with open(new_config_name, "w") as new_config_file:
                    new_config_file.write(config)
                    
            commands.append(f"python datacards_producer.py {new_config_name}")
            
    run_commands_in_parallel(commands)

def run_command(command):
    return os.system(command)

def run_combine():
    cwd = os.getcwd()
    base_command = f"cd {cmssw_path}; cmsenv; cd {cwd}/../datacards/;"
    commands = []
    
    for variant in variants:
        for process in processes:
            if "mZprime" not in process and "mDarkPhoton" not in process:
                continue
        
            datacard_path = base_datacard_name.format(get_file_name(process, variant)) + ".txt"
            combine_output_path = base_combine_output_name.format(get_file_name(process, variant))
            
            # combine_work_dir = f"combine_tmp_{process}"
            # # create work dir if doesn't exist
            # if not os.path.exists(combine_work_dir):
            #     os.makedirs(combine_work_dir)
            
            command = f"{base_command} combine -M AsymptoticLimits {datacard_path} > {combine_output_path}"
            commands.append(command)
            
    run_commands_in_parallel(commands)
    
    
def get_limits():
    limits_per_process = {}
    
    for variant in variants:    
        for process in processes:
            if "mZprime" not in process and "mDarkPhoton" not in process:
                continue
            
            combine_output_path = base_combine_output_name.format(get_file_name(process, variant))

            with open(f"../datacards/{combine_output_path}", "r") as combine_output_file:
                combine_output = combine_output_file.read()
                r_values = [line.split("r < ")[1].strip() for line in combine_output.split("\n") if "r < " in line]    
                limits_per_process[(process, variant)] = r_values
                
    return limits_per_process

def save_limits(limits_per_process):
    
    variant_name = variants[0] if len(variants) == 1 else ""
    file_path = f"limits_{histogram_name}_{variant_name}{suffix}.txt"
    info(f"Saving limits to {file_path}")
    
    with open(f"../datacards/{file_path}", "w") as limits_file:
        for (process, variant), limits in limits_per_process.items():
            limits_file.write(f"{process}_{variant}: {limits}\n")
            info(f"{process}_{variant}: {limits}")
            
def main():
    if not skip_combine:
        prepare_datacards()
        run_combine()
    limits_per_process = get_limits()
    save_limits(limits_per_process)
    
if __name__ == "__main__":
    main()
