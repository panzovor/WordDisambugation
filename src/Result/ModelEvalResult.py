__author__ = 'E440'
import os
class ModelEvalResult:

    def __init__(self):
        self.className=""
        self.trainData=[]
        self.testData =[]
        self.precision=0.0
        self.recall = 0.0
        self.f_score =0.0
    def GetFileNameAndExt(self,filename):
        (filepath,tempfilename) = os.path.split(filename);
        (shotname,extension) = os.path.splitext(tempfilename);
        return shotname,extension

    def toString(self):
        content =""

        for string in self.trainData:
            content+= self.GetFileNameAndExt(string)[0]+" "
        content+=","
        for string in self.testData:
            content+= self.GetFileNameAndExt(string)[0]+" "
        content+=","
        content+= self.className+","
        content+= str(self.precision)+","
        content+= str(self.recall)+","
        content+= str(self.f_score)
        return content

    def test(self):
        self.className = "dd"
        self.trainData=["aaa","bbbb","cccc"]
        self.testData =["ddddd"]
        self.precision=1.0
        self.recall = 1.0
        self.f_score =1.0
        print(self.toString())