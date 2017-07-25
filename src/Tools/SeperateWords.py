__author__ = 'E440'
import jieba
import jieba.posseg as posseg
from src.Tools.FileChecker import FileChecker
import codecs
from src.Tools.langcov import *
from ProjectDir import ProjectDir

class wordSegment(object):
    # projectDir = ProjectDir()

    def __init__(self):
        file = ProjectDir.resourceDir+"dict/absolute_words"
        file_black = ProjectDir.resourceDir+"dict/blackList.txt"
        file_white = ProjectDir.resourceDir+"dict/whiteList.txt"
        self.absolute_words = set(codecs.open(file,"r","utf-8").read().split("\r\n"))
        self.black_list_words = set(codecs.open(file_black,"r","utf-8").read().split("\r\n"))
        self.white_list_words = set(codecs.open(file_white,"r","utf-8").read().split("\r\n"))
        tmp_words  =set()
        file1 = ProjectDir.resourceDir+"dict/汽车专业词典-PURE.txt"
        tmp_words = set(codecs.open(file1,"r","utf-8").read().split("\r\n"))
        # self.absolute_words = self.absolute_words|tmp_words

        # print(self.absolute_words)
        jieba.load_userdict(ProjectDir.resourceDir+"dict/userdict")
        jieba.load_userdict(ProjectDir.resourceDir+"dict/car_brand.txt")
        jieba.load_userdict(ProjectDir.resourceDir+"dict/car_type.txt")
        jieba.load_userdict(ProjectDir.resourceDir+"dict/汽车专业词典-PURE.txt")
        self.carwords = [line.strip() for line in codecs.open(ProjectDir.resourceDir+"dict/car_brand.txt",encoding="utf-8").readlines()]
        self.carwords += [line.strip() for line in codecs.open(ProjectDir.resourceDir+"dict/car_type.txt",encoding="utf-8").readlines()]
        for i in range(self.carwords.__len__()-1):
            for j in range(i+1,self.carwords.__len__()):
                if self.carwords[i].__len__() < self.carwords[j].__len__():
                    tmp = self.carwords[i]
                    self.carwords[i] = self.carwords[j]
                    self.carwords[j] = tmp
        self.stopwords = [line.strip() for line in codecs.open(ProjectDir.resourceDir+"dict\stop.txt",encoding="utf-8").readlines()]
        self.absolute_words = self.absolute_words-set(self.carwords)
        return

    def conv(self,line):
        # line = Converter('zh-hans').convert(line)
        return line

    def readContent (self,filepath):
        return codecs.open(filepath,encoding="utf-8").read()

    def readFile(self, filepath):
        return [self.conv(line.strip()) for line in codecs.open(filepath,encoding="utf-8").readlines()]

    def readFileWityDict(self,filepath,seperator=","):
        dicts = {}
        for line in codecs.open(filepath,encoding="utf-8").readlines():
            tmp = line.split(seperator)
            dicts[tmp[0]] = tmp[1].strip()
        return dicts

    def readFileWityDict_(self,filepath,seperator=","):
        dicts = {}
        for line in codecs.open(filepath,encoding="utf-8").readlines():
            line = line.replace("\n","")
            tmp = line.split(seperator)
            dicts[tmp[0]] = [int(i) for i in tmp[1:] ]
        return dicts

    def seperatewords(self, line, userjieba = True ):
        result =[]
        if userjieba:
            words = jieba.cut(line)
        else :
            words = list(line)
        for val in words :
            # print(val.word+"  "+val.flag)
            if val not in self.stopwords :
                if val.isalpha():
                    if val not in self.carwords:
                        val = val.lower();
                result.append(val)
        # result =[val for val in words if val not in self.stopwords]
        # result = set(words) - set(self.stopwords)
        return result

    def saveIntoFile_list(self,filepath,content, encoding ="utf-8", append =False):
        file =None;
        checker = FileChecker();
        checker.checkFile(filepath)
        if(append ==True):
            file = codecs.open(filepath,"a",encoding=encoding)
        else:
            file = codecs.open(filepath,"w",encoding=encoding)
        for line in content:
            file.write(line+"\n")
        file.flush()
        file.close()

    def saveIntoFile(self,filepath,content, encoding ="utf-8", append =False):
        file =None;
        checker = FileChecker();
        checker.checkFile(filepath)
        if(append ==True):
            file = codecs.open(filepath,"a",encoding=encoding)
        else:
            file = codecs.open(filepath,"w",encoding=encoding)
        file.write(content+"\n")
        file.flush();
        file.close();

    def saveDictIntoFileWithLines(self,filepath,dict,encoding="utf-8",append=False):
        file =None
        if(append ==True):
            file = codecs.open(filepath,"a",encoding=encoding)
        else:
            file = codecs.open(filepath,"w",encoding=encoding)
        for key in dict.keys():
            for line in dict[key]:
                file.write(line+"\n")
        file.close()
    def saveDictIntoFile(self,filepath,dict,encoding="utf-8",append=False):
        file =None
        if(append ==True):
            file = codecs.open(filepath,"a",encoding=encoding)
        else:
            file = codecs.open(filepath,"w",encoding=encoding)
        for key in dict.keys():
            file.write(key+","+str(dict[key])+"\n")
        # print(filepath)
        file.close()

    def seperateFilepath(self,file):
        import os
        (filepath,tempfilename) = os.path.split(file);
        (shotname,extension) = os.path.splitext(tempfilename);
        return filepath,shotname,extension

# wordS = wordSegment()
# word = wordS.seperatewords(line = "经着手准备青少年高尔夫发展基金，公益培")
# print(word)
# for w in word:
#     print(w)
#
# words = wordSegment()
# line = words.conv("日本豐田上週針對第三代、也就是上一代rav4在全球發出召回令，馬來西亞豐田也宣布召回rav4休旅車")
# print(line)
# words.readFileWityDict(ProjectDir.resourceDir+"TfidfModel\pos.txt")