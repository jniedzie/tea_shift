import os, subprocess
import concurrent.futures

from shift_paths import processes, histograms_path, base_datacard_name
from shift_utils import get_file_name
from Logger import info

cmssw_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_11_3_4/src"
config_path = "./shift_datacards_config.py"

base_config_name = "shift_datacards_config_{}.py"
base_combine_output_name = "output_{}.txt"


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
    
    for process in processes:
        if "mZprime" not in process:
            continue
        
        with open(config_path, "r") as config_file:
            config = config_file.read()
            config = config.replace("signal_name = \"dummy_value\"", f"signal_name = \"{process}\"")

            new_config_name = base_config_name.format(get_file_name(process))
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
    
    for process in processes:
        if "mZprime" not in process:
            continue
    
        datacard_path = base_datacard_name.format(get_file_name(process)) + ".txt"
        combine_output_path = base_combine_output_name.format(get_file_name(process))
        
        # combine_work_dir = f"combine_tmp_{process}"
        # # create work dir if doesn't exist
        # if not os.path.exists(combine_work_dir):
        #     os.makedirs(combine_work_dir)
        
        command = f"{base_command} combine -M AsymptoticLimits {datacard_path} > {combine_output_path}"
        commands.append(command)
        
    run_commands_in_parallel(commands)
    
    
def get_limits():
    limits_per_process = {}
    for process in processes:
        if "mZprime" not in process:
            continue
        
        combine_output_path = base_combine_output_name.format(get_file_name(process))
        with open(f"../datacards/{combine_output_path}", "r") as combine_output_file:
            combine_output = combine_output_file.read()
            r_values = [line.split("r < ")[1].strip() for line in combine_output.split("\n") if "r < " in line]    
            limits_per_process[process] = r_values
            
    return limits_per_process

def save_limits(limits_per_process):
    
    file_path = f"limits_mass_{histograms_path.replace('histograms_', '')}.txt"
    
    with open(f"../datacards/{file_path}", "w") as limits_file:
        for process, limits in limits_per_process.items():
            limits_file.write(f"{process}: {limits}\n")
            info(f"{process}: {limits}")
            
def main():
    prepare_datacards()
    run_combine()
    limits_per_process = get_limits()
    save_limits(limits_per_process)
    
if __name__ == "__main__":
    main()
