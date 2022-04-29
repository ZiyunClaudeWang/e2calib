import h5py
import numpy as np
import hdf5plugin

import pdb

name = "/home/cwang/data_temp/2022-04-29-01-50-19/2022-04-29-01-50-19.h5"

data = h5py.File(name, 'r')
trigger = data['dvs']['trigger']
save_file = name.replace(".h5", "_ts.txt")

with open(save_file, 'w') as f:
    for t in trigger:
        f.write(str(int(t))+"\n")
