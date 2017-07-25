__author__ = 'E440'

import math
from src.Preprocess.Duplicate import Dupicate
from src.Tools.SeperateWords import wordSegment as wordSegment
from ProjectDir import ProjectDir
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText

class FeatureExtractor():

    def __init__(self):
        self.posCorpos=[]
        self.negCorpos=[]
        self.dupicate = Dupicate()
        self.wordTools = wordSegment()
        self.pos_tf = {}
        self.idf={}
        self.neg_tf = {}
        self.possible={}
        self.carExtractor= ExtractSentenceFromText()
        print(self.wordTools.absolute_words)

    def loadFiles(self,filepaths):
        for filepath in filepaths:
            if filepath.find("pos")>=0:
                self.posCorpos.extend(self.wordTools.readFile(filepath))
            elif filepath.find("neg")>=0:
                self.negCorpos.extend(self.wordTools.readFile(filepath))
            else:
                for line in self.wordTools.readFile(filepath):
                    if(line.find("pos")>=0):
                        self.posCorpos.append(line)
                    else :
                        self.negCorpos.append(line)
        self.posCorpos = self.dupicate.dupicate(self.posCorpos)
        self.negCorpos = self.dupicate.dupicate(self.negCorpos)

    def tf_idf(self):
        all =0;
        for line in self.posCorpos:
            all = all+1;
            # print(line)
            words = self.wordTools.seperatewords(line = line.strip())
            for word in words:
                # print(word)
                if(word.strip() == ""):
                    continue
                if word in self.pos_tf:
                    self.pos_tf[word] = self.pos_tf[word]+1
                else: self.pos_tf[word]=1
                if word in self.idf.keys():
                    self.idf[word] = self.idf[word]+1
                else:
                    self.idf[word] =1

        for line in self.negCorpos:
            all = all+1;
            words = self.wordTools.seperatewords(line = line.strip())
            for word in words:
                if(word.strip() == ""):
                    continue
                if word in self.neg_tf.keys() : self.neg_tf[word] = self.neg_tf[word]+1
                else: self.neg_tf[word] =1
                if word in self.idf.keys(): self.idf[word] = self.idf[word]+1
                else: self.idf[word] =1
        for word in self.idf.keys():
            count_word = self.idf[word]
            self.idf[word] = abs(math.log10(count_word/all))
        for word in self.pos_tf.keys():
            self.pos_tf[word] = abs(self.pos_tf[word]* self.idf[word])
        for word in self.neg_tf.keys():
            self.neg_tf[word] = abs(self.neg_tf[word]* self.idf[word])

    def car_possbile(self):
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
                self.possible[word] = [posWord[word],negWord[word]]
            else :
                self.possible[word] = [posWord[word],0]
        for word in negWord.keys():
            if word not in posWord.keys():
                self.possible[word] =[0,negWord[word]]

    def buildModel(self,filepaths):
        self.loadFiles(filepaths)
        self.tf_idf()
        self.car_possbile()

    def extract_pos_num(self,words):
        result = 0
        for word in words:
            if word in self.pos_tf.keys():
                result+=1
        return result

    def extract_pos_tfidf(self,words):
        result = 0
        for word in words:
            if word in self.pos_tf.keys():
                result+=self.pos_tf[word]
        return result

    def extract_neg_num(self,words):
        result = 0
        for word in words:
            if word in self.neg_tf.keys():
                result+=1
        return result

    def extract_neg_tfidf(self,words):
        result = 0
        for word in words:
            if word in self.neg_tf.keys():
                result+=self.neg_tf[word]
        return result

    def extract_possible(self,line):
        cars = set()
        self.carExtractor.findCarWordsFromSentence(cars,line)
        if cars.__len__() ==0:
            return 0.5
        else:
            result = 0
            for car in cars:
                if car in self.possible:
                    possibility = self.possible[car][0]+ self.possible[car][1]
                    result+=self.possible[car][0]/possibility
                else:
                    result+=0.5
            result /= cars.__len__()
            return result

    def extract_contains_keywords(self,words):
        result = [0,0,0]
        for word in words:
            if word in self.wordTools.absolute_words:
                result[0]+=1
            if word in self.wordTools.black_list_words:
                result[1]+=1
            if word in self.wordTools.white_list_words:
                result[2]+=1
        return result

    def extract_most_relevant_words(self,words):
        word_pos_dict =[]
        word_neg_dict =[]
        for word in words:
            if word in self.pos_tf:
                word_pos_dict.append(self.pos_tf[word])
            if word in self.neg_tf:
                word_neg_dict.append(self.neg_tf[word])
        word_pos_dict.sort(reverse= True)
        word_neg_dict.sort(reverse = True)
        if word_pos_dict.__len__()>=3:
            word_pos_dict = word_pos_dict[0:3]
        else:
            for i in range(3-word_pos_dict.__len__()):
                word_pos_dict.append(0)
        if word_neg_dict.__len__()>=3:
            word_neg_dict = word_neg_dict[0:3]
        else:
            for i in range(3-word_neg_dict.__len__()):
                word_neg_dict.append(0)
        result  = word_pos_dict
        result.extend(word_neg_dict)
        return result

    def extract_all_feature(self,line):
        result = []
        words = self.wordTools.seperatewords(line)
        result.append(self.extract_pos_num(words))
        result.append(self.extract_pos_tfidf(words))
        result.append(self.extract_neg_num(words))
        result.append(self.extract_neg_tfidf(words))
        result.extend(self.extract_contains_keywords(words))
        result.extend(self.extract_most_relevant_words(words))
        result.append(self.extract_possible(line))
        if self.extract_nb_feature(line) != None:
            result.append(self.extract_nb_feature(line))
        else:
            result.append("none")
        if "pos" in line.lower():
            result.append("1")
        else:
            result.append("0")
        return result

    def extract_nb_feature(self,line):
        if "\t" in line:
            tmp= line.split("\t")
            if tmp.__len__() == 3:
                return tmp[1]
            else:
                return None

    def make_arff_file(self,file,savepath):
        content= self.wordTools.readFile(file)
        string="@relation arff_data2\n@attribute pos_num numeric\n@attribute pos_tfidf numeric\n@attribute neg_num numeric\n@attribute neg_tfidf numeric\n@attribute possible numeric\n@attribute class {0,1}\n@data\n"
        for line in content:
            result = self.extract_all_feature(line)
            string+= str(result)[1:-1]+"\n"
        # print(string)
        self.wordTools.saveIntoFile(savepath,string)



