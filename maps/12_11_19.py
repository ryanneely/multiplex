#120_11_19.py

##data structure that defines the multiplex assay experiment

"""
Notes:

experiment comparing sham stimulation to a 30Hz, 40m stim using 4 1-hr timepoints. 
Pro-inflammatory experiments:
all in-vivo
n = 4 stim, n = 4 sham
40m 30Hz stim protocol
Poly I:C injection occurred 30m into stimulation (0.5mg/kg)
150ul blood samples @ pre-stim, 60m, 120m, 180m, 240m
"""



##by Ryan Neely 12/11/19

##full path to the excel data file
workbook = r"C:\Users\Ryan\OneDrive - Iota Bio\data\multiplex\12_11_19_rat_ifn-g.xlsx"

##information about the experiment. The top level are the experimental groups, 
# the second level is individual animals within that group, and
##the next level is samples within groups, and the last level is the sample names
##corresponding to the data in the workbook



experiment = { 
    "sham":{
        "11_20_19_IS2":{
            0:'X21', 60:'X22', 120:'X23', 180:'X24', 240:'X25'
        },
        "11_18_19_IS2":{
            0:'X6', 60:'X7', 120:'X8', 180:'X9', 240:'X10'
        },
        "11_22_19_IS1":{
            0:'X31', 60:'X32', 120:'X33', 180:'X34', 240:'X35'
        },
        "11_22_19_IS2":{
            0:'X36', 60:'X37', 120:'X38', 180:'X39', 240:'X40'
        }
    },
    "30Hz_rc":{
        "11_18_19_IS1":{
            0:'X1', 60:'X2', 120:'X3', 180:'X4', 240:'X5'
        },
        "11_19_19_IS1":{
            0:'X11', 60:'X12', 120:'X13', 180:'X14', 240:'X15'
        },
        "11_20_19_IS1":{
            0:'X16', 60:'X17', 120:'X18', 180:'X19', 240:'X20'
        },
        "11_21_19_IS1":{
            0:'X26', 60:'X27', 120:'X28', 180:'X29', 240:'X30'
        }
    } 

}