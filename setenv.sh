#!/bin/sh

currentDIR="$( pwd )"
pythiaDIR=$currentDIR/MG5/HEPTools/pythia8
lhapdfDIR=$currentDIR/MG5/HEPTools/lhapdf6_py3
collierDIR=$currentDIR/MG5/HEPTools/collier
ninjaDIR=$currentDIR/MG5/HEPTools/ninja/lib/
export LD_LIBRARY_PATH=$lhapdfDIR/lib:$pythiaDIR/lib:$collierDIR:$ninjaDIR:$LD_LIBRARY_PATH
export PYTHONPATH=$currentDIR/MG5/HEPTools/lhapdf6_py3/local/lib/python3.12/dist-packages:$PYTHONPATH
export ROOT_INCLUDE_PATH=$currentDIR/MG5/Delphes/external:$ROOT_INCLUDE_PATH
