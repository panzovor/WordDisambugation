__author__ = 'E440'
from src.Result.ClassifierResult import ClassfiierResult
from src.Model.Model import Model
from src.Model.TfIdfModels import TfidfModels
from src.Model.DiscriminationModel import DiscriminationModel

class MultiModels(Model):
    tfidf = TfidfModels()
    discrimination = DiscriminationModel()
    threshold = 0.8

    def buildModel(self,filepaths):
        self.tfidf.buildModel(filepaths)
        self.discrimination.buildModel(filepaths)

    def saveModel(self):
        self.tfidf.saveModelsDefault()
        self.discrimination.saveModelDefault()

    def loadModel(self):
        self.tfidf.loadModelDefault()
        self.discrimination.loadModelDefault()

    def predict(self,line):
        finalResult = ClassfiierResult()
        line  = line.replace("#","")
        finalResult.string = line
        value ={}
        words =self.wordTools.seperatewords(line)
        if set(words).intersection(set(self.wordTools.carwords)).__len__() == 0:
            finalResult.detailInfo ="not contains carwords"
            finalResult.predict = False
            return finalResult
        for word in words:
            posvalue = 1
            negvalue =1
            idf = 0.5
            if word in self.discrimination.words :
                posvalue = self.discrimination.words[word][0]
                if posvalue == 0: posvalue =1
                negvalue = self.discrimination.words[word][1]
                if negvalue == 0: negvalue=1
            if word in self.tfidf.idf:
                idf = self.tfidf.idf[word]
            tmp = (posvalue)/(negvalue)
            value[word] = idf * tmp
        finalResult.detailInfo = str(value)
        # print(value)
        count  =0
        for val in value:
            if value[val] >0.5: count+=1
        if count > value.__len__()*(self.threshold):
            finalResult.predict  = True
        else:
            finalResult.predict = False
        return finalResult


    def test(self,trainFiles,testFile):
        self.eval.className = "multi"
        self.eval.trainData = trainFiles
        self.eval.testData = [testFile]
        self.buildModel(filepaths=trainFiles)
        self.saveModel()
        self.loadModel()
        self.loadTestData(testFile)
        self.evaluateModel()


# testString =["车旺季，记者走访北京市部分4S店和亚"
#     ,"夺命铃身份被于贞发现后，只给了迷迭两"
#     ,"中以纯真却稳重的阳光性格获得了众多粉"
#     ,"高管们，想对一直野马财经，作为专注于"]
#
# filpaths = [ProjectDir.resourceDir+"Corpus\数据1.txt"
#             ]
#     # ,ProjectDir.resourceDir+"Corpus/noauto_filterResult.txt"
#     # ,ProjectDir.resourceDir+"Corpus\文章2000篇_扩充.txt"]
# testFile =ProjectDir.resourceDir+"Corpus\数据2.txt"
# mModel = MultiModels()
# mModel.buildModel(filpaths)
# print(type(mModel.discrimination.words))
# for string in testString:
#     result = mModel.predict(string)
#     print(result.predict)
#     print(result.toString())
