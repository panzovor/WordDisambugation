__author__ = 'E440'
from src.Model.Model import Model
from src.Observation.Obervator import DataObservator
from ProjectDir import ProjectDir
from src.Result.ClassifierResult import ClassfiierResult

class TFPerCarModel(Model):

    def __init__(self):
        self.data ={}
        self.observator = DataObservator()
        self.normalwords = {}
        self.weight=[1.0746,1.3616,1.7095,2.1832,2.8009,3.9798,4.005,2.9318,2.2870,1.8105,1.4379,1.1379]


    def buildModel(self,corpus):
        middleFile = ProjectDir.resourceDir+"TfPerCarModel\seperateByCar.txt"
        self.observator.seperateCorpusByCars(corpus,middleFile)
        resultFile = ProjectDir.resourceDir+"TfPerCarModel\posnegPerCar.txt"
        self.data = self.observator.tfPerCars(middleFile,resultFile)
        self.buildNormalWords()

    def buildNormalWords(self):
        for string in self.data.keys():
            carinfo = string.split(",")
            key = carinfo[1]+","+carinfo[2]
            if self.data[string][0] + self.data[string][1] <4:
                continue
            if key not in self.normalwords:
                self.normalwords[key] = [self.data[string][0],self.data[string][1]]
            else:
                self.normalwords[key][0] += self.data[string][0]
                self.normalwords[key][1] += self.data[string][1]

    def loadModel(self):
        middleFile = ProjectDir.resourceDir+"TfPerCarModel\seperateByCar.txt"
        resultFile = ProjectDir.resourceDir+"TfPerCarModel\posnegPerCar.txt"
        self.data = self.observator.tfPerCars(middleFile,resultFile)
        self.buildNormalWords()

    def getCarWords(self,words):
        result =[]
        for car in self.observator.wordTools.carwords:
            for i in range(words.__len__()):
                if words[i] in car:
                    result.append(i)
        return result


    def predict(self,line):
        line = line.replace("#","")
        result = ClassfiierResult()
        words  = self.observator.wordTools.seperatewords(line)
        carWords = self.getCarWords(words)
        result.string = line
        if carWords.__len__() == 0:
            result.detailInfo="no car word"
            result.predict  =False
            return  result
        for index in carWords:
            value =[0.0,0.0]
            detailString =""
            for i in range(words.__len__()):
                if i!=index:
                    key  = words[index]+","+ words[i]+","+str(i-index)
                    # print(key)
                    if key in self.data:
                        if (i-index)<6 and (i-index)>=-6:
                            posvalue = (self.data[key][0]+1)/(self.data[key][0]+self.data[key][1]+1)
                            negvalue = 1-posvalue
                            detailString+=key+":"
                            value[0] += self.weight[i-index+6]*posvalue
                            value[1] += self.weight[i-index+6]*negvalue
                            detailString+=str(value[0])+","+str(value[1])+" "
                            # print(value[0])
                            # print(value[1])
                    else:
                        key = words[i]+","+str(i-index)
                        if key in self.normalwords:
                            posvalue = (self.normalwords[key][0]+1)/(self.normalwords[key][0]+self.normalwords[key][1]+1)
                            negvalue = 1- posvalue
                            detailString += key+":"
                            if i-index+6>=0 and i-index+6<12:
                                value[0] += self.weight[i-index+6]*posvalue
                                value[1] += self.weight[i-index+6]*negvalue
                            # else:
                            #     value[0] += 0.4*posvalue
                            #     value[1] += 0.4*negvalue
                            detailString+=str(value[0])+","+str(value[1])+" "
                            # print(value[0])
                            # print(value[1])

            result.detailInfo = detailString
            if value[0] > value[1]:
                result.predict = True
            else:
                result.predict = False
        return result

    def test(self,trainFile,testFile):
        self.eval.className = "tfpercar"
        self.eval.trainData = trainFile
        self.eval.testData = testFile
        self.buildModel(trainFile)
        self.loadTestData(testFile)
        return  self.evaluateModel()

    def buildModelDemo(self):
        corpus =[
        #          ProjectDir.resourceDir+"Corpus\数据1.txt",
        #          ProjectDir.resourceDir+"Corpus\数据2.txt",
        #          ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt",
        #          # ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"
                 ProjectDir.resourceDir+"Corpus\crossvalidation\\file0"
        ]
        seperateFile = ProjectDir.resourceDir+"Corpus\seperateByCar4test.txt"
        self.buildModel(corpus)
        print(self.predict("贴着别克的标志并且很便宜，于是国人就把它抢疯了	pos").toString())

# model = TFPerCarModel()
# model.buildModelDemo()
