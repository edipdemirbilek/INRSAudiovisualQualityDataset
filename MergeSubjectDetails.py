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

class MergeSubjectDetails:
    
    subjectScoresFirstHalf = pd.DataFrame()
    subjectScoresSecondHalf = pd.DataFrame()
    fd1=None
    fd2=None    
    subjectName="Subject31"
    
    def __init__(self, master=None):   
                
            
        if sys.platform.startswith('win'):
            self.inputdir="<SubjectsDetailDirectory>"
            self.outputdir="<SubjectsMergeDirectory>"
        elif sys.platform.startswith('darwin'):
            self.inputdir="<SubjectsDetailDirectory>"
            self.outputdir="<SubjectsMergeDirectory>"

        subjectFilesFirstHalf = [self.inputdir + "/"+self.subjectName+"Session1Part1.csv", 
                        self.inputdir + "/"+self.subjectName+"Session1Part2.csv",
                        self.inputdir + "/"+self.subjectName+"Session2Part1.csv",
                        self.inputdir + "/"+self.subjectName+"Session2Part2.csv"]
        for file_ in subjectFilesFirstHalf:
            df = pd.read_csv(file_,index_col=None, header=0)
            self.subjectScoresFirstHalf = pd.concat([self.subjectScoresFirstHalf, df], ignore_index=True)
        print("subjectFilesFirstHalf len: "+str(len(self.subjectScoresFirstHalf)))
            
        subjectFilesSecondHalf = [self.inputdir + "/"+self.subjectName+"Session1Part3.csv", 
                        self.inputdir + "/"+self.subjectName+"Session1Part4.csv",
                        self.inputdir + "/"+self.subjectName+"Session2Part3.csv",
                        self.inputdir + "/"+self.subjectName+"Session2Part4.csv"]
        for file_ in subjectFilesSecondHalf:
            df = pd.read_csv(file_,index_col=None, header=0)
            self.subjectScoresSecondHalf = pd.concat([self.subjectScoresSecondHalf, df], ignore_index=True)
        print("subjectScoresSecondHalf len: "+str(len(self.subjectScoresSecondHalf)))

        subjectFileName=self.subjectName+".csv"
        subjectSummaryFile="Summary"+self.subjectName+".csv"

        self.fd2 = open(self.outputdir+subjectFileName,'w')
        self.fd3 = open(self.outputdir+subjectSummaryFile,'w')

    def writeAll(self, row):
        self.fd2.write(row)
        
    def writeHeader(self, header):
        self.fd2.write(header)
        
    def writeSummaryHeader(self, header):
        self.fd3.write(header)
        
    def appendSummary(self, row):
        self.fd3.write(row)
        
    def findMeanTime1(self):
        return int(mean(self.subjectScoresFirstHalf.iloc[:,2]))
        
    def findMeanTime2(self):
        return int(mean(self.subjectScoresSecondHalf.iloc[:,2]))
        
    def findACRScore(self, fileName):
        return self.subjectScoresSecondHalf.loc[self.subjectScoresSecondHalf['GeneralFileName'] == fileName].iloc[:,1]
     
    def merge(self):

        header="GeneralFileName,MOS\n"
        self.writeHeader(header)
        unmatchingACRValues=0
        
        for index, row in self.subjectScoresFirstHalf.iterrows():
            fileName= row['GeneralFileName']
            acrScore1=int(row['ACRScore'])
            acrScore2=int(self.findACRScore(fileName))
            
            if abs(acrScore1-acrScore2)<2:
                mos=float(acrScore1+acrScore2)/2
                #print "ACR1: "+str(acrScore1) + " ACR2: "+str(acrScore2)+ " MOS: "+str(mos)
                self.writeAll(fileName+","+str(mos)+"\n")
            else:
                print "Ignoring, difference between two ACR scores is more than 1."
                print "FileName: "+fileName
                print "ACR Score1: "+str(acrScore1)
                print "ACR Score2: "+str(acrScore2)
                unmatchingACRValues+=1
        
        summaryHeader="Subject,Size,Time\n"
        self.writeSummaryHeader(summaryHeader)
        
        meanTime1=self.findMeanTime1()
        meanTime2=self.findMeanTime2()        
        meanTime=int((meanTime1+meanTime2)/2)
        print "MeanTim1: "+str(meanTime)
        
        size=len(self.subjectScoresFirstHalf)-unmatchingACRValues
        print "Size: "+str(size)
        
        self.appendSummary(self.subjectName+","+str(size)+","+str(meanTime)+"\n")
        
        #self.fd1.close()
        self.fd2.close()
        self.fd3.close()
        
if __name__ == "__main__":
    mergeSubjectDetails = MergeSubjectDetails()
    mergeSubjectDetails.merge()
    

