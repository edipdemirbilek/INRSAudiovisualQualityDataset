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
import matplotlib
matplotlib.style.use('ggplot')

class GenerateGraphs:
    
    subjectFileName="SubjectsSummary.csv"
    mosAndSideFileName="MOSAndSideWithHeader.csv"
 

    def __init__(self, master=None):   
                
        if sys.platform.startswith('win'):
            self.subjectinputdir="<SubjectInputDir>"
            self.mosinputdir="<MOSInputDir>"
        elif sys.platform.startswith('darwin'):
            self.subjectinputdir="<SubjectInputDir>"
            self.mosinputdir="<MOSInputDir>"
        
        self.subjectsDF=pd.read_csv(self.subjectinputdir+self.subjectFileName,index_col=None, header=0)
        self.allDF=pd.read_csv(self.mosinputdir+self.mosAndSideFileName,index_col=None, header=0)
        

    def generate(self):

        score = self.subjectsDF[['Score','Id']]
        time = self.subjectsDF[['Time','Id']]
        correlation = self.subjectsDF[['Correlation','Id']]
        
        score.plot.box(y='Score', figsize=(1.5, 4), widths = 0.45);
        #plt.title("Accepted Subjective Scores")
        plt.ylabel('Subjective Score Count')
        plt.xlabel('All Observers')
        #plt.xticks(['Score'],['All Observers'])
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.show()
        
        time.plot.box(y='Time', figsize=(1.5, 4), widths = 0.45);
        #plt.title("Average Time to Rate")
        plt.ylabel('Time (s)')
        plt.xlabel('All Observers')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.show()
        
        correlation.plot.box(y='Correlation', figsize=(1.5, 4), widths = 0.45);
        #plt.title("Pearson Correlation")
        plt.ylabel('Pearson Correlation')
        plt.xlabel('All Observers')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.show()
        
        #plr.boxplot(by='PacketLossRate');
        self.allDF.boxplot(by='PacketLossRate',column=['MOS']);
        #plt.title("Packet Loss Rate vs MOS")
        plt.title("")
        plt.suptitle("")
        plt.ylabel('MOS')
        plt.xlabel('Packet Loss Rate (%)')
        plt.show()
        
        #fps.boxplot(by='VideoFrameRate');
        self.allDF.boxplot(by='VideoFrameRate',column=['MOS']);
        #plt.title("Video Frame Rate vs MOS")
        plt.title("")
        plt.suptitle("")
        plt.ylabel('MOS')
        plt.xlabel('Video Frame Rate (fps)')
        plt.show()
        
        #qp.boxplot(by='QP');
        self.allDF.boxplot(by='QP',column=['MOS']);
        #plt.title("Quantization Parameter vs MOS")
        plt.title("")
        plt.suptitle("")
        plt.ylabel('MOS')
        plt.xlabel('Quantization Parameter')
        plt.show()
        
        #nr.boxplot(by='NR');
        fig = self.allDF.boxplot(by='NR',column=['MOS']);
        #plt.title("Noise Reduction value vs MOS")
        #fig.set_axis_bgcolor('None')
        plt.title("")
        plt.suptitle("")
        plt.ylabel('MOS')
        plt.xlabel('Noise Reduction')
        plt.show()
        
        fig1, fig2, fig3 = self.subjectsDF.plot.bar(x='Id',subplots=True, figsize=(8, 6), legend='None', facecolor='k', edgecolor='k', width=0.25, alpha=0.8); 
        fig1.legend_.remove()
        fig2.legend_.remove()
        fig3.legend_.remove()
        fig1.set_ylabel('Score')
        fig2.set_ylabel('Time(s)')
        fig3.set_ylabel('Correlation')
        fig1.set_title("")
        fig2.set_title("")
        fig3.set_title("")
        plt.xlabel('Observer Id')
        

if __name__ == "__main__":
    generateGraphs = GenerateGraphs()
    generateGraphs.generate()
    

