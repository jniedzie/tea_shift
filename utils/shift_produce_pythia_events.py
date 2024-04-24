import os
from pathlib import Path
import shutil
import argparse
import fileinput
import random

dry_run = False


def run_command(config_path, output_path, file_name, pythia_exec_path):
    
    # Run Pythia production
    output_file_path = f"{output_path}/{file_name}.hepmc"
    command = f"{pythia_exec_path} {config_path} {output_file_path}"
    
    print(f"running command: {command}")
    if not dry_run:
        os.system(command)

    # Convert hepmc to ROOT
    hepmc_path="./hepmc2root"
    command = f"{hepmc_path} {output_file_path}"

    print(f"running command: {command}")
    if not dry_run:
        os.system(command)
    
    # Move ROOT file to the output directory
    command = f"mv {file_name}.root {output_path}/"

    print(f"running command: {command}")
    if not dry_run:
        os.system(command)

    # Remove hepmc file
    command = f"rm {output_path}/{file_name}.hepmc"
    
    print(f"running command: {command}")
    if not dry_run:
        os.system(command)


def create_paths(paths):
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

    
def copy_and_update_config(base_config_path, new_config_path, values_to_change):
    
    shutil.copyfile(base_config_path, new_config_path)

    for line in fileinput.input(new_config_path, inplace=True):
        line = line.rstrip()
        if not line:
            continue
        
        for key, value in values_to_change.items():
            keyword, default_value = key
            if keyword in line:
                line = line.replace(default_value, str(value))
        print(line)
        

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", help="", default=0)
    parser.add_argument("-n", "--n_events", help="", default=1000)
    
    parser.add_argument("-z", "--m_z_prime", help="Z' mass (GeV)", default=100, type=float)
    parser.add_argument("-d", "--m_dark_hadron", help="Dark pi/rho mass (GeV)", default=2, type=float)
    parser.add_argument("-q", "--m_dark_quark", help="Dark quark mass (GeV)", default=1, type=float)
    
    parser.add_argument("-l", "--lifetime", help="Dark pi/rho mean lifetime (m)", default=70, type=float)
    
    parser.add_argument("-o", "--output_path", help="", default=".")
    
    parser.add_argument("-bc", "--base_pythia_card", help="", default="")
    parser.add_argument("-pe", "--pythia_exec", help="", default="")
    
    return parser.parse_args()


def clear_string(s):
    return s.replace(".", "p").replace("-", "m").replace("+", "")
    

def main():
    random.seed(None)
    
    args = get_args()
    
    part = args.part
    n_events = args.n_events
    
    m_z_prime = args.m_z_prime
    m_dark_hadron = args.m_dark_hadron
    m_dark_quark = args.m_dark_quark
    lifetime = args.lifetime
    
    output_path = args.output_path
    
    create_paths(("tmp_cards", output_path))
    
    file_hash = random.getrandbits(128)
    
    new_pythia_card_path = f"tmp_cards/pythia_card_{file_hash}.cmnd"

    m_z_prime_name = clear_string(f"{m_z_prime:.0f}")
    m_dark_hadron_name = clear_string(f"{m_dark_hadron:.0f}")
    m_dark_quark_name = clear_string(f"{m_dark_quark:.0f}")
    
    lifetime_name = clear_string(f"{lifetime:.2e}")
    
    if args.m_z_prime > 0:
        file_name = f"mZprime-{m_z_prime_name}GeV"
        file_name += f"_mDarkHadron-{m_dark_hadron_name}GeV"
        file_name += f"_mDarkQuark-{m_dark_quark_name}GeV"
        file_name += f"_lifetime-{lifetime_name}m"
        file_name += f"_part-{part}"
    elif args.m_z_prime == -1:
        file_name = f"qcd_part-{part}"
    elif args.m_z_prime == -2:
        file_name = f"dy_part-{part}"
    
    # prepare pythia card
    to_change = {
        ("Main:numberOfEvents", "dummy_value"): n_events,
        ("Random:seed", "dummy_value"): random.randint(0, 1000000),
        
        ("4900023:m0", "dummy_value"): m_z_prime,
        ("4900023:mMin", "dummy_value"): m_z_prime-1,
        ("4900023:mMax", "dummy_value"): m_z_prime+1,
    
        ("4900111:m0", "dummy_value"): m_dark_hadron,
        ("4900113:m0", "dummy_value"): m_dark_hadron,
        
        ("4900101:m0", "dummy_value"): m_dark_quark,
    
        ("4900111:tau0", "dummy_value"): lifetime * 1000,
        ("4900113:tau0", "dummy_value"): lifetime * 1000,
    }

    copy_and_update_config(args.base_pythia_card, new_pythia_card_path, to_change)

    # run production
    run_command(new_pythia_card_path, output_path, file_name, args.pythia_exec)


if __name__ == "__main__":
    main()
