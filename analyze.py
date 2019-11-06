##analyze.py

##functions to perform analysis on multiplex data

##by Ryan Neely 10/31/19

import load_expt
import numpy as np

def norm_single(ctrl,test):
    """
    Function to normalize test values to some control.
    Args:
        -ctrl: control results dictionary for one analyte
        -test: test results dictionary for same analyte
    Returns:
        -norms: values of each test result normalized to the mean of the control
    """
    ##first find the mean of all the control values at each time point
    ctrl = ctrl.mean(axis=0)
    return test/ctrl

def norm_all(data,ctrl='sham'):
    """
    Normalizes the all of the test values for each analyte to the matched
    controls at each time point
    args:
        -data: full populated data dictionary (output of load_expt.get_data)
        -ctrl: the key associated with the control dataset
    returns:
        -norm_data: data dictionary in which all the test values have been normalized to 
            the mean of the matched control for each analyte
    """
    ##get the list of analytes in this dataset
    groups = list(data)
    trials = list(data[groups[0]])
    samples = list(data[groups[0]][trials[0]])
    analyte_list = data[groups[0]][trials[0]][samples[0]].analyte_names
    ##create the output dictionary
    norm_data = {}
    for a in analyte_list:
        ##create an entry in the output data
        norm_data[a] = {}
        results = load_expt.get_analyte_data(data,a,avg=True,warn_cv=0.5)
        x,vals = load_expt.group_data(results)
        groups = [v for v in vals if not v==ctrl]
        for g in groups:
            ctrl_data = vals[ctrl]
            test_data = vals[g]
            norm = norm_single(ctrl_data,test_data)
            norm_data[a][g] = norm
    return x,norm_data
            
def norm_mean(norm_data,test=None):
    """
    A function to collapse the normalized data into a single array
    of mean values. Only works with one test dset (for now)
    Args:
        -norm_data: normalized data dictionary
        -test: the test dset to use, if None defaults to the first
    Returns:
        -analytes, dsets
    """
    ##get the name of the test dset to look at, if unspecified
    if test == None:
        test = list(norm_data[list(norm_data)[0]])[0]
    analytes = list(norm_data)
    ##find the expected size of the output array
    x = len(analytes) ##the analyte dimension
    y = norm_data[analytes[0]][test].shape[0]
    dsets = np.zeros((x,y))
    for i,a in enumerate(analytes):
        dsets[i,:] = norm_data[a][test].mean(axis=0)
    return analytes,dsets
    
    
def divergence_single(ctrl,test):
    """
    A Function to compute the "divergence" of the test data from 
    the control, which here we'll define as the mean difference between
    stim and control relative to the mean difference at the baseline timepoint.
    Specifically for single-anayte data. 
    Args:
        -ctrl: control results dictionary for one analyte
        -test: test results dictionary for same analyte
    Returns:
        -divergence: values of divergence (1d array) including the first value (always 1)
    """
    ##the value to normalize to is the difference between test and ctrl at the baseline
    ##timepoint, assumed to be the first one.
    base = test[:,0].mean()-ctrl[:,0].mean()
    ##absoulte difference at all timepoints
    diff = test.mean(axis=0)-ctrl.mean(axis=0)
    ##now normalize to the first difference
    return (diff-base)/abs(base)

def divergence_all(data,ctrl='sham',test=None):
    """
    Computes the divergence of the all of the test values for each analyte relative to the matched
    controls at each time point, normalized to the starting difference between test and ctrl
    args:
        -data: full populated data dictionary (output of load_expt.get_data)
        -ctrl: the key associated with the control dataset
        -test: the key associated with the test dataset. if None, uses the first non-control group.
    returns:
        -analyte_list: list of analytes in order of the divergence data matrix axis 0
        -samples: array of timepoints in order of the divergence data matrix axis 1
        -divergence_data: a 2D np.array in dimensions analytes x samples
    """
    ##get the list of analytes in this dataset
    groups = list(data)
    trials = list(data[groups[0]])
    samples = list(data[groups[0]][trials[0]])
    analyte_list = data[groups[0]][trials[0]][samples[0]].analyte_names
    ##create the output array
    divergence = np.zeros((len(analyte_list),len(samples)))
    for i,a in enumerate(analyte_list):
        ##get the data arrays for this analyte
        results = load_expt.get_analyte_data(data,a,avg=True,warn_cv=0.5)
        x,vals = load_expt.group_data(results)
        groups = [v for v in vals if not v==ctrl]
        if test == None:
            g = groups[0]
        ctrl_data = vals[ctrl]
        test_data = vals[g]
        d = divergence_single(ctrl_data,test_data)
        divergence[i,:] = d
    return analyte_list,np.asarray(samples),divergence

