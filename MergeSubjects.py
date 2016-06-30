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

class MergeSubjects:
    
    subjectscores = pd.DataFrame()
    fd1=None
    fd2=None
    fd3=None
    fd4=None
    fd5=None
    fd6=None

    def __init__(self, master=None):   
                
        if sys.platform.startswith('win'):
            self.inputdir="<SubjectsMergeDirectory>"
            self.outputdir="<MOSDirectory>"
            self.paramsdir="<ParametersDirectory>"
        elif sys.platform.startswith('darwin'):
            self.inputdir="<SubjectsMergeDirectory>"
            self.outputdir="<MOSDirectory>"
            self.paramsdir="<ParametersDirectory>"
            
        self.packetheaderparams = pd.read_csv(self.paramsdir+"PacketHeaderInfo.csv")
        self.packetheadersubsetparams = pd.read_csv(self.paramsdir+"PacketHeaderInfoSubset.csv")
        self.bitstreamstats = pd.read_csv(self.paramsdir+"BitStreamStats.csv")
        self.bitstreamstatssubset = pd.read_csv(self.paramsdir+"BitStreamStatsSubset.csv")
        self.bitstreamstatsside = pd.read_csv(self.paramsdir+"BitStreamStatsSide.csv")
        
        allFiles = glob.glob(self.inputdir + "/Subject*.csv")
        print "Current Size: "+str(len(allFiles))
        #list_ = []
        for file_ in allFiles:
            df = pd.read_csv(file_,index_col=None, header=0)
            fileName=os.path.splitext(file_)[0]
            print "File Name: "+str(fileName)
            #df['Subject'] = fileName.split("Subject").pop()
            #print "Subject no: "+str(fileName.split("Subject").pop())
            #list_.append(df)
            self.subjectscores = pd.concat([self.subjectscores, df], ignore_index=True)
        
        #print str(self.subjectscores)
        
        shortFileName="MOSAndParametersCombined"
        shortFileNameWithHeader=shortFileName+"WithHeader"
        
        #All packet header info params + bit stream info params - general file name
        #We dont need this for python ML code
        shortFileName+=".csv"
        
        #All packet header info params + bit stream info params - general file name
        #Header is included in the file itself. This is needed for weka
        shortFileNameWithHeader+=".csv"
        
        #Only subset of packet headers and bit streams included. no general file Name
        #This is for python ML
        shortFileNameSubset="MOSAndSubset.csv"
        
        #Only subset of packet headers and bit streams included. no general file Name
        #This is for weka
        shortFileNameSubsetWithHeader="MOSAndSubsetWithHeader.csv"
        
        #Only general file Name and MOS included. This is fpr calculating the correlations.
        mosFileNameWithHeader="MOSandGeneralFileNameWithHeader.csv"
        
        #General File Name + Subset of packet headers + Side info for packet loss
        #This is for making visual graphs
        mosFileNameSideWithHeader="MOSAndSideWithHeader.csv"
        
        
        
        self.fd1 = open(self.outputdir+shortFileName,'w')
        self.fd2 = open(self.outputdir+shortFileNameWithHeader,'w')
        self.fd3 = open(self.outputdir+mosFileNameWithHeader,'w')
        self.fd4 = open(self.outputdir+shortFileNameSubset,'w')
        self.fd5 = open(self.outputdir+shortFileNameSubsetWithHeader,'w')
        self.fd6 = open(self.outputdir+mosFileNameSideWithHeader,'w')

        
    def findPacketHeaderParams(self, fileName):
        return self.packetheaderparams.loc[self.packetheaderparams['GeneralFileName'] == fileName].iloc[:,1:].to_csv(index = False, header=False, line_terminator="")

    def findPacketHeaderSubsetParams(self, fileName):
        return self.packetheadersubsetparams.loc[self.packetheadersubsetparams['GeneralFileName'] == fileName].iloc[:,1:].to_csv(index = False, header=False, line_terminator="")
        
    def findBitStreamStats(self, fileName):
        return self.bitstreamstats.loc[self.bitstreamstats['GeneralFileName'] == fileName].iloc[:,1:].to_csv(index = False, header=False, line_terminator="")
    
    def findBitStreamStatsSubset(self, fileName):
        return self.bitstreamstatssubset.loc[self.bitstreamstatssubset['GeneralFileName'] == fileName].iloc[:,1:].to_csv(index = False, header=False, line_terminator="")
    
    def findBitStreamStatsSide(self, fileName):
        return self.bitstreamstatsside.loc[self.bitstreamstatsside['GeneralFileName'] == fileName].iloc[:,1:].to_csv(index = False, header=False, line_terminator="")
        
    def writeAll(self, row):
        self.fd1.write(row)
        self.fd2.write(row)
        
    def writeHeader(self, header):
        self.fd2.write(header)
        
    def writeMOSAndFileName(self, row):
        self.fd3.write(row)

    def writeMOSandFileNameHeader(self, header):
        self.fd3.write(header)
        
    def writeAllSubset(self, row):
        self.fd4.write(row)
        self.fd5.write(row)
        
    def writeHeaderSubset(self, header):
        self.fd5.write(header)
        
    def writeMOSAndFileNameAndSide(self, row):
        self.fd6.write(row)

    def writeMOSandFileNameSideHeader(self, header):
        self.fd6.write(header)
        
    def calculateMOS(self):
        
        finalFrames = pd.DataFrame()
        
        #print "Subject Scores len: " + str(len(self.subjectscores))
        frame = self.subjectscores.sort(['GeneralFileName'])
        uniqueVals =unique(frame['GeneralFileName']) 
        for fileName in uniqueVals:
            
            fileFrames=frame[frame.GeneralFileName == fileName]
            MOS=float(sum(fileFrames.MOS))/len(fileFrames)
                
            mosFrame=pd.DataFrame(columns=['GeneralFileName','MOS'])
            mosFrame.loc[0]=[fileName, MOS]
            
            finalFrames=pd.concat([finalFrames, mosFrame], ignore_index=True)
        self.subjectscores=finalFrames
        #print str(self.subjectscores)
        
    def merge(self):

        self.calculateMOS()
        
        header="GeneralFileSize,GeneralDuration,GeneralOverallBitRate,GeneralFrameRate,GeneralFrameCount,GeneralStreamSize,GeneralStreamSizeProportion,GeneralDataSize,GeneralFooterSize,VideoDuration,VideoSourceDuration,VideoBitRate,VideoFrameRate,VideoFrameCount,VideoBits(Pixel*Frame),VideoStreamSize,VideoStreamSizeProportion,NR,KeyInt,KeyIntMin,QP,AudioDuration,AudioBitRate,AudioFrameCount,AudioStreamSize,AudioStreamSizeProportion,VideoOctetsReceived,VideoPacketsreceived,VideoPacketsLost,VideoPacketLossRate,AudioOctetsReceived,AudioPacketsReceived,AudioPacketsLost,AudioPacketLossRate,MOS\n"
        headerSubset="VideoFrameRate,NR,QP,VideoPacketLossRate,AudioPacketLossRate,MOS\n"
        mosHeader="GeneralFileName,MOS\n"
        mosSideHeader="VideoFrameRate,NR,QP,PacketLossRate,MOS\n"
        
        self.writeHeader(header)
        self.writeMOSandFileNameHeader(mosHeader)
        self.writeHeaderSubset(headerSubset)
        self.writeMOSandFileNameSideHeader(mosSideHeader)
        
        print "Data Size: "+str(len(self.subjectscores))
        for index, row in self.subjectscores.iterrows():
            
            fileName= row['GeneralFileName']
            MOS=str(float(row['MOS']))
            
            packetHeaderParamsRow=self.findPacketHeaderParams(fileName)
            bitStreamStatsRow=self.findBitStreamStats(fileName)
            
            self.writeAll(str(packetHeaderParamsRow)+","+str(bitStreamStatsRow)+","+str(MOS)+"\n")
            
            self.writeMOSAndFileName(str(fileName)+","+str(MOS)+"\n")
            
            packetHeaderParamsSubsetRow=self.findPacketHeaderSubsetParams(fileName)
            bitStreamStatsSubsetRow=self.findBitStreamStatsSubset(fileName)
            
            self.writeAllSubset(str(packetHeaderParamsSubsetRow)+","+str(bitStreamStatsSubsetRow)+","+str(MOS)+"\n")
            
            findBitStreamStatsSide=self.findBitStreamStatsSide(fileName)
            
            self.writeMOSAndFileNameAndSide(str(packetHeaderParamsSubsetRow)+","+str(findBitStreamStatsSide)+","+str(MOS)+"\n")
            
            
        self.fd1.close()
        self.fd2.close()
        self.fd3.close()
        self.fd4.close()
        self.fd5.close()
        self.fd6.close()
        
if __name__ == "__main__":
    mergeSubjects = MergeSubjects()
    mergeSubjects.merge()
    

