__author__ = 'E440'

import math
from src.Preprocess.Duplicate import Dupicate
from src.Tools.SeperateWords import wordSegment as wordSegment
from ProjectDir import ProjectDir
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText
import re

class FeatureExtractor():

    def __init__(self):
        self.corpos={}
        self.dupicate = Dupicate()
        self.wordTools = wordSegment()
        # self.pos_tf = {}
        self.idf={}
        self.debug = False
        self.tf ={}
        # self.neg_tf = {}
        self.possible={}
        self.carExtractor= ExtractSentenceFromText()
        self.label_info = {"pos":"^1\t","neg":"^-1\t","neu":"^0\t"}
        self.labels = ["pos","neu","neg"]
        # print(self.wordTools.absolute_words)

    def loadFiles(self,filepaths):
        for key in self.label_info.keys():
            self.corpos[key] =[]
        for key in self.label_info.keys():
            self.tf[key] ={}
        for filepath in filepaths:
            for line in self.wordTools.readFile(filepath):
                for key in self.label_info.keys():
                    pattern = re.compile(self.label_info[key])
                    if pattern.match(line):
                        line = re.sub(self.label_info[key],"",line)
                        self.corpos[key].append(line)

    def tf_idf(self):
        all =0
        for label in self.label_info.keys():
            for line in self.corpos[label]:
                all+=1
                words = self.wordTools.seperatewords(line = line.strip())
                for word in words:
                    if(word.strip() == ""):
                        continue
                    if word in self.tf[label].keys():
                        self.tf[label][word]+=1
                    else:
                        self.tf[label][word] =1
                    if word in self.idf.keys():
                        self.idf[word] = self.idf[word]+1
                    else:
                        self.idf[word] =1
        for word in self.idf.keys():
            count_word = self.idf[word]
            self.idf[word] = abs(math.log10(count_word/all))

        for label in self.tf.keys():
            for word in self.idf.keys():
                if word in self.tf[label].keys():
                    self.tf[label][word] = abs(self.tf[label][word]* self.idf[word])

    def buildModel(self,filepaths):
        self.loadFiles(filepaths)
        self.tf_idf()

    def extract_num(self,words):
        result =[]
        for i in range(self.labels.__len__()):
            result.append(0)
        for word in words:
            for i in range(self.labels.__len__()):
                if word in self.tf[self.labels[i]].keys():
                    result[i]+=1
        return result

    def extract_tfidf(self,words):
        result =[]
        for i in range(self.labels.__len__()):
            result.append(0)
        for word in words:
            for i in range(self.labels.__len__()):
                if word in self.tf[self.labels[i]].keys():
                    result[i]+=self.tf[self.labels[i]][word]

        return result

    def extract_most_relevant_words(self,words,lenth):
        result =[]
        for i in range(self.labels.__len__()):
            result.append([])
        for word in words:
            for i in range(self.labels.__len__()):
                if word in self.tf[self.labels[i]].keys():
                    result[i].append(self.tf[self.labels[i]][word])
        for i in range(self.labels.__len__()):
            # print(result[i])
            # tmp = result[i]
            # input()
            result[i].sort(reverse = True)
            if result[i].__len__()>=lenth:
                result[i] = result[i][0:lenth]
            else:
                for j in range(lenth-result[i].__len__()):
                    result[i].append(0)
        final_result = []
        for tmp in result:
            final_result.extend(tmp)
        return final_result

    def extract_all_feature(self,line,lenth):
        result = []
        words = self.wordTools.seperatewords(line)
        if self.debug:
            print("num",self.extract_num(words))
            print("tfidf",self.extract_tfidf(words))
            print("relev",self.extract_most_relevant_words(words,lenth))
            input()
        result.extend(self.extract_num(words))
        result.extend(self.extract_tfidf(words))
        result.extend(self.extract_most_relevant_words(words,lenth))
        for key in self.label_info.keys():
            pattern = re.compile(self.label_info[key])
            if pattern.match(line):
                result.append(key)
        # print(line,result)
        return result

    def make_arff_file(self,file,savepath):
        content= self.wordTools.readFile(file)
        count =0
        lenth =6
        fea = feature.extract_all_feature("上传动力方面更是不错，起步反应灵敏，涡轮介入比较积极，车速随着涡轮的介入，迅速的得以提升，发动机声音也比较清纯没有嘈杂音",lenth)
        string ="@relation arff_data2\n"
        for i in range(fea.__len__()):
            string+="@attribute attr"+str(i)+" numeric\n"
        string+="@attribute class {"
        for i in range(self.labels.__len__()-1):
            string+=self.labels[i]+","
        string+= self.labels[-1]+"}\n"
        string+="\n@data\n"
        # string="@relation arff_data2\n@attribute pos_num numeric\n@attribute pos_tfidf numeric\n@attribute neg_num numeric\n@attribute neg_tfidf numeric\n@attribute possible numeric\n@attribute class {0,1}\n@data\n"
        for line in content:
            count+=1
            print(count,"/",content.__len__())
            result = self.extract_all_feature(line,lenth)
            string+= str(result)[1:-1]+"\n"
        # print(string)
        self.wordTools.saveIntoFile(savepath,string)



trainfile =ProjectDir.resourceDir+"Corpus\\Sentement\\traincut1.3.0.txt"
feature = FeatureExtractor()
feature.buildModel([trainfile])
feature.debug = False
# print(feature.extract_all_feature("上传动力方面更是不错，起步反应灵敏，涡轮介入比较积极，车速随着涡轮的介入，迅速的得以提升，发动机声音也比较清纯没有嘈杂音 pos"))
savepath = ProjectDir.resourceDir+"Corpus\\Sentement\\trainfile.arff"
feature.make_arff_file(trainfile,savepath)
print(savepath)

testfile = ProjectDir.resourceDir+"Corpus\\Sentement\\testcut1.2.0.txt"
savepath = ProjectDir.resourceDir+"Corpus\\Sentement\\testcut1.2.0.arff"
feature.make_arff_file(testfile,savepath)
print(savepath)