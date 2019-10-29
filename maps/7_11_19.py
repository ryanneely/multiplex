##7_11_19.py

##data structure that defines the multiplex assay experiment

"""
Notes:

experiment comparing sham stimulation (no RC) to 
RC+100% stim, 150us PW, 30Hz, 40 mins, 10 mins post-LPS
"""



##by Ryan Neely 7/15/19

##full path to the excel data file
workbook = r"C:\Users\Ryan\OneDrive - Iota Bio\data\multiplex\7_11_19.xlsx"

##information about the experiment. The top level are the experimental groups, 
# the second level is individual animals within that group, and
##the next level is samples within groups, and the last level is the sample names
##corresponding to the data in the workbook
experiment = { 
    "sham":{
        "7_1_19_RN1":{
            0:'X1', 45:'X2', 90:'X3', 135:'X4', 180:'X5'
        },
        "6_21_19_RN1":{
            0:'X6', 45:'X7', 90:'X8', 135:'X9', 180:'X10'
        },
    },
    "RC/100%/40m/30Hz":{
        "5_30_19_RN1":{
            0:'X11', 45:'X12', 90:'X13', 135:'X14', 180:'X15'
        },
        "6_3_19_RN1":{
            0:'X16', 45:'X17', 90:'X18', 135:'X19', 180:'X20'
        },
        "6_4_19_RN1":{
            0:'X21', 45:'X22', 90:'X23', 135:'X24', 180:'X25'
        },
        "6_5_19_RN1":{
            0:'X26', 45:'X27', 90:'X28', 135:'X29', 180:'X30'
        },
        "6_6_19_RN1":{
            0:'X31', 45:'X32', 90:'X33', 135:'X34', 180:'X35'
        },
        "6_7_19_RN1":{
            0:'X36', 45:'X37', 90:'X38', 135:'X39', 180:'X40'
        },  
    } 
}