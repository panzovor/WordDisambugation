__author__ = 'E440'
import math
from src.Model.Model import Model
from src.Tools.SeperateWords import wordSegment as wordSegment
from src.Preprocess.Duplicate import Dupicate
from src.ForText.Tfidf import Tfidf
from ProjectDir import ProjectDir
from src.Result.ClassifierResult import ClassfiierResult


class VectorSpace( Model ):

    #义项矩阵：文档：以每个车型的正例为文档，负例为文档（）

    def __init__(self):
        self.weight=[1.0746,1.3616,1.7095,2.1832,2.8009,3.9798,4.005,2.9318,2.2870,1.8105,1.4379,1.1379]
        self.wordTool = wordSegment()
        self.du = Dupicate()
        self.vectorspaceModel ={}
        self.tfidf = Tfidf()
        self.datatrained ={}

        self.keyToline={}
        self.corpusMatrix =[]
        self.keyToMatrixLocaiton={}
        self.keyToVector ={}

    def buildKeyToLine(self,trainFile):
        data = []
        for file in trainFile:
            data.extend(self.wordTool.readFile(file))
        data  = self.du.dupicate(data)
        for line in data:
            words  = self.wordTool.seperatewords(line)
            for word in words:
                if word in self.wordTool.carwords:
                    if "pos" in line:
                        if word+" pos" not in self.keyToline.keys():
                            self.keyToline[word+" pos"] = ""
                        self.keyToline[word+" pos"]+= line+" "
                    if "neg" in line:
                        if word+" neg" not in self.keyToline.keys():
                            self.keyToline[word+" neg"] = ""
                        self.keyToline[word+" neg"]+= line+" "

    def buildCorpusMatrix(self):
        i =0
        for key in self.keyToline.keys():
            tmp_line = self.wordTool.seperatewords(self.keyToline[key].replace("\t",""))
            string=""
            for tmp_line_ in tmp_line:
                string+=tmp_line_+" "
            string = string.strip()
            if string == "":
                continue
            # print(string)
            self.keyToMatrixLocaiton[key]=i
            i+=1
            self.corpusMatrix.append(string)

    def buildKeytoVector(self):
        for key in self.keyToMatrixLocaiton.keys():
            loc= self.keyToMatrixLocaiton[key]
            # print(key)
            # print(self.tfidf.getVector(loc,self.corpusMatrix[loc]))
            self.keyToVector[key] = self.tfidf.getVector(loc,self.corpusMatrix[loc])

    def buildModel(self,trainFile):
        self.buildKeyToLine(trainFile)
        self.buildCorpusMatrix()
        # print(self.corpusMatrix)
        self.tfidf.getTfidf(self.corpusMatrix)
        self.buildKeytoVector()

    def getLineVector(self,words,word):
        result={}
        loc =0
        for word_ in words:
            if word_ == word:
                break;
            else:
                loc+=1
        for i in range(len(words)):
            if i !=loc:
                if i-loc<0 and i-loc>-7:
                    result[words[i]] = self.weight[i-loc+6]
                elif i-loc >0 and i-loc<7:
                    result[words[i]] = self.weight[i-loc+5]
                else:
                    result[words[i]] = 0.5
        return result

    def getLengthOfVector(self,words):
        value =0.0
        for word in words.keys():
            value+= words[word]**2
        value = math.sqrt(value)
        if value ==0:
            return 1
        return value

    def predict(self,line):
        cresult = ClassfiierResult()
        detailInfo = ""
        cresult.string = line
        words = self.wordTool.seperatewords(line)
        carword = []
        result ={}
        for word in words:
            if word in self.wordTool.carwords:
                carword.append(word)
        for car in carword:
            result[car]= False
            keyTolineVector = self.getLineVector(words,car)
            tmp_pos_result =0.0
            tmp_neg_result =0.0
            if car+" pos" not in self.keyToVector:
                detailInfo+= car+"\tnot in pos"
                continue
            if car+" neg" not in self.keyToVector:
                detailInfo+= car+"\tnot in neg"
                result[car] = True
                continue

            for word in words:
                if word != car:
                    tivalue_pos =0.0
                    tivalue_neg =0.0
                    if word in self.keyToVector[car+" pos"]:
                        tivalue_pos = self.keyToVector[car+" pos"][word]
                    if word in self.keyToVector[car+" neg"]:

                        tivalue_neg = self.keyToVector[car+" neg"][word]
                    tmp_pos_result+= tivalue_pos* keyTolineVector[word]
                    tmp_neg_result+= tivalue_neg* keyTolineVector[word]
            if tmp_pos_result>tmp_neg_result:
                # print(car+" "+str(tmp_pos_result)+" "+str(tmp_pos_result))
                result[car] = True
            detailInfo+= car+":"+str(tmp_pos_result)+","+str(tmp_neg_result)+"\t"
        cresult.detailInfo =detailInfo
        cresult.predict = False
        # print(result)
        for car in result.keys():
            if result[car] == True:
                cresult.predict =True
                break
        return cresult

    def test(self,trainFile,testFile):
        self.eval.className = "vectopspace"
        self.eval.trainData = trainFile
        self.eval.testData = testFile
        self.buildModel(trainFile)
        self.loadTestData(testFile)
        return  self.evaluateModel()

    def demo(self):
        vectspace = VectorSpace()
        trainFile =[
            ProjectDir.resourceDir+"Corpus\seperate_allData_train.txt"
        ]
        vectspace.buildModel(trainFile)
        # line = "原地产 陈佳乐： 优化行 neg"
        # print(vectspace.predict(line).toString())
        # line = "去年江铃福特推出首款乘用车撼路者之后再推一款全新MPV——途睿欧	pos"
        # print(vectspace.predict(line).toString())
        line = "宝马对3系的悬架系统作了不少改进 pos"
        print(vectspace.predict(line).toString())

# vect= VectorSpace()
# vect.demo()
