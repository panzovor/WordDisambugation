__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment as wordSegment
import re

class GenerateTextData:

    posCorpos =[]
    negCorpos =[]
    wordTools = wordSegment()

    def loadFiles(self,filepaths):
        for filepath in filepaths:
            if filepath.find("pos")>0:
                self.posCorpos.extend(self.wordTools.readFile(filepath))
            elif filepath.find("neg")>0:
                self.negCorpos.extend(self.wordTools.readFile(filepath))
            else:
                # print("other")
                for line in self.wordTools.readFile(filepath):
                    if(line.find("pos")>0):
                        self.posCorpos.append(line)
                    else :
                        self.negCorpos.append(line)

    def judget(self,filepath):
        data = self.wordTools.readFile(filepath)
        self.judgeData(data)

    def judgeData(self,data):
        posCount =0
        detail ={}
        flag =False
        for line in data:
            # posCount +=1
            for car in self.wordTools.carwords:
                if line.__contains__(car):
                    # posCount+=1
                    # flag =True
                    # print(line)
                    if car not in detail:detail[car] =1
                    else: detail[car]+=1
                    # break
            # if not flag:
            #     print(line)
            flag = False
        print(detail.__len__())
        print(detail)
        print(posCount)


files = ["E:\汽车消歧\数据\文章\数据1.txt","E:\汽车消歧\数据\文章\数据2.txt"]
filepath ="E:\汽车消歧\数据\文章/noauto.txt"
generator = GenerateTextData()
generator.loadFiles(files)
# generator.judge(filepath)
generator.judgeData(generator.posCorpos)