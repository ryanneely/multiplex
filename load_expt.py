##load_expt.py

##functions to load multiplex data

##by Ryan Neely 7/15/19

import numpy as np
import importlib.util
from sample import Sample
import xlrd
import copy

def get_data(f):
    """
    A function to load and organize all of the data
    from on experiment
    Args:
        -f: the path experiment file containing all of the metadata
    Returns:
        -experiment: data dictionary populated with Sample objects containing the data
    """
    ##import the metadata (I know, bad practice etc, etc)
    ##here we have to do some tricks to load a module from a different location
    spec = importlib.util.spec_from_file_location("expt", f)
    expt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expt)
    wb = xlrd.open_workbook(expt.workbook) ##the path to the excel datafile
    experiment = expt.experiment ##the dictionary with all of the group/sample info
    ##the experiment dictionary now contains the sample ID of each sample as 
    ##specified in the excel file. Now we have what we need to go through and
    ##replace each str sample ID with populated Sample objects
    for g in list(experiment): ##top level is ctrl, experimental groups
        group = experiment[g]
        for t in list(group): ##next level is trials/animals
            trial = group[t]
            for s in list(trial):
                sample_id = trial[s]
                ##now replace the ID with a populated Sample object
                trial[s] = Sample(s,trial,sample_id,wb)
    return experiment

def get_analyte_data(data,name,avg=True,warn_cv=0.2):
    """
    Function that returns data from a single analyte for all samples. 
    Args:
        -data: a populated dictionary of data
        -name: name of the analyte (str), must match what is in the spreadsheet.
        -avg (bool): whether or not to average across duplicates
        -warn_cv: warn if the CV of the concentration is over N.
            if N = 0, do not issue a warning. 
    Returns:
        -concentrations of analyte for all samples, in dictionary format. 
    """
    data2 = copy.deepcopy(data) ##create a full copy so as not to edit the original
    for g in list(data2): ##top level is ctrl, experimental groups
        group = data2[g]
        for t in list(group): ##next level is trials/animals
            trial = group[t]
            for s in list(trial):
                sample = trial[s]
                ##find the analyte object corresponding to the requested analyte
                idx = np.where(sample.analyte_names==name)[0]
                assert len(idx)>0, "Cant find {} in data.".format(name)
                analyte = sample.analytes[idx[0]]
                assert analyte.name == name
                ##get the computed concentration of this analyte
                c = check_data(analyte.c_obs)
                # print(c)
                ##TODO: decide whether to look at FI %CV or to stick with concentrations
                cv = np.nanstd(c,ddof=1)/np.nanmean(c)
                if (warn_cv>0) and (cv>warn_cv):
                    print("Warning: cv for sample {} from {} is {}".format(s,t,cv))
                if avg:
                    c = np.nanmean(c)
                trial[s] = c
    return data2

def group_data(results):
    """
    Returns the group data one analyte packaged in a nice array format.
    Note: this was really designed assuming a set of experiments
    with regular, equal sample structure, and might not work well for 
    other experimental designs. 
    Args:
        -results: the results dictionary, as output buy the function get_analyte_data.
            data needs to be averaged across duplicates.
    Returns:
        -x: putative "time" axis, assuming that is how the samples are arranged
        -out: dictionary with data compiled across the top-
            level groups, assumed to be experimental conditions.
    """
    groups = list(results)
    ##create the output dictionary
    out = {}
    x = None
    for g in groups:
        trials = list(results[g])
        data = []
        for t in trials:
            if x is not None:
                ##check here to make sure the sample times are are the same
                assert np.all(x == np.asarray(list(results[g][t]))), "Sample times not aligned"
            x = np.asarray(list(results[g][t]))
            data.append(np.asarray(list(results[g][t].values())))
        out[g] = np.asarray(data)
    return x,out

def check_data(c):
    """
    Handle any odd notations that might occur in the excel file
    Args:
        -c: list of concentration values
    Returns:
        -c: same list with problematic values changed
    """
    ##check if any of the values are outside of the observable range
    for i,x in enumerate(c):
        if type(x)==str:
            if x == "OOR <": ##below detectable range, set to 0
                c[i] = 0.0
            elif x == "OOR >": ##above detectable range, set to NaN
                c[i] = np.nan
            elif x == "***": #data not available; set to NaN
                c[i] = np.nan
            elif x == "---": #designated outlier; set to NaN
                c[i] = np.nan
            elif '*' in x:
                c[i] = float(''.join( c for c in x if  c !='*'))
    return c
                
        
def standard_curve():
    pass