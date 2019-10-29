#10_25_19_1.py

##data structure that defines the multiplex assay experiment

"""
Notes:

experiment comparing sham stimulation to a 30Hz standardized RC. 
***NO LPS*** was used in these experiments!
Pro-inflammatory experiments:
all in-vivo
n = 5 stim, n = 3 sham
RC stim protocol:
-8 sets of 30 pulses
-30Hz pulse rate (33.33ms inter-pulse interval)
-24s period between sets
-amplitude ramps across each set (520,650,780,910,1000,1160,1300,1420uA)
150ul blood samples @ pre-stim, 45m, 90m, 135m, 180m
"""



##by Ryan Neely 10/25/19

##full path to the excel data file
workbook = r"C:\Users\Ryan\OneDrive - Iota Bio\data\multiplex\10_25_19_1.xlsx"

##information about the experiment. The top level are the experimental groups, 
# the second level is individual animals within that group, and
##the next level is samples within groups, and the last level is the sample names
##corresponding to the data in the workbook
experiment = { 
    "sham":{
        "10_23_19_IS1":{
            0:'X1', 45:'X2', 90:'X3', 135:'X4', 180:'X5'
        },
        "10_23_19_RN1":{
            0:'X6', 45:'X7', 90:'X8', 135:'X9', 180:'X10'
        },
        "10_24_19_IS1":{
            0:'X11', 45:'X12', 90:'X13', 135:'X14', 180:'X15'
        }
    },
    "30Hz_rc":{
        "10_23_19_RN2":{
            0:'X16', 45:'X17', 90:'X18', 135:'X19', 180:'X20'
        },
        "10_23_19_IS2":{
            0:'X21', 45:'X22', 90:'X23', 135:'X24', 180:'X25'
        },
        "10_24_19_IS2":{
            0:'X26', 45:'X27', 90:'X28', 135:'X29', 180:'X30'
        },
        "10_24_19_RN1":{
            0:'X31', 45:'X32', 90:'X33', 135:'X34', 180:'X35'
        },
        "10_24_19_RN2":{
            0:'X36', 45:'X37', 90:'X38', 135:'X39', 180:'X40'
        }
    } 

}