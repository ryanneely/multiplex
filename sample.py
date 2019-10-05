##sample.py

##defines structure of Sample object and analyte sub-objects, and 
##creates functions for populating the data fields

##by Ryan Neely 7/11/19

import numpy as np
import xlrd

class Sample:
    """
    Sample class. contains info about the sample, and acts as a
    container for analyte objects containing analyte data
    """
    def __init__(self,name,group_name,sample_id,wb):
        self.name = name ##the name of the sample (i.e. t=45)
        self.group_name = group_name ##name of the group that this sample belongs to (i.e. 'animal 4')
        self.sample_id = sample_id ##ID that MAGPIX associates with the sample, ex 'X3'
        self.wells = [] ##list of wells that contain this sample (could be 1 or more if duplicates were used)
        self.type = None ##defines the type of sample, from 'std', 'test', or 'blank'
        self.dilution = 1
        self.analyte_names = []
        self.analytes = [] ##list of analyte objects belonging to this sample
        self.add_wells(wb)
        self.get_type()
        self.get_dilution(wb)
        self.get_analyte_names(wb)
        for an in self.analyte_names:
            self.analytes.append(Analyte(an,self.wells,wb))

    def find_rows(self,sheet):
        """
        Finds row addresses that contain information about this sample
        """
        ##get the first column, and find the index corresponding to the sample ID
        start,stop = col_idx(sheet) ##row indices of the relevant data block
        id_col = np.array([x.value for x in sheet.col(0)[start:stop]]) ##sample ID data
        rows = np.where(id_col==self.sample_id)[0]
        assert rows.size > 0, "Unable to locate samples with ID# "+self.sample_id
        return rows+start ##this index will be the correct index for the full sheet
    
    def add_wells(self,wb):
        """
        Adds well addresses. 
        Args:
            -wb: xlrd workbook object
        """
        ##we can use an sheet here, so just take the first one
        sheet = wb.sheet_by_index(0)
        rows = self.find_rows(sheet)
        well_col = [x.value for x in sheet.col(1)] #well ID data
        for r in rows:
            self.wells.append(well_col[r])
    
    def get_dilution(self,wb):
        """
        Returns the dilution of this sample
        """
        sheet = wb.sheet_by_name("Dilution")
        rows = self.find_rows(sheet)
        ##I'm assuming that dilution has to be the same for all analytes. 
        col = np.array([x.value for x in sheet.col(2)])
        dilutions = col[rows]
        ##warn if duplicates are not the same dilution
        if not np.unique(dilutions).size == 1:
            print("Warning: "+self.name+" has duplicates with different dilution values")
        self.dilution = float(dilutions[0])
    
    def get_analyte_names(self,wb):
        """
        Returns a list of full analyte names used in the analysis
        Args:
            -wb: workbook object
        """
        ##we can use an sheet here, so just take the first one
        sheet = wb.sheet_by_index(0)
        ##TODO: add some error checking here. depending on the metadata entered into 
        ##the reader software, you could have more or less lines. Therefore in the line
        ##below, row(9) might not be correct. Need some way to find which row to use.
        names = np.array([x.value for x in sheet.row(9) if not x.value==xlrd.empty_cell.value])
        ##not sure the best way to error-check this, but at least make sure the list isn't empty:
        assert names.size > 0, "No analytes found"
        self.analyte_names = names

    def get_type(self):
        
        """
        looks at the sample id defined for this sample and determins the type
        """
        if "X" in self.sample_id:
            self.type = 'test'
        elif "B" in self.sample_id:
            self.type = 'blank'
        elif "S" in self.sample_id:
            self.type = 'std'
        else:
            print("Sample type undefined!")
        
class Analyte:
    """
    Analyte class contains data from a single analyte 
    for a single sample.
    """
    def __init__(self,name,wells,wb):
        self.name = name ##should be the full name of the analyte as listed in the data file
        self.wells = wells ##list of wells to check for data
        self.outlier = [] ##boolean is outlier
        self.fl_raw = [] ##raw fluorescence value
        self.fl = [] ##fluorescence with background fluorescence subtracted
        self.c_obs = [] ##observed concentration based on std curve
        self.c_exp = [] ##expected concentration (only applies to std wells)
        self.props = ['Outlier','FI','FI - Bkgd','Obs Conc', 'Exp Conc'] ##the corresponding shet names containing the data
        self.get_data(wb)

    def get_data(self,wb):
        ##populate the data from the workbook
        vals = [self.outlier,self.fl_raw,self.fl,self.c_obs,self.c_exp]
        for val,p in zip(vals,self.props):
            sheet = wb.sheet_by_name(p) ##the sheet for this analyte
            analyte_names = np.array([x.value for x in sheet.row(9)]) ##analyte row headings
            col = np.where(analyte_names==self.name)[0] ##column with data for this analyte
            assert len(col) > 0, "Can't find {} in sheet {}.".format(self.name,p)
            if len(col) > 1:
                print("Warning: found two entries for {} in sheet {}.".format(self.name,p))
            col=col[0]
            ##now we can get only the column chunk that contains the single-well data      
            start,stop = col_idx(sheet)
            data = sheet.col(col)[start:stop]
            well_ids = sheet.col(1)[start:stop]
            for i,w in enumerate(well_ids):
                if w.value in self.wells:
                    val.append(data[i].value)

##helper functions down here

def col_idx(sheet):
    """
    The sheet created by MAGPIX usually has two blocks of data, with the
    first one containing the average values of each sample and the second
    containing the individual well values. We want to get the indices of 
    the data block containing only the individual well values. 
    Args:
        -sheet: the xlrd sheet object
    Returns:
        -idx: row indices for the individual well data only
    """
    #we are making several assumtions about the structure of the 
    ##data, so we will go through a few checks to make sure our assumtions hold. 
    ##first find the indices corresponding to the start of each data block
    col = np.array([x.value for x in sheet.col(1)])
    block_starts = np.where(col=='Well')[0] ##the index of the column headings
    try:
        start = block_starts[1]+1
    except IndexError:
        start = block_starts[0]+1
        print("Warning: single data block detected")
    ##There are usually empty rows at the end of this column, don't include them
    stop = min(np.where(col[start:]=='')[0])+start
    ##do some error checking; if we did everything correctly, each element in col
    ##from start:stop should be a length-2 string (ex: "A5")
    length_checker = np.vectorize(len)
    lengths = length_checker(col[start:stop])
    assert not(np.any(lengths>3) or np.any(lengths<2)), "Error: did not return single column indices"
    return start,stop


    
    

    