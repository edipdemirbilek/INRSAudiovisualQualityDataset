import pandas as pd
import sys
import glob
import os
import os.path
from numpy import unique
from numpy import mean
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
from collections import OrderedDict
import operator

class CalculateCorrelation:
    
    subjectFileName="Subject30.csv"
    allFileName="MOSandGeneralFileNameWithHeader.csv"
 

    def __init__(self, master=None):   
                
        if sys.platform.startswith('win'):
            self.subjectinputdir="C:/Users/edip.demirbilek/Dropbox/INRS/2016Winter/ACRScores/SubjectMerged/"
            self.allinputdir="C:/Users/edip.demirbilek/Dropbox/INRS/2016Winter/ACRScores/MOS/"
        elif sys.platform.startswith('darwin'):
            self.subjectinputdir="/Users/edipdemirbilek/Dropbox/INRS/2016Winter/ACRScores/SubjectMerged/"
            self.allinputdir="/Users/edipdemirbilek/Dropbox/INRS/2016Winter/ACRScores/MOS/"
        
        self.subjectDF=pd.read_csv(self.subjectinputdir+self.subjectFileName,index_col=None, header=0)
        self.allDF=pd.read_csv(self.allinputdir+self.allFileName,index_col=None, header=0)
        

    def calculate(self):
        #print self.subjectDF
        #print self.allDF
        ind = self.allDF['GeneralFileName'].isin(self.subjectDF['GeneralFileName'])
        
        #print ind 
        
        allSortedDF=self.allDF[ind].sort(['GeneralFileName'])
        subjectSortedDF=self.subjectDF.sort(['GeneralFileName'])
        
        result = pd.merge(allSortedDF, subjectSortedDF, on=['GeneralFileName', 'GeneralFileName'])

        print str(len(subjectSortedDF))+","+str(result['MOS_x'].corr(result['MOS_y']))

        
if __name__ == "__main__":
    calculateCorrelation = CalculateCorrelation()
    calculateCorrelation.calculate()
    