trainfile =ProjectDir.resourceDir+"Corpus\\20161108\\train.txt"
feature = FeatureExtractor()
feature.buildModel([trainfile])

# print(feature.extract_all_feature("上传动力方面更是不错，起步反应灵敏，涡轮介入比较积极，车速随着涡轮的介入，迅速的得以提升，发动机声音也比较清纯没有嘈杂音 pos"))
# savepath = ProjectDir.resourceDir+"Corpus\\trainfile.arff"
# testfile1 = ProjectDir.resourceDir+"Corpus\\20161108\\test10月-庆丽.txt"
# savepath1 = ProjectDir.resourceDir+"Corpus\\20161108\\test10月-庆丽-arff.arff"
# testfile2 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-万礼.txt"
# savepath2 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-万礼-arff.arff"
# testfile3 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-庆丽.txt"
# savepath3 = ProjectDir.resourceDir+"Corpus\\20161108\\test1107-庆丽-arff.arff"
# feature.make_arff_file(trainfile,savepath)
# print(savepath)
# feature.make_arff_file(testfile1,savepath1)
# print(savepath1)
# feature.make_arff_file(testfile2,savepath2)
# print(savepath2)
# feature.make_arff_file(testfile3,savepath3)
# print(savepath3)
#

testfile3 = ProjectDir.resourceDir+"Corpus\\20161108\\combine-1107qinli.txt"
savepath3 = ProjectDir.resourceDir+"Corpus\\20161108\\combine-1107qinli.arff"
feature.make_arff_file(testfile3,savepath3)