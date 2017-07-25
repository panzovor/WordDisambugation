__author__ = 'E440'
from src.Model.Model import Model
from src.Model.TfIdfModels import  TfidfModels
from src.Model.VectorSpace import  VectorSpace
from src.Result.ClassifierResult import ClassfiierResult
from ProjectDir import ProjectDir

class MultiModel_tfidf_vector(Model):

    def __init__(self):
        self.tfidf= TfidfModels()
        self.vetspace = VectorSpace()

    def buildModel(self,trainFile):
        self.tfidf.buildModel(trainFile)
        self.vetspace.buildModel(trainFile)

    def predict(self,line):
        # result = ClassfiierResult()
        # result.string = line
        # tfidfresult = self.tfidf.predict(line)
        # vect = self.vetspace.predict(line)
        # result.predict =False
        # if vect.predict == True:
        #     result.predict = True
        # elif tfidfresult.predict  == True:
        #     result.predict = True
        # return result
        result = ClassfiierResult()
        result.string = line
        result.predict =False
        if self.vetspace.predict(line).predict == True:
            result.detailInfo+= "  vect:true"
            result.predict = True
        elif line.__len__()>10:
            if self.tfidf.predict(line).predict == True:
                result.predict =True
                result.detailInfo+= "  vect:False,tfidf:true"
            else:
                result.detailInfo+= "  both denied"
        return result

    def test(self,trainFile,testFile):
        self.eval.className = "multi with tfidf and vector"
        self.eval.trainData = trainFile
        self.eval.testData = testFile
        self.buildModel(trainFile)
        self.loadTestData(testFile)
        return self.evaluateModel()


    def demo(self):
        trainFile =[
            ProjectDir.resourceDir+"Corpus\seperate_allData_train.txt"
        ]
        self.buildModel(trainFile)
        line ="宝马对3系的悬架系统作了不少改进 pos"
        print(self.predict(line).toString())

# mul = MultiModel_tfidf_vector()
# mul.demo()