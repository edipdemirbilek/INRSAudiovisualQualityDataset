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

class PrepareBitstreamStats:
    
    fd1=None
    fd2=None    

    def __init__(self, master=None):   
                
        if sys.platform.startswith('win'):
            self.inputdir="<StatsDirectory>"
            self.outputdir="<ParametersDirectory>"
        elif sys.platform.startswith('darwin'):
            self.inputdir="<StatsDirectory>"
            self.outputdir="<ParametersDirectory>"
        
        shortFileName="BitStreamStats.csv"
        self.fd1 = open(self.outputdir+shortFileName,'w')

    def writeAll(self, row):
        self.fd1.write(row)
        
    def writeHeader(self, header):
        self.fd1.write(header)
        
    def prepare(self):

        header="GeneralFileName,VideoOctetsReceived,VideoPacketsreceived,VideoPacketsLost,VideoPacketLossRate,AudioOctetsReceived,AudioPacketsReceived,AudioPacketsLost,AudioPacketLossRate\n"
        
        self.writeHeader(header)
        
        allFiles = glob.glob(self.inputdir + "*.csv")
        print "Current Size: "+str(len(allFiles))

        for file_ in allFiles:
            df = pd.read_csv(file_,index_col=None, header=None)
            baseName=os.path.basename(file_)
            fileName=os.path.splitext(baseName)[0]
            #print "File Name: "+str(fileName)
            
            videoOctetsReceived=""
            videoPacketsReceived=""
            videoPacketsLost=""
            videoPacketLossRate=""
            audioOctetsReceived=""
            audioPacketsReceived=""
            audioPacketsLost=""
            audioPacketLossRate=""
                
            for index, row in df.iterrows():

                sessionInfo=int(row[0].split(':')[1])
                
                if sessionInfo == 0: #video stream
                    #print "Found Video Stream."
                    videoOctetsReceived=row[12].split(':')[1].strip()
                    videoPacketsReceived=row[13].split(':')[1].strip()
                    videoPacketsLost=row[15].split(':')[1].strip()
                    videoPacketLossRate=str(round((float(videoPacketsLost)*100)/(float(videoPacketsLost)+float(videoPacketsReceived)),2))
                elif sessionInfo == 1: #audio stream
                    #print "Found Audio Stream."
                    audioOctetsReceived=row[12].split(':')[1].strip()
                    audioPacketsReceived=row[13].split(':')[1].strip()
                    audioPacketsLost=row[15].split(':')[1].strip()
                    audioPacketLossRate=str(round((float(audioPacketsLost)*100)/(float(audioPacketsLost)+float(audioPacketsReceived)),2))
                else: #do nothing, this is not supposed to happen
                    print "Inccorect session info retrieved: "+str(sessionInfo)
                
            row=fileName+","+videoOctetsReceived+","+videoPacketsReceived+","+videoPacketsLost+","+videoPacketLossRate+","+audioOctetsReceived+","+audioPacketsReceived+","+audioPacketsLost+","+audioPacketLossRate+"\n"
            print row

            self.writeAll(row)

        self.fd1.close()
        
if __name__ == "__main__":
    prepareBitstreamStats = PrepareBitstreamStats()
    prepareBitstreamStats.prepare()
    

