__author__ = 'E440'
from src.Result.ClassifierResult import ClassfiierResult
from src.Model.Model import Model
from ProjectDir import ProjectDir

class DiscriminationModel(Model):
    words = {}
    pos_size =0;
    neg_size =0;

    def buildModel(self,filepaths):
        self.loadFiles(filepaths)
        posWord ={}
        negWord ={}
        for line in self.posCorpos:
            for tmpword in self.wordTools.seperatewords(line):
                if(tmpword in posWord.keys()):
                    posWord[tmpword] +=1
                else:
                    posWord[tmpword] =1
        for line in self.negCorpos:
            for tmpword in self.wordTools.seperatewords(line):
                if(tmpword in negWord.keys()):
                    negWord[tmpword] +=1
                else:
                    negWord[tmpword] =1
        for word in posWord.keys():
            if word in negWord.keys():
                self.words[word] = [posWord[word],negWord[word]]
            else :
                self.words[word] = [posWord[word],0]
        for word in negWord.keys():
            if word not in posWord.keys():
                self.words[word] =[0,negWord[word]]

    def saveModelDefault(self):
        filepath =ProjectDir.resourceDir+"DiscriminationModel\model.txt";
        self.saveModel(filepath)

    def saveModel(self,filepath):
        content ="pos_neg,"+str(self.posCorpos.__len__())+","+str(self.negCorpos.__len__())+"\n"
        for word in self.words:
            content += word+","+str(self.words[word][0])+","+str(self.words[word][1])+"\n"
        self.wordTools.saveIntoFile(filepath,content,"utf-8")

    def loadModelDefault(self):
        filepath =ProjectDir.resourceDir+"DiscriminationModel\model.txt";
        self.loadModel(filepath)

    def loadModel(self,filepath):
        content = self.wordTools.readFile(filepath)
        head = content[0];
        headContent = head.split(",");
        if headContent.__len__() != 3 :
            print("model is damaged")
            return ;
        self.pos_size = float(headContent[1])
        self.neg_size = float(headContent[2])
        for string in content[1: content.__len__()]:
            tmp =string.split(",")
            if(tmp.__len__() != 3):
                continue
            self.words[tmp[0]]= [float(tmp[1]),float(tmp[2])]

    def predict(self,line):
        result =ClassfiierResult()
        result.string =line
        pos_value =0
        neg_value =0
        details ="";
        words = self.wordTools.seperatewords(line)
        for word in words:
            if(word in self.words):
                if  float(self.words[word][0]) > float(self.words[word][1]):
                    pos_value+=1;
                else:
                    neg_value+=1;
                details +=word+":"+str(self.words[word][0]) +","+ str(self.words[word][1])+";"
            else:
                continue;
        details += str(pos_value)+":"+str(neg_value)
        result.detailInfo = details
        if pos_value> neg_value:
            result.predict =True;
        else:
            result.predict =False;
        return result

    def test(self,trainFiles,testFile):
        self.eval.className = "discrimination"
        self.eval.trainData = trainFiles
        self.eval.testData = testFile
        filepath =ProjectDir.resourceDir+"DiscriminationModel\model.txt";
        self.buildModel(trainFiles)
        # self.saveModel(filepath)
        # self.loadModel(filepath)
        self.loadTestData(testFile)
        return  self.evaluateModel()
