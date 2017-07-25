__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment as wordSegment
import random
class TrainDataGenerator:

    posCorpos =[]
    negCorpos =[]

    posTrainData =[]
    negTrainData =[]

    posTestData = []
    negTestData =[]
    wordTool = wordSegment()
    def loadPos(self,file):
        self.posCorpos +=  self.wordTool.readFile(file)
    def loadNeg(self,file):
        self.negCorpos += self.wordTool.readFile(file)
    def randomSeperator(self,rate):
        posSize = self.posCorpos.__len__()
        negSize = self.negCorpos.__len__()
        posNum = int(posSize* rate)
        negNum = int(negSize* rate)
        used = []
        self.posTrainData = random.sample(self.posCorpos,posNum)
        self.negTrainData = random.sample(self.negCorpos,negNum)
        self.posTestData = list(set(self.posCorpos).difference(set(self.posTrainData)))
        self.negTestData = list(set(self.negCorpos).difference(set(self.negTrainData)))
    def saveTrainTestData(self,trainFile,testFile):
        trainData=[]
        testData =[]
        for line in self.posTrainData:
            trainData.append(line)
        for line in self.negTrainData:
            trainData.append(line)
        for line in self.posTestData:
            testData.append(line)
        for line in self.negTestData:
            testData.append(line)
        self.wordTool.saveIntoFile_list(trainFile,trainData)
        self.wordTool.saveIntoFile_list(testFile,testData)

    def generate(self,posfile,negfile,rate , trainFile,testFile):
        self.loadPos(posfile)
        self.loadNeg(negfile)
        self.randomSeperator(rate)
        self.saveTrainTestData(trainFile,testFile)

dataGenerator = TrainDataGenerator()
posfile =""
negfile =""
rate = 0.8;
trainFile =""
testFile =""
dataGenerator.generate()