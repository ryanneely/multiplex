##load_expt.py

##functions to load multiplex data

##by Ryan Neely 7/15/19 modified by Marius Guerard

import numpy as np
import importlib.util
from sample import Sample
import xlrd
import copy


def get_data(data_file, output_analytes=False):
    """
    A function to load and organize all of the data
    from on experiment
    Args:
        -data_file (str): the path of the file containing all the multiplex data and the map.
    Returns:
        -experiment (dic): data dictionary populated with Sample objects containing the data
    """

    ### Start by getting the map from the "map sheet" at the end of the data file.
    data_xl = xlrd.open_workbook(data_file)
    map_sheet = data_xl.sheet_by_index(-1)
    experiment = extract_map_from_sheet(map_sheet)

    # Store all the analytes present on this experiment.
    analytes_set = set()

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
                trial[s] = Sample(s, trial, sample_id, data_xl)
                analytes_set.update(set(trial[s].analyte_names))
    if output_analytes:
        return experiment, analytes_set
    else:
        return experiment


def extract_map_from_sheet(map_sheet):
    """ Given an excel map, return the multiplex_id it is associated with as well as a python
    dictionary contianing the map.
    """
    exp = {}
    for row_idx in range(1, map_sheet.nrows):
        stim_type = map_sheet.cell(row_idx, 3).value
        dataset_name = map_sheet.cell(row_idx, 0).value
        # print(dataset_name)
        # Extracting the mapping for each time.
        time_tmp = map_sheet.cell(row_idx, 1).value
        map_tmp = map_sheet.cell(row_idx, 2).value
        # Removing the eventual spaces.
        time_tmp = time_tmp.replace(" ", "")
        map_tmp = map_tmp.replace(" ", "")
        # Getting all the values for time and map.
        time_vec = time_tmp.split(',')
        map_vec = map_tmp.split(',')
        exp.setdefault(stim_type, {})[dataset_name] = {time: map_time
                                                       for time, map_time in zip(time_vec, map_vec)}
    return exp



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
                # cv = np.nanstd(c,ddof=1)/np.nanmean(c)
                # if (warn_cv>0) and (cv>warn_cv):
                #     print("Warning: cv for sample {} from {} is {}".format(s,t,cv))
                if avg:
                    c = np.nanmean(c)
                trial[s] = c
    return data2


def group_data(results):
    """
    Returns the group data from one analyte packaged in a nice array format.
    Note: this was really designed assuming a set of experiments
    with regular, equal sample structure, and might not work well for
    other experimental designs. We'll try to organize things as best we can. 
    Args:
        -results: the results dictionary, as output buy the function get_analyte_data.
            data needs to be averaged across duplicates.
    Returns:
        -x: putative "time" axis, assuming that is how the samples are arranged
        -out: dictionary with data compiled across the top-
            level groups, assumed to be experimental conditions.
    """
    groups = list(results) ##this is the group level ("sham","stim",etc)
    ##create the output dictionary
    out = {}
    x = check_timepoints(results) ##this is the list of all possible timepoints
    for g in groups:
        trials = list(results[g]) ##these are the individual experiments ("12_12_20_RN1")
        data = np.empty((len(trials),len(x))) #we will fill this with the data 
        data[:] = np.nan ##any sets with missing data will be left as NaN
        for i,t in enumerate(trials):
            ##now put all of the available data in the data array
            for n,p in enumerate(x):
                try:
                    data[i,n] = results[g][t][p]
                except KeyError: ##case where we're missing this timepoint
                    print("Missing timepoint {} in set {}".format(p,t))
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

def check_timepoints(d):
    """
    Function to check timepoints present in a set of data. Understanding
    that some timepoints will be missing from some samples, we want to 
    be able to define those points as np.nan so that we can still integrate that
    set with everything else.
    Args:
        -d: data dictionary for one analyte. 
    Returns:
        -timepoints: an array with the most timepoints recorded in this set of data
    """
    groups = list(d)
    timepoints = []
    for g in groups:
        for e in list(d[g]): ##the data from one animal, presumeably
            x = list(d[g][e]) ##the timepoints from this set
            if len(x)>len(timepoints):
                timepoints = x
    return timepoints



def standard_curve():
    pass
