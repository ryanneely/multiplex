###plot.py

##functions to plot results

##by Ryan Neely 7/15/19

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import load_expt
import combine_plates
import os

def plot_analyte(data,analyte,save=False):
    """
    Plots the results from a single analyte. 
    Args:
        -data: populated data dictionary
        -analyte (str): name of the analyte to plot (must match name in excel file)
        -save: if not False, should be the path to save the plot to
    """
    colors = ['r','b','g','orange','cyan']
    
    error_config = {
    'ecolor':'k',
    'capthick':2,
    'capsize':5,
    'elinewidth':2
    }
    fig,ax = plt.subplots(1)
    ##grab the data from this analyte
    results = load_expt.get_analyte_data(data,analyte,avg=True,warn_cv=0.2)
    ##organize the data into a convenient structure
    x,vals = load_expt.group_data(results)
    groups = list(vals)
    w = 1.0/len(groups)
    bars = np.arange(len(x))*1.3
    for i,g in enumerate(groups):
        index = bars+i*w
        heights = np.nanmean(vals[g],axis=0)
        err = np.nanstd(vals[g],axis=0)/vals[g].shape[0]
        ax.bar(index, heights, w,
            color=colors[i],edgecolor='k',linewidth=3,alpha=0.9,
               yerr=err, error_kw=error_config,label="{}, n={}".format(g,str(vals[g].shape[0])),
               zorder=-1)
        ##now the individual points
        for n,b in enumerate(index):
            ax.scatter(b+np.random.random(vals[g][:,n].size)*w-w/2,vals[g][:,n], 
            color=colors[i],zorder=1,edgecolors='k')
    ax.set_xlabel('Serum sample time',fontsize=14)
    ax.set_ylabel('Serum concentration, pg/ml',fontsize=14)
    ax.set_title(analyte,fontsize=14)
    ax.set_xticks(bars + w / 2)
    ax.set_xticklabels(x)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12) 
        tick.label.set_rotation(30)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(12) 
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    if save:
        analyte = remove_forward_slash(analyte)
        plt.savefig(os.path.join(save,analyte+".png"))



def plot_all(f,save=False):
    """
    Plots all analytes from a single plate experiment.
    Args:
        -f: file path to the maps file
        -save: if not False, should be a file path to save the files to.
    """
    data = load_expt.get_data(f) ##data for all analytes
    ##now pull out the full list of analytes
    groups = list(data)
    trials = list(data[groups[0]])
    samples = list(data[groups[0]][trials[0]])
    analyte_list = data[groups[0]][trials[0]][samples[0]].analyte_names
    for a in analyte_list:
        plot_analyte(data,a,save=save)

def plot_multi(maps,ignore=[],save=False):
    """
    Same as plot_all, but combines data across plates.
    Args:
        -maps (iterable): list of metadata file paths        
        -ignore (list): adding group names to ignore causes the function not to
            add these groups to the final dset. Helpful if you want to grab the control
            data from a plate, but not the stim data. 
        -save: if not False, should be a file path to save the files to.
    """
    data = combine_plates.combine(maps,ignore=ignore) ##data for all analytes
    ##now pull out the full list of analytes
    groups = list(data)
    trials = list(data[groups[0]])
    samples = list(data[groups[0]][trials[0]])
    analyte_list = data[groups[0]][trials[0]][samples[0]].analyte_names
    for a in analyte_list:
        plot_analyte(data,a,save=save)

def remove_forward_slash(string):
    newstr = ''
    for l in string:
        if l != '/':
            newstr+=l
        else:
            newstr+='-'
    return newstr

        
        
