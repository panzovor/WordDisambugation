__author__ = 'E440'

from src.Preprocess.Duplicate import Dupicate
from src.Tools.SeperateWords import wordSegment as wordSegment
from src.Result.ModelEvalResult import ModelEvalResult

class Model:

    posCorpos=[]
    negCorpos=[]
    testData ={}
    wordTools = wordSegment()
    predictResult ={}
    summarizeInfo=""
    dupicate = Dupicate()
    eval = ModelEvalResult()

    def loadFiles(self,filepaths):
        for filepath in filepaths:
            if filepath.find("pos")>=0:
                self.posCorpos.extend(self.wordTools.readFile(filepath))
            elif filepath.find("neg")>=0:
                self.negCorpos.extend(self.wordTools.readFile(filepath))
            else:
                # print("other")
                for line in self.wordTools.readFile(filepath):
                    if(line.find("pos")>=0):
                        self.posCorpos.append(line)
                    else :
                        self.negCorpos.append(line)
        self.posCorpos = self.dupicate.dupicate(self.posCorpos)
        self.negCorpos = self.dupicate.dupicate(self.negCorpos)
        # print(self.posCorpos.__len__())
        # print(self.negCorpos.__len__())


    def loadTestData(self,filepath):
        for file in filepath :
            self.testData =self.testData.copy()
            self.testData.update(self.wordTools.readFileWityDict(filepath=file,seperator="\t"))


    def predict(self,line):
        return

    def evaluate(self):
        pos_hit =[]
        pos_mis =[]
        neg_hit =[]
        neg_mis =[]
        self.predictResult = {"pp":[], "pn" : [], "np": [], "nn": []}
        for testString in self.testData.keys():
            result = self.predict(testString)
            # print(self.testData[testString])
            if(self.testData[testString] == "pos" and result.predict ):
                result.classType = True;
                pos_hit.append(result.toString())
            elif (self.testData[testString] == "pos" and not result.predict ):
                result.classType = True;
                pos_mis.append(result.toString())
            elif (self.testData[testString] == "neg" and result.predict):
                result.classType = False;
                neg_hit.append(result.toString())
            else:
                result.classType = False;
                neg_mis.append(result.toString())

        # print(pos_hit.__len__())
        self.predictResult["pp"] = pos_hit
        self.predictResult["pn"] = pos_mis
        self.predictResult["np"] = neg_hit
        self.predictResult["nn"] = neg_mis
        return self.predictResult

    def evaluateModel(self):
        dicts = self.evaluate()

        result = "";
        prec = dicts["pp"].__len__()/(dicts["pp"].__len__()+dicts["np"].__len__())
        reca = dicts["pp"].__len__() / (dicts["pp"].__len__()+dicts["pn"].__len__())
        result+="\t\t\t\tpos\tneg\n"
        result+="pos(classfied):"+ str(dicts["pp"].__len__())+"\t"+str(dicts["np"].__len__())+"\n"
        result+="neg(classfied):"+ str(dicts["pn"].__len__()) +"\t"+ str(dicts["nn"].__len__())+"\n"
        result+="precision:" + str(prec)+"\n"
        result+="recall:" + str(reca)+"\n"
        result+="f-score:" +str(2*prec*reca/(prec+reca))+"\n"
        self.summarizeInfo = result
        self.eval.precision = prec
        self.eval.recall = reca
        self.eval.f_score = 2*prec*reca/(prec+reca)
        print(self.eval.toString())
        # return result
        return self.eval.toString()

    def saveEvaluationResult(self,filepath):
        content =""
        content+=self.summarizeInfo
        content+="漏判\n"
        for classifiedResult in self.predictResult["pn"]:
            content+= classifiedResult+"\n"
        content+="误判\n"
        for classifiedResult in self.predictResult["np"]:
            content+= classifiedResult+"\n"
        content+="pp\n"
        for classifiedResult in self.predictResult["pp"]:
            content+= classifiedResult+"\n"
        content+="nn\n"
        for classifiedResult in self.predictResult["nn"]:
            content+= classifiedResult+"\n"
        self.wordTools.saveIntoFile(filepath,content,"utf-8")
        return content
