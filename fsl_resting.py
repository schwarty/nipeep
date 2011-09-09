# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
   A nipeep example to show that peeping isn't always bad. 
   That uses integrates several interfaces to perform a first 
   and second level analysis on a two-subject data set.
"""


"""
1. Tell python where to find the appropriate functions.
"""
import os                                    # system functions
import glob
from functools import partial

import numpy as np

import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.fsl as fsl          # fsl
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.algorithms.modelgen as model   # model generation

from nipeep import Memory

from pyxnat import Interface

mem = Memory('.')

central = Interface('https://central.xnat.org', 'schwarty', 'plopplop', 
                    '/havoc/store/xnat')

fsl.FSLCommand.set_default_output_type('NIFTI_GZ')

input_files = [central.select('/project/Volatile/resources/123150742/files/000075760021s002a1001.nii.gz').get()]

# where put files arguments?

# extract_ref = partial(mem.cache(fsl.ExtractROI), t_min=42, t_size=1)
nosestrip = partial(mem.cache(fsl.BET), frac=0.3)
skullstrip = partial(mem.cache(fsl.BET), mask=True)
refskullstrip = partial(mem.cache(fsl.BET), mask=True)
# coregister = mem.cache(fsl.FLIRT)(dof=6)

# extract_ref_exec = [
#     extract_ref(in_file=in_file) for in_file in input_files]

nosestrip_exec = [
    nosestrip(in_file=in_file) for in_file in input_files] 

skullstrip_exec = [
    skullstrip(in_file=o.outputs.out_file) for o in nosestrip_exec] 

refskullstrip_exec = [
    refskullstrip(in_file=o.outputs.out_file) for o in skullstrip_exec] 

mem.clear_previous_runs()

