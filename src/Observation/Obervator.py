__author__ = 'E440'
#-*- coding: utf-8 -*-

from pylab import mpl
import operator
import numpy as np
import matplotlib.pyplot as plt
import pylab
import matplotlib.pyplot as plt;plt.rcdefaults()
import numpy as np
from pandas import Series
from src.Tools.SeperateWords import wordSegment
from ProjectDir import ProjectDir
from src.Preprocess.Duplicate import Dupicate
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText

class DataObservator:

    def __init__(self):
        self.extractor = ExtractSentenceFromText()
        self.wordTools = wordSegment();
        self.duplciate  = Dupicate()

    def loadData(self,filepath):
        data = self.wordTools.readFileWityDict(filepath=filepath,seperator="\t")
        return data

    def showDataInPict(self,filepath):
        data = self.loadData(filepath)
        words = [tmp for tmp in data.keys()]
        values = [float(data[tmp]) for tmp in words]
        ind = np.linspace(0,words.__len__()-1,words.__len__())
        fig = plt.figure(1)
        ax  = fig.add_subplot(111)
        ax.plot(ind,values)
        ax.set_xticklabels(words)
        plt.grid(True)
        plt.show()

    def showpicture(self,x,y,savepath=""):
        mpl.rcParams['font.sans-serif'] = ['FangSong']
        mpl.rcParams['axes.unicode_minus'] = False
        # menStd = (2, 3, 4, 1, 2)
        # womenStd = (3, 5, 2, 3, 3)
        fig = plt.figure()
        ind = np.arange(x.__len__())    # the x locations for the groups
        width = 0.35       # the width of the bars: can also be len(x) sequence

        p1 = plt.bar(ind, y.__getitem__(0), width, color='r')
        p2 = plt.bar(ind, y.__getitem__(1), width, color='b',
                     bottom=y.__getitem__(0))

        # plt.ylabel('Scores')
        plt.title(self.GetFileNameAndExt(savepath)[0])
        plt.xticks(ind + width/2., x,rotation=90)
        # plt.yticks(np.arange(0, 81, 10))
        plt.legend((p1[0], p2[0]), ('Pos', 'Neg'))
        # plt.show()

        if savepath !="":
            fig.savefig(savepath)
        plt.show()

    def GetFileNameAndExt(self,filename):
        import os
        (filepath,tempfilename) = os.path.split(filename);
        (shotname,extension) = os.path.splitext(tempfilename);
        return shotname,extension

    def showTrainDataInPict(self,filepath,cars):
        data  = self.loadData(filepath)
        posCount=0
        negCount=0
        for line in data:
            if cars in line and data[line] == "pos":
                posCount +=1
                print(line)
            elif cars in line and data[line] == "neg":
                negCount +=1
        print(str(posCount)+" " + str(negCount))

    def showTrainDataCarDistribution(self,filepath,savpath =""):
        corpus=[]
        for file in filepath:
            corpus.extend(self.wordTools.readFile(file))
        corpus = list(set(corpus))
        print(corpus.__len__())
        result ={}
        for line in corpus :
            cars = set()
            self.extractor.findCarWordsFromSentence(cars,line)
            if cars.__len__()>0:
                for car in cars:
                    if car not in result: result[car] =[0,0,0]
                    if "pos" in line:
                        result[car][0]+=1
                    elif "neg" in line:
                        result[car][1]+=1
                    result[car][2]+=1
        tmp  ={}
        for val in result :
            ## 出现次数大于10并且含有正负例
            # if result[val][0]+ result[val][1] >10 and result[val][0] >0 and result[val][1] >0:
            # if result[val][1] >2 and result[val][0] >2:
                if val not in tmp : tmp[val] = [0,0]
                tmp[val][0] = result[val][0]
                tmp[val][1] = result[val][1]
        self.wordTools.saveDictIntoFile(savpath+"all.txt",result,"utf-8")
        self.wordTools.saveDictIntoFile(savpath+"pic.txt",tmp,"utf-8")
        y = []
        tmp1 =[]
        tmp2 =[]
        for val in tmp:
            tmp1.append(tmp[val][0]/(tmp[val][0]+tmp[val][1]))
            tmp2.append(tmp[val][1]/(tmp[val][0]+tmp[val][1]))
        y.append(tmp1)
        y.append(tmp2)

        # print(y.__len__())
        self.showpicture(tmp.keys(),y,savpath)
        # self.showpicture(y,tmp.keys())

    def seperateCorpusByCars(self,corpusFile,resultfile):
        corpus =[]
        for file in corpusFile:
            corpus.extend(self.wordTools.readFile(file))
        result ={}
        for line in corpus:
            words = self.wordTools.seperatewords(line)
            for cars in self.wordTools.carwords:
                if cars in words:
                    if cars not in result:
                        result[cars] = []
                    result[cars].append(line)
        content =""
        for key in result.keys():
            for line in result[key]:
                content+=key
                content+="\t"
                content+=line+"\n"
        self.wordTools.saveIntoFile(resultfile,content)

    def getLocationForCars(self,words,word):
        location =-1;
        for i in range(words.__len__()):
            if words[i] == word:
                location = i
                break
        return location

    def tfPerCars(self,file,resultfile):
        data = self.wordTools.readFile(file)
        result ={}
        for line in data:
            if line.strip().__len__() == 0:
                continue
            tmp = line.split("\t")
            words = self.wordTools.seperatewords(tmp[1])
            location = self.getLocationForCars(words,tmp[0])
            for i in  range(words.__len__()):
                word = words[i]
                if word == tmp[0] or word.strip() == "":
                    continue
                key = tmp[0]+","+word+","+str(i-location)
                if key not in result:
                    result[key] = [0,0]
                if tmp[2] == "pos":
                    result[key][0]+=1
                else:
                    result[key][1]+=1
        content =""
        for key in result.keys():
            content+=key
            content+=","
            content+=str(result[key][0])
            content+=","
            content+=str(result[key][1])
            content+="\n"
        self.wordTools.saveIntoFile(resultfile,content)
        return result

    def duplicateRateBetweenTwoData(self,datafile):
        result = {}
        for data in datafile:
            if data not in result:
                result[data] = self.duplciate.dupicate(self.wordTools.readFile(data))

        observeresult ={}
        for data in datafile:
            if data not in observeresult:
                observeresult[data] = {}
            for data1 in datafile:
                if data1 not in observeresult[data]:
                    observeresult[data][data1] =0
                insect = set(result[data]).intersection(set(result[data1]))
                # print(insect)
                observeresult[data][data1] = insect.__len__()
        content =""
        for key in observeresult.keys():
            content+=self.GetFileNameAndExt(key)[0]+","
            for key1 in observeresult[key].keys():
                content+=str(observeresult[key][key1])+","
            content+="\n"
        print(content)

    def demo(self):
        dataFile =[
            # ProjectDir.resourceDir+"Corpus\数据1.txt"
            # ,ProjectDir.resourceDir+"Corpus\数据2-remove#.txt"
            # ,ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt"
            # ,ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"
            # ,ProjectDir.resourceDir+"Corpus\\20160906\汽车信息过滤句子语料-carwords.txt"
            # ProjectDir.resourceDir+"\Corpus\\alldata\\alldata.txt"
            # ,ProjectDir.resourceDir+"Corpus/seperate_allData_train.txt"
            # ,ProjectDir.resourceDir+"Corpus/seperate_allData_test.txt"
            # ,ProjectDir.resourceDir+"Corpus/combineallDataRestructByCar.txt"
            # ProjectDir.resourceDir+"Corpus/data1235/data/alldata.txt"
            ProjectDir.resourceDir+"Corpus/20161011/testData/20160902-5000.txt"
        ]
        savepath =ProjectDir.resourceDir+"observationResult\\汽车信息过滤句子语料-carwords.jpg"
        savepath =ProjectDir.resourceDir+"Corpus\data20160902\observationOfAllData\data1235.jpg"
        self.showTrainDataCarDistribution(dataFile,savepath)
        #

    def countCars(self):
        file = ProjectDir.resourceDir+"Corpus/数据2.txt"
        content = self.wordTools.readFile(file)
        result ={}
        for line in content:
            cars = set()
            self.extractor.findCarWordsFromSentence(cars,line)
            for car in cars:
                if car not in result.keys():
                    result[car] = [0,0,0]
                result[car][2]+=1
                if "pos" in line:
                    result[car][0]+=1
                else :
                    result[car][1]+=1
        for car in result.keys():
            print(car+","+str(result[car][0])+","+str(result[car][1])+","+str(result[car][2]))

observator = DataObservator()
# observator.dem


# observator.countCars()



# observator.duplicateRateBetweenTwoData(dataFile)


# corpus =[ProjectDir.resourceDir+"Corpus\数据1.txt",
#          # ProjectDir.resourceDir+"Corpus\数据2.txt",
#          ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt",
#          ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"]
# seperateFile = ProjectDir.resourceDir+"Corpus\seperateByCar1-3-5.txt"
# observator.seperateCorpusByCars(corpus,seperateFile)
# resultFile = ProjectDir.resourceDir+"Corpus\posnegPerCar1-3-5.txt"
# observator.tfPerCars(seperateFile,resultFile)


# filepath =ProjectDir.resourceDir+"Corpus\combineallDataRestructByCar.txt"
# savepath =ProjectDir.resourceDir+"observationResult\data5\ecombineallDataRestructByCar.jpg"
# # observator.showTrainDataInPict(filepath,"阳光")
# observator.showTrainDataCarDistribution(filepath,savepath)


