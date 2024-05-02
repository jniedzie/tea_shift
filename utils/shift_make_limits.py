import os, subprocess

from shift_paths import processes, histograms_path
from Logger import info

cmssw_path = "/afs/desy.de/user/j/jniedzie/combine/CMSSW_11_3_4/src"
config_path = "./shift_datacards_config.py"

def prepare_datacards():
    for process in processes:
        if not process.startswith("pythia_mZprime"):
            continue
        
        with open(config_path, "r") as config_file:
            config = config_file.read()
            config = config.replace("signal_name = \"dummy_value\"", f"signal_name = \"{process}\"")

            new_config_name = f"shift_datacards_config_{process}.py"
            with open(new_config_name, "w") as new_config_file:
                new_config_file.write(config)
                
        os.system(f"python datacards_producer.py {new_config_name}")

def get_limits():
    cwd = os.getcwd()
    limits_per_process = {}
    
    base_command = f"cd {cmssw_path}; cmsenv; cd {cwd}/../datacards/;"
    for process in processes:
        if not process.startswith("pythia_mZprime"):
            continue
    
        datacard_path = f"limits_mass_{histograms_path.replace('histograms_', '')}_{process.replace('pythia_', '')}.txt"
        combine_output_path = f"output_{process.replace('pythia_', '')}.txt"
        
        info(f"Calculating limits for {process}")
        command = f"{base_command} combine -M AsymptoticLimits {datacard_path} > {combine_output_path}"
        info(f"Running command: {command}")
        os.system(command)
        
        with open(f"../datacards/{combine_output_path}", "r") as combine_output_file:
            combine_output = combine_output_file.read()
            r_values = [line.split("r < ")[1].strip() for line in combine_output.split("\n") if "r < " in line]    
            limits_per_process[process] = r_values
            
    return limits_per_process

def save_limits(limits_per_process):
    
    file_path = f"../datacards/limits_mass_{histograms_path.replace('histograms_', '')}.txt"
    
    with open(file_path, "w") as limits_file:
        for process, limits in limits_per_process.items():
            limits_file.write(f"{process}: {limits}\n")
            info(f"{process}: {limits}")
            

def main():
    prepare_datacards()
    
    cwd = os.getcwd()
    limits_per_process = get_limits()
    
    save_limits(limits_per_process)
    os.chdir(cwd)
    
    

if __name__ == "__main__":
    main()
