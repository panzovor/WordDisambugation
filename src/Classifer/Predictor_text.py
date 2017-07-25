
__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText
from ProjectDir import ProjectDir
from src.Model.DiscriminationModel import  DiscriminationModel
from src.Model.TfIdfModels import TfidfModels
from src.Model.TfPerCarModel import TFPerCarModel
from src.Model.MultiModels import MultiModels
from src.Model.MultiModel_tfidf_vector import MultiModel_tfidf_vector
from src.Model.VectorSpace import VectorSpace
import time

class Predictor_text():

    def __init__(self):
        self.tools = wordSegment()
        self.extractor = ExtractSentenceFromText()
        self.testdata =[]
        self.result =""

    def initModel(self,model ):
        self.model = model

    ##  trainFile  is a list
    def loadModel(self,trainfile):
        self.result ="训练数据："+str(trainfile)+"  \n"
        # self.result +="测试数据："+testfile+"  \n"
        # self.load_test(testfile)
        self.model.buildModel(trainfile)

    def load_test(self,testfile):
        data = self.tools.readFile(testfile)
        self.result+="测试数据大小："+str(data.__len__())+"  \n"
        print(data.__len__())
        for line in data:
            lines = line.split("\t",1)
            # self.testdata[lines[1]] = lines[0].lower()
            self.testdata.append([lines[1],lines[0]])
            # self.testdata[1] = lines[0].lower()
        self.result+="测试数据去重："+str(self.testdata.__len__())+"  \n"
        print(self.testdata.__len__())

    def evaluate(self,details_file,text_file):
        #np:误判，pn:漏判
        pp,np,pn,nn = 0,0,0,0
        details = ""
        i= 0
        text_id = ""
        # self.extractor.point_cars = set(["世嘉"])
        for text in self.testdata:
            i+=1
            lines = self.extractor.extractSentenceFromText(text[0])
            predict_result =False
            tmp_details = ""
            text_id += str(i)+"\t"+text[0]+"\t"+text[1]+"\t"+"\n"
            for line in lines:
                tmp = self.model.predict(line)
                tmp_details += tmp.toString()
                if tmp.predict == True:
                    predict_result = True
                    break
            # details +=str(i)+"\t"+tmp_details+"\n"
            if text[1] =="pos":
                if predict_result == True:
                    pp+=1
                else:
                    details+=str(i)+"\t"+tmp_details+"\n"
                    pn+=1
            else:
                if predict_result == True:
                    np+=1
                    details +=str(i)+"\t"+tmp_details+"\n"
                else:
                    nn+=1

        precision_p = pp/(pp+np)
        recall_p = pp/(pp+pn)
        f_score_p = 2/(1/precision_p+1/recall_p)

        precision_n = nn/(nn+pn)
        recall_n = nn/(nn+np)
        f_score_n = 2/(1/precision_n+1/recall_n)
        self.result=""
        self.result+="混淆矩阵\n\n|  | P(label) | N(label) |\n| -------- | -------- | -------- |\n| P(predict)  | "+str(pp)+"  | "+str(np)+" |\n| N(predict)  | "+str(pn)+"  | "+str(nn)+" | \n效果\n\n| 类别 | 准确率 | 召回率 | f值 |\n| -------- | -------- | -------- | -------- |\n| P(predict)  | "+str(precision_p)+"  | "+str(recall_p)+" | "+str(f_score_p)+" |\n| N(predict)  | "+str(precision_n)+"  | "+str(recall_n)+" | "+str(f_score_n)+" | "
        # print(result)
        # print(details)
        self.tools.saveIntoFile(details_file,details)
        self.tools.saveIntoFile(text_file,text_id)
        return self.result

# print(ProjectDir.resourceDir)

trainfile =ProjectDir.resourceDir+"Corpus\\20161108\\train.txt"
details_file1 = ProjectDir.resourceDir+\
            "Corpus\\20161108\\testResult\\details1.txt"
details_file2 = ProjectDir.resourceDir+\
            "Corpus\\20161108\\testResult\\details2.txt"
details_file3 = ProjectDir.resourceDir+\
            "Corpus\\20161108\\testResult\\details3.txt"
textfile1 = ProjectDir.resourceDir+\
            "Corpus\\20161108\\testResult\\text1.txt"
textfile2 = ProjectDir.resourceDir+\
            "Corpus\\20161108\\testResult\\text2.txt"
textfile3 = ProjectDir.resourceDir+\
            "Corpus\\20161108\\testResult\\text3.txt"

testfile1 = ProjectDir.resourceDir+"Corpus\\20161108\\test10月-庆丽.txt"
savefile1 = ProjectDir.resourceDir+"Corpus\\20161108\\test10月-庆丽-testresult.txt"
testfile2 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-万礼.txt"
savefile2 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-万礼-testresult.txt"
testfile3 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-庆丽.txt"
savefile3 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-庆丽-testresult.txt"


models = []
# models.append(TfidfModels())
models.append(TFPerCarModel())
# models.append(VectorSpace())
# models.append(MultiModel_tfidf_vector())
models.append(DiscriminationModel())

def test(trainfile,testfiles,details_files,textfiles,savefiles):
    print("ddd")
    for model in models:

        predictor = Predictor_text()
        predictor.initModel(model)
        trainfiles  = [
            trainfile
            ]
        predictor.loadModel(trainfiles)
        print(type(model)," trained")
        for i in range(3):
            predictor.load_test(testfiles[i])
            result = predictor.evaluate(details_files[i],textfiles[i])
            tmp  = str(trainfiles)
            tmp +="\n"+str(testfiles[i])+"\n"
            tmp += result
            print(result)

            predictor.tools.saveIntoFile(savefiles[i],tmp)

testfiles = [testfile1,testfile2,testfile3]
detailsfiles = [details_file1,details_file2,details_file3]
savefiles = [savefile1,savefile2,savefile3]
textfiles =[textfile1,textfile2,textfile3]
test(trainfile,testfiles,detailsfiles,textfiles,savefiles)