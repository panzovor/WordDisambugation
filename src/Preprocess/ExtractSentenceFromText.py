from ProjectDir import ProjectDir
from src.Tools.SeperateWords import wordSegment
import re

class ExtractSentenceFromText:

    def __init__(self):
        self.wordTools = wordSegment()
        self.point_cars = self.wordTools.carwords
        self.regex =""
        for word in self.wordTools.carwords:
            self.regex +=word+"|"
        self.regex = self.regex[0:self.regex.__len__()-1]

    def loadTextData(self,filepath):
        wordTools = wordSegment()
        content = wordTools.readFile(filepath)
        data ={"pos":[],"neg":[]}
        for line in content:
            linelist = line.split("\t",1)
            # contentLine =""
            # for i in range(1,linelist.__len__()):
            #     contentLine+=linelist[i]
            data[linelist[0].lower()].append(linelist[1])
        return data

    def findCarWordsFromSentence(self,result,sentence):
        # if sentence.__len__()>1000:
        #     return
        match = re.search(self.regex,sentence)
        if match:
            car = match.group(0)
            result.add(car)
            # print(sentence+","+car)
            sen = sentence[sentence.find(car)+car.__len__():]
            # print(sen)
            self.findCarWordsFromSentence(result,sen)
        return result

    def extractSentenceFromTextWithCars(self,cars,data):
        result={}
        for type in data.keys():
            count=0
            for line in data[type]:
                count+=1
                print(str(count)+"/"+str(data[type].__len__()))
                sentences = re.split("。|\.|\!|？|\?",line)
                for sentence in sentences:
                    for car in cars:
                        if car in sentence:
                            if car not in result.keys():
                                result[car] = set()
                            result[car].add(sentence+"\t"+type)
        return result

    def containsChinese(self,sentence):
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zhPattern.search(sentence)
        if match :
            return True
        else:
            return False

    def extractSentenceFromText(self,text):
        result =[]
        sentences = re.split("。|\.|\!|？|\?",text)
        for sentence in sentences:
            cars =set()
            self.findCarWordsFromSentence(cars,sentence)
            cars = set(self.point_cars).intersection(cars)
            if cars.__len__() >0:
                if self.containsChinese(sentence) or True:
                    result.append(sentence)
        return result


    def extractCarSentenceFromText(self,data):
        result={}
        for type in data.keys():
            count=0
            for line in data[type]:
                count+=1
                print(str(count)+"/"+str(data[type].__len__()))
                sentences = re.split("。|\.|\!|？|\?",line)
                for sentence in sentences:
                    cars =set()
                    self.findCarWordsFromSentence(cars,sentence)
                    if cars.__len__() >0:
                        for car in cars:
                            if car not in result.keys():
                                result[car] = set()
                            result[car].add(sentence+"\t"+type)
        return result

    def preprocessFilterCorpus(self):
        wordTools=  wordSegment()
        # filepath = ProjectDir.resourceDir+"Corpus/20160906/汽车信息过滤测试语料.csv"
        # savepath = ProjectDir.resourceDir+"Corpus/20160906/汽车信息过滤句子语料-carwords.txt"
        filepath = ProjectDir.resourceDir+"Corpus/20161011/testData/20160902-5000.txt"
        savepath = ProjectDir.resourceDir+"Corpus/20161011/testData/20160902-5000-sentences.txt"
        data = self.loadTextData(filepath)
        result = self.extractCarSentenceFromText(data)
        print(result.__len__())
        wordTools.saveDictIntoFileWithLines(savepath,result)

    def extract_pointed_cars_data(self,cars,filepath,savepath):
        wordTools = wordSegment()
        data = self.loadTextData(filepath)
        result = self.extractSentenceFromTextWithCars(cars,data)
        print(result.__len__())
        wordTools.saveDictIntoFileWithLines(savepath,result)

ex = ExtractSentenceFromText()
# result = ex.containsChinese("com/2366414607/E6L9b0CaR")
# print(result)
cars = ["世嘉"]
filepath = ProjectDir.resourceDir+"Corpus/20161024/testData/世嘉-ori.txt"
savepath = ProjectDir.resourceDir+"Corpus/20161024/testData/世嘉-sentence.txt"

# ex.extract_pointed_cars_data(cars,filepath,savepath)
# ex.preprocessFilterCorpus()









