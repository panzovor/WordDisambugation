__author__ = 'E440'
from src.Preprocess.ExtractSentenceFromText import  ExtractSentenceFromText
from src.Tools.SeperateWords import wordSegment
from ProjectDir import ProjectDir


class TransferIntoSameFormat():

    def __init__(self):
        self.extractor = ExtractSentenceFromText()
        self.wordTools = wordSegment()

    def transfer(self,files):
        for file in files:
            result =[]
            data = self.wordTools.readFile(file)
            for line in data:
                cars =set()
                self.extractor.findCarWordsFromSentence(cars,line)
                for car in cars:
                    words = self.wordTools.seperatewords(line)
                    if words.__len__()<3:
                        continue
                    content = line
                    result.append(content)
            savepath =self.wordTools.seperateFilepath(file)
            self.wordTools.saveIntoFile_list(savepath[0]+"\\alldata\\"+savepath[1]+savepath[2],result)

    def combineall(self):

        files =[
            ProjectDir.resourceDir+"Corpus\\alldata\数据1.txt"
            ,ProjectDir.resourceDir+"Corpus\\alldata\数据2-remove#.txt"
            ,ProjectDir.resourceDir+"Corpus\\alldata\数据3—duplicate.txt"
            ,ProjectDir.resourceDir+"Corpus\\alldata\数据5—duplicate.txt"
            ,ProjectDir.resourceDir+"Corpus\\alldata\汽车信息过滤句子语料-carwords.txt"
        ]
        filepath = ProjectDir.resourceDir+"Corpus\\alldata\\alldata.txt"
        data=[]
        for file in files:
            data.extend(self.wordTools.readFile(file))
        data =set(data)
        data = list(data)
        self.wordTools.saveIntoFile_list(filepath,data)

dataFile =[
    ProjectDir.resourceDir+"Corpus\数据1.txt"
    ,ProjectDir.resourceDir+"Corpus\数据2-remove#.txt"
    ,ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt"
    ,ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"
    ,ProjectDir.resourceDir+"Corpus\汽车信息过滤句子语料-carwords.txt"
]
transfer = TransferIntoSameFormat()
transfer.transfer(dataFile)

transfer.combineall()
