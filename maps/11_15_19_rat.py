#10_25_19_2.py

##data structure that defines the multiplex assay experiment

"""
Notes:

experiment comparing sham stimulation to a 30Hz standardized RC, using 6-hr timepoints. 
Pro-inflammatory experiments:
all in-vivo
n = 6 stim, n = 2 sham
RC stim protocol, Pre-LPS:
-8 sets of 30 pulses
-30Hz pulse rate (33.33ms inter-pulse interval)
-24s period between sets
-amplitude ramps across each set (520,650,780,910,1000,1160,1300,1420uA)
150ul blood samples @ pre-stim, 180m, 360m, 270m, 360m
"""



##by Ryan Neely 11/15/19

##full path to the excel data file
workbook = r"C:\Users\Ryan\OneDrive - Iota Bio\data\multiplex\11_15_19_rat.xlsx"

##information about the experiment. The top level are the experimental groups, 
# the second level is individual animals within that group, and
##the next level is samples within groups, and the last level is the sample names
##corresponding to the data in the workbook
experiment = { 
    "sham":{
        "sham1":{
            0:'X1', 90:'X2', 180:'X3', 270:'X4', 360:'X5'
        },
        "sham2":{
            0:'X6', 90:'X7', 180:'X8', 270:'X9', 360:'X10'
        }
    },
    "30Hz_rc":{
        "stim1":{
            0:'X11', 90:'X12', 180:'X13', 270:'X14', 360:'X15'
        },
        "stim2":{
            0:'X16', 90:'X17', 180:'X18', 270:'X19', 360:'X20'
        },
        "stim3":{
            0:'X21', 90:'X22', 180:'X23', 270:'X24', 360:'X25'
        },
        "stim4":{
            0:'X26', 90:'X27', 180:'X28', 270:'X29', 360:'X30'
        },
        "stim5":{
            0:'X31', 90:'X32', 180:'X33', 270:'X34', 360:'X35'
        },
        "stim6":{
            0:'X36', 90:'X37', 180:'X38', 270:'X39', 360:'X40'
        }
    } 

}