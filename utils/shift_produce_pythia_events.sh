#!/bin/bash

user_base_path="/afs/desy.de/user/j/jniedzie/tea_shift/bin/"
python_path="/afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/python3"
base_pythia_card="shift_base_pythia_card.cmnd"
pythia_exec_path="/afs/desy.de/user/j/jniedzie/pythia_new/pythia8309/examples/main42"

export PYTHIA8=/afs/desy.de/user/j/jniedzie/pythia_new/install
export PYTHIA8DATA=$PYTHIA8/share/Pythia8/xmldoc
export PATH=$PYTHIA8/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PYTHIA8/lib
export LD_LIBRARY_PATH=/cvmfs/sft.cern.ch/lcg/releases/gcc/8.3.0-cebb0/x86_64-centos7/lib64:$LD_LIBRARY_PATH

# source /afs/desy.de/user/j/jniedzie/miniconda3/envs/tta/bin/thisroot.sh

cd $user_base_path || exit
#mkdir -p output error log

$python_path $user_base_path/shift_produce_pythia_events.py --part $1 --n_events $2 --m_z_prime $3 --m_dark_hadron $4 --m_dark_quark $5 --lifetime $6 --output_path $7 --base_pythia_card $base_pythia_card --pythia_exec $pythia_exec_path
