__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText
import re
from ProjectDir import ProjectDir

class ResultObservator:

    def __init__(self):
        self.wordTools = wordSegment()
        self.extractor = ExtractSentenceFromText()


    def analyse(self,files):
        result = {}
        regex ="漏判\n|误判\n|pp\n|nn\n"
        for file in files:
            data = self.wordTools.readContent(file)
            tmp = re.split(regex,data)
            if tmp.__len__() == 5:
                #漏判
                lines = tmp[1].split("\n")
                for line in lines:
                    if line.strip() == "":
                        continue
                    line = line.replace("predict.*","")
                    cars=set()
                    self.extractor.findCarWordsFromSentence(cars,line)
                    if cars.__len__() == 0:
                        continue
                    for car in cars:
                        if car not in result.keys():
                            result[car] =[0,0,0,0,0]
                        result[car][0]+=1
                        result[car][4]+=1
                #误判
                lines = tmp[2].split("\n")
                for line in lines:
                    if line.strip() == "":
                        continue
                    line = line.replace("predict.*","")
                    cars=set()
                    self.extractor.findCarWordsFromSentence(cars,line)
                    for car in cars:
                        if car not in result.keys():
                            result[car] =[0,0,0,0,0]
                        result[car][1]+=1
                        result[car][4]+=1
                #pp
                lines = tmp[3].split("\n")
                # print("pp line's length: "+str(lines.__len__()))
                for line in lines:
                    if line.strip() == "":
                        continue
                    line = line.replace("predict.*","")
                    cars=set()
                    self.extractor.findCarWordsFromSentence(cars,line)
                    for car in cars:
                        if car not in result.keys():
                            result[car] =[0,0,0,0,0]
                        result[car][2]+=1
                        result[car][4]+=1
                #nn
                lines = tmp[4].split("\n")
                # print("nn line's length: "+str(lines.__len__()))
                for line in lines:
                    if line.strip() == "":
                        continue
                    line = line.replace("predict.*","")
                    cars=set()
                    self.extractor.findCarWordsFromSentence(cars,line)
                    for car in cars:
                        if car not in result.keys():
                            result[car] =[0,0,0,0,0]
                        result[car][3]+=1
                        result[car][4]+=1
            else:
                print("format error"+str(tmp.__len__()))
        return result


    def analyseDemo(self,prefix,modelname):
        files =[
            prefix+modelname+"_file0.txt"
            ,prefix+modelname+"_file1.txt"
            ,prefix+modelname+"_file2.txt"
            ,prefix+modelname+"_file3.txt"
            ,prefix+modelname+"_file4.txt"
        ]
        result = self.analyse(files)
        content =""
        for car in result.keys():
            content+= modelname +","+car+","
            content+= str(result[car][0])+","
            content+= str(result[car][1])+","
            content+= str(result[car][2])+","
            content+= str(result[car][3])+","
            content+= str(result[car][4])+","
            content+= str((result[car][2]+result[car][3])/result[car][4])+","
            content+= str((result[car][0]+result[car][1])/result[car][4])+"\n"
            # content+= str((result[car][2])/(result[car][0]+result[car][2]))+","
            # content+= str((result[car][2])/(result[car][1]+result[car][2]))+"\n"
        return content


    def analyseall(self):
        modelnames = [
            "tfidf"
            ,"disc"
            ,"tfPerCar"
            ,"mult_tfidf_vect"
            ,"vector"
        ]
        result =""
        prefix = ProjectDir.resourceDir+"Corpus/data1235/observationOfResult/crossvalidationResult/new_"
        for name in modelnames:
            result+=self.analyseDemo(prefix,name)
        savepath = prefix+"observation.csv"
        wordSegment.saveIntoFile(wordSegment,filepath=savepath,content= result)
        return result

    # def testAnalyse(self):
    #     file = [
    #         ProjectDir.resourceDir+"ModelEvaluationResult//new_tfidf_file0.txt"
    #        ]
    #     result = self.analyse(file)
    #     print(result)


robservator = ResultObservator()
res = robservator.analyseall()
print(res)