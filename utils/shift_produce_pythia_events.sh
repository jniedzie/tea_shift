#!/bin/bash

user_base_path="/afs/desy.de/user/j/jniedzie/tea_shift/bin/"
python_path="/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"
pythia_exec_path="/afs/desy.de/user/j/jniedzie/pythia_new/pythia8309/examples/main42"
# pythia_exec_path="/afs/desy.de/user/j/jniedzie/pythia_new/pythia8309/examples/main42_biased"

export PYTHIA8=/afs/desy.de/user/j/jniedzie/pythia_new/install
export PYTHIA8DATA=$PYTHIA8/share/Pythia8/xmldoc
export PATH=$PYTHIA8/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PYTHIA8/lib
export LD_LIBRARY_PATH=/cvmfs/sft.cern.ch/lcg/releases/gcc/8.3.0-cebb0/x86_64-centos7/lib64:$LD_LIBRARY_PATH

# source /afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/thisroot.sh

cd $user_base_path || exit
#mkdir -p output error log

# read third argument as process type
process_type=$3

# depending on the process type, invoke the appropriate python script
if [ $process_type == "qcd" ]; then
    $python_path $user_base_path/shift_produce_pythia_events.py --part $1 --n_events $2 --process 1 --ptHat_min $4 --ptHat_max $5 --output_path $6 --base_pythia_card $7 --pythia_exec $pythia_exec_path
elif [ $process_type == "dy" ]; then
    $python_path $user_base_path/shift_produce_pythia_events.py --part $1 --n_events $2 --process 2 --output_path $4 --base_pythia_card $5 --pythia_exec $pythia_exec_path
elif [ $process_type == "hidden_valley" ]; then
    $python_path $user_base_path/shift_produce_pythia_events.py --part $1 --n_events $2 --process 3 --m_z_prime $4 --m_dark_hadron $5 --m_dark_quark $6 --lifetime $7 --output_path $8 --base_pythia_card $9 --pythia_exec $pythia_exec_path
elif [ $process_type == "dark_photon" ]; then
    $python_path $user_base_path/shift_produce_pythia_events.py --part $1 --n_events $2 --process 4 --m_dark_photon $4 --lifetime $5 --output_path $6 --base_pythia_card $7 --pythia_exec $pythia_exec_path
fi


