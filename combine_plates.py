##combine_plates.py

##functions to load data from multiple plates

##by Ryan Neely 10/5/19

import load_expt

def combine(maps,ignore=[]):
    """
    A function to create on dictionary out of multiple data dictionaries.
    Note that groups with the same name will be combined, but separately
    named groups will remain separate.
    Args:
        -maps (iterable): list of experiment files to combine
        -ignore (list): adding group names to ignore causes the function not to
            add these groups to the final dset. Helpful if you want to grab the control
            data from a plate, but not the stim data. 
    Returns:
        -data: single data dictionary
    """
    ##load all of the data into a list
    data = [load_expt.get_data(f) for f in maps]
    ##create a master dictionary with all of the data combined
    combined = {}
    for dset in data:
        groups = list(dset)
        for g in groups:
            if not g in ignore: ##don't add it if it's blacklisted
                ##check to see if this group already exists
                if g in combined:
                    expts = list(dset[g])
                    for e in expts:
                        combined[g][e] = dset[g][e]
                else:
                    combined[g] = dset[g]
    return combined




