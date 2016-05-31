import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys
import os.path


def zeroDimPlot():
    raise Exception("Not implemented yet")
    
def oneDimPlot(data, path,label, xlabel,ylabel, ylim, std=[]):
    imgName = os.path.realpath(path)
    
    if(len(std)!=0):
        plt.errorbar(range(0, len(data)),data,yerr=std,xerr=[0]*len(data),lw=1,label=label)
    else:
        plt.plot(range(0, len(data)),data,lw=1,label=label)
        
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(label)
    plt.ylim(ylim[0],ylim[1])
    plt.savefig(imgName)
    plt.show()

"""example of data

data={mlp:{
mean:[1,2,3,4,5],
std:None
},
wide:{
mean:[2,3,1,4],
std:[0.5,0.5,0.6,0.6]
}}
"""
def multiOneDimPlot(data,xlabel,ylabel,ylim,path):
    color = ["r","g","b","k"]
    imgName = os.path.realpath(path)
    i=0
    hand = []
    for dict_ in data:

        name = dict_["name"]
        mean = dict_["mean"]
        std = dict_["std"]

        
        if(len(std)!=0):
            plt.errorbar(range(0, len(mean)),mean,color=color[i],yerr=std,lw=1,label=name)
        hand.append(plt.plot(range(0, len(mean)),mean,color=color[i],lw=1,label=name)[0])

        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(name)
        
        i+=1
        i%=len(color)
    
    plt.legend(handles=hand)
    plt.ylim(ylim[0],ylim[1])   
    plt.savefig(imgName)
    plt.show()
    
def twoDimPlot():
    raise Exception("Not implemented yet")