__author__ = 'E440'
import math
import random
from src.Preprocess.Duplicate import Dupicate
from ProjectDir import ProjectDir
from src.Tools.SeperateWords import wordSegment as wordSegment
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText

class DataSeperator():

    def __init__(self):
        self.extractor = ExtractSentenceFromText()
        self.wordTools = wordSegment()
        self.du = Dupicate()
        self.data =[]
        self.dataByCar ={}
        self.trainData_=[]
        self.testData_ = []

    def loadData(self,files):
        for file in files:
            self.data += self.wordTools.readFile(file)
            self.data = self.du.dupicate(self.data)

    def restructDataByCars(self,files,tmpfile):
        tmp=[]
        self.loadData(files)
        for line in self.data:
            if "#" in line:
                line  = line.replace("#","")
            cars = self.extractor.findCarWordsFromSentence(line)
            for car in cars:
                if car not in self.dataByCar:
                    self.dataByCar[car] ={}
                    self.dataByCar[car]["pos"] = []
                    self.dataByCar[car]["neg"] = []
                if "pos" in line:
                    self.dataByCar[car]["pos"].append(line)
                else:
                    self.dataByCar[car]["neg"].append(line)
                tmp+=(line)
        self.wordTools.saveIntoFile_list(tmpfile,tmp)
        # print(self.dataByCar["大众"]["pos"])

    def randomSeperateorByRate(self,rate):
        tmp =[]
        for key in self.dataByCar.keys():
            tmp.extend(self.dataByCar[key]["pos"])
            tmp.extend(self.dataByCar[key]["neg"])
        # tmp1=[]
        # for line in self.data:
        #     if line not in tmp:
        #         tmp1.append(line)
        # for strn in tmp1:
        #     print(strn)
        # print(set(tmp).__len__())
        for key in self.dataByCar.keys():
            if self.dataByCar[key]["pos"].__len__() >0:
                trainPosNum = int(self.dataByCar[key]["pos"].__len__()* rate)
                testPosNum = self.dataByCar[key]["pos"].__len__()-trainPosNum
                random.shuffle(self.dataByCar[key]["pos"])
                for i in range(testPosNum):
                    if self.dataByCar[key]["pos"][i] not in self.trainData_:
                        self.testData_.append(self.dataByCar[key]["pos"][i])
                for i in range(self.dataByCar[key]["pos"].__len__()):
                    if self.dataByCar[key]["pos"][i] not in self.testData_:
                        self.trainData_.append(self.dataByCar[key]["pos"][i])

            if self.dataByCar[key]["neg"].__len__()>0:
                trainNegNum = int(self.dataByCar[key]["neg"].__len__()* rate)
                testNegNum = self.dataByCar[key]["neg"].__len__()-trainNegNum

                random.shuffle(self.dataByCar[key]["neg"])

                for i in range(testNegNum):
                    if self.dataByCar[key]["neg"][i] not in self.trainData_:
                        self.testData_.append(self.dataByCar[key]["neg"][i])
                for i in range(trainNegNum,trainNegNum+testNegNum):
                    if self.dataByCar[key]["neg"][i] not in self.testData_:
                        self.trainData_.append(self.dataByCar[key]["neg"][i])
            self.trainData_ = self.du.dupicate(self.trainData_)
            self.testData_ = self.du.dupicate(self.testData_)
        tmp1 = self.trainData_.copy()
        tmp1.extend(self.testData_)
        for str in tmp:
            if str not in tmp1:
                print(str)


    def randomSeperatorByLabel(self,n):
        random.shuffle(self.data)
        result ={}
        result["pos"] = []
        result["neg"] =[]
        for line in self.data:
            if "\tpos" in line:
                result["pos"].append(line)
            if "\tneg" in line:
                result["neg"].append(line)
        neg_num = result["neg"].__len__()
        pos_num = result["pos"].__len__()
        pos = int(pos_num/n)+1
        neg = int(neg_num/n)+1
        trainData={}
        for i in range(n):
            trainData[i]=[]
        indexpos =0
        for i in range(result["pos"].__len__()):
            if trainData[indexpos].__len__() <pos:
                trainData[indexpos].append(result["pos"][i])
            else:
                # print(trainData[indexpos].__len__())
                indexpos+=1
                trainData[indexpos].append(result["pos"][i])


        indexneg =0
        # print(str(result["neg"].__len__()) +" "+str(neg))
        for i in range(result["neg"].__len__()):
            if trainData[indexneg].__len__() <pos+neg:
                trainData[indexneg].append(result["neg"][i])
            else:
                indexneg+=1
                trainData[indexneg].append(result["neg"][i])
                # print(trainData[indexneg].__len__())
        return trainData




def ranndomSeperateData(files,tmpfile,trainpath,testpath,rate):
    dataSeperator = DataSeperator()
    dataSeperator.restructDataByCars(files,tmpfile)
    dataSeperator.randomSeperateorByRate(rate)
    print("trainSize "+str(dataSeperator.trainData_.__len__()))
    print("testSize "+str(dataSeperator.testData_.__len__()))
    dataSeperator.wordTools.saveIntoFile_list(trainpath,dataSeperator.trainData_)
    dataSeperator.wordTools.saveIntoFile_list(testpath,dataSeperator.testData_)


def randomSeperateDataByLabels(files,n,saveinall,savefile):
    dataSeperator =DataSeperator()
    dataSeperator.loadData(files)
    traindata = dataSeperator.randomSeperatorByLabel(n)
    dataSeperator.wordTools.saveIntoFile_list(saveinall,dataSeperator.data)
    for i in range(traindata.__len__()):
        dataSeperator.wordTools.saveIntoFile_list(savefile+"file"+str(i),traindata[i])

files = [
    ProjectDir.resourceDir+"Corpus/数据1.txt"
    ,ProjectDir.resourceDir+"Corpus/数据2-remove#.txt"
    # ,ProjectDir.resourceDir+"Corpus/数据3.txt"
    # ,ProjectDir.resourceDir+"Corpus/数据5.txt"
    # ,ProjectDir.resourceDir+"Corpus/20160906/汽车信息过滤句子语料.txt"
]
# tmpfile = ProjectDir.resourceDir+"Corpus/combineallDataRestructByCar.txt"
# trainpath = ProjectDir.resourceDir+"Corpus/seperate_allData_train.txt"
# testpath  = ProjectDir.resourceDir+"Corpus/seperate_allData_test.txt"
# ranndomSeperateData(files,tmpfile,trainpath,testpath,0.8)
allfile = ProjectDir.resourceDir+"Corpus/data12/data/allcombined.txt"
seperatebylablefile = ProjectDir.resourceDir+"Corpus/crossvalidation/"
seperatebylablefile = ProjectDir.resourceDir+"Corpus/data12/data/"


# files = [ProjectDir.resourceDir+"Corpus/alldata/alldata.txt"]
randomSeperateDataByLabels(files,5,allfile,seperatebylablefile)
