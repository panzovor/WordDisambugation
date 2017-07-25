__author__ = 'E440'
import math
import re
from src.Result.ClassifierResult import ClassfiierResult
from src.Model.Model import Model
from ProjectDir import ProjectDir



class TfidfModels(Model):

    possible = {}
    pos_tf = {}
    idf={}
    neg_tf = {}
    # pos={}
    # neg= {}

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

    def buildModel(self,filepaths):
        self.loadFiles(filepaths)
        self.tf_idf()
        self.saveModelsDefault()

    def saveModelsDefault(self):
        posSavefile = ProjectDir.resourceDir+"TfidfModel/pos.txt"
        negSavefile = ProjectDir.resourceDir+"TfidfModel/neg.txt"
        self.saveModels(posSavefile,negSavefile)

    def saveModels(self,posFilepath,negFilepath):
        self.wordTools.saveDictIntoFile(posFilepath,self.pos_tf,"utf-8")
        self.wordTools.saveDictIntoFile(negFilepath,self.neg_tf,"utf-8")

    def loadModelDefault(self):
        posSavefile = ProjectDir.resourceDir+"TfidfModel/pos.txt"
        negSavefile = ProjectDir.resourceDir+"TfidfModel/neg.txt"
        self.loadModel(posSavefile,negSavefile)

    def loadModel(self,posfile,negfile,possiblefile =""):
        self.pos = self.wordTools.readFileWityDict(posfile)
        self.neg = self.wordTools.readFileWityDict(negfile)
        if possiblefile != "":
            self.loadPossibleData(possiblefile)

    def loadPossibleData(self,filepath):
        content = self.wordTools.readFileWityDict_(filepath)
        for string in content:
            # print(content[string])
            pos = content[string][0]
            neg = content[string][1]
            if pos  == 0: pos =1
            if neg  ==0 : neg =1
            content[string].append((pos)/(pos+neg))
        self.possible  = content


    def compareByRate(self,pos_intersection,neg_intersection):
        intersection = set(pos_intersection).intersection(set(neg_intersection))
        value = 1
        for word in intersection:
            value*=float(self.pos[word]) / float(self.neg[word])
        # print(value)
        if value>1 :return True
        else : return False


    def compareByCountAll(self,pos_intersection, neg_intersection):
        intersection = set(pos_intersection).intersection(set(neg_intersection))
        poscount =0
        negcount =0
        for word in intersection:
            poscount = poscount + float(self.pos_tf[word])
            negcount = negcount + float(self.neg_tf[word])
            # for word in intersection:
            #     if(self.pos[word] > self.neg[word]):
            #         poscount = poscount +1
            #     else:
            #         negcount = negcount +1
        # print(str(poscount)+" "+str(negcount))
        if(poscount>= negcount):
            return True
        else:
            return False

    def getMax(self,intersection,pos =True):
        max =0
        maxWord =""
        tmp =None
        for word in intersection:
            if pos:
                tmp = self.pos_tf
            if not pos:
                tmp = self.neg_tf
            if float(tmp[word]) > max:
                max = float(tmp[word])
                maxWord = word
                # print(word)
        return maxWord


    def compareByTopMax(self,pos_intersection, neg_intersection):
        pos_max= self.getMax(pos_intersection)
        neg_max= self.getMax(neg_intersection,False)
        if pos_max == "" or neg_max == "":
            return False
        if self.pos_tf[pos_max] > self.neg_tf[neg_max]:
            return True
        else:
            return False

    def compareByWins(self,pos_intersection,neg_intersection):
        pos_count =0
        neg_count =0;
        tmp  = set(pos_intersection).intersection(set(neg_intersection))
        if(tmp.__len__() == 0):
            return self.compareByTopMax(pos_intersection,neg_intersection)
        for word in tmp:
            if float(self.pos_tf[word]) > float(self.neg_tf[word]):
                pos_count+=1
            else:
                neg_count +=1
        if pos_count >neg_count:
            return True
        else:
            return False;

    def compareByNumAndTfidf(self,pos_intersection,neg_intersection):
        if pos_intersection.__len__() > neg_intersection.__len__() :
            return True;
        elif pos_intersection.__len__() < neg_intersection.__len__():
            return False;
        else :
            return self.compareByCountAll(pos_intersection,neg_intersection)

    def compareByPossibleAndTfidf(self,pos_intersection,neg_intersection):
        posCount =0
        negCount =0
        carword=""
        self.possible[""] = [1,1,0.5]

        for word in pos_intersection:
            if word in self.possible:
                carword = word
                break
        # if pos_intersection.__len__()*self.possible[carword][2] > neg_intersection.__len__()*(1-self.possible[carword][2]) :
        #     return True;
        # elif pos_intersection.__len__()*self.possible[carword][2] < neg_intersection.__len__()*(1-self.possible[carword][2]):
        #     return False;
        for posword  in pos_intersection:
            posCount+= self.possible[carword][2] * float(self.pos[posword])
        for negword in neg_intersection:
            negCount+= (1-self.possible[carword][2]) * float(self.neg[negword])
        if posCount > negCount:
            return True
        else:
            return False


    def predict(self,line):
        result = ClassfiierResult()
        detailInfo = ""
        result.string = line
        words = self.wordTools.seperatewords(line = line)
        contains = list(set(words).intersection(self.wordTools.absolute_words))

        pos_intersection =set(words).intersection(set(self.pos_tf.keys()))
        neg_intersection =set(words).intersection(set(self.neg_tf.keys()))
        if contains.__len__()>0:
            for i in range(contains.__len__()):
                key_str = "absolute"+str(i)+":"+contains[i]+"("+str(contains[i])+")"
                pos_intersection.add(key_str)
                if key_str not in self.pos_tf.keys():
                    self.pos_tf[key_str] =500
                    self.idf[key_str] = 1
        detailInfo +="pos:["
        for word in pos_intersection:
            detailInfo += word+":"+str(self.pos_tf[word])+","
        detailInfo+="], neg =["
        for word in neg_intersection:
            detailInfo +=word+","+str(self.neg_tf[word])+","
        detailInfo+="]"
        result.detailInfo = detailInfo
        # result.predict = self.compareByCountAll(pos_intersection,neg_intersection)
        # result.predict = self.compareByPossibleAndTfidf(pos_intersection,neg_intersection)
        # result.predict = self.compareByTopMax(pos_intersection,neg_intersection)
        # result.predict = self.compareByWins(pos_intersection,neg_intersection)
        result.predict = self.compareByNumAndTfidf(pos_intersection,neg_intersection)
        # result.predict = self.compareByPossibleAndTfidf(pos_intersection,neg_intersection)
        # result.predict = self.compareByRate(pos_intersection,neg_intersection)

        return result


    def test(self,trainFiles,testFile):
        self.eval.className = "tfidf"
        self.eval.trainData = trainFiles
        self.eval.testData = testFile
        posSavefile = ProjectDir.resourceDir+"TfidfModel/pos.txt"
        negSavefile = ProjectDir.resourceDir+"TfidfModel/neg.txt"
        possiblefile = ProjectDir.resourceDir+"TfidfModel\data1.csv"
        self.buildModel(filepaths=trainFiles)
        self.saveModels(posSavefile,negSavefile)
        self.loadModel(posSavefile,negSavefile,possiblefile)
        self.loadTestData(testFile)
        return  self.evaluateModel()

    def demo(self):
        trainFile =[
            ProjectDir.resourceDir+"Corpus\seperate_allData_train.txt"
        ]
        # line = "不管从外观还是性能上看，高尔夫这款车型简直太差了	pos"
        line ="宝马对3系的悬架系统作了不少改进 pos"
        self.buildModel(filepaths=trainFile)
        posSavefile = ProjectDir.resourceDir+"TfidfModel/pos.txt"
        negSavefile = ProjectDir.resourceDir+"TfidfModel/neg.txt"
        # possiblefile = ProjectDir.resourceDir+"TfidfModel\data1.csv"
        self.saveModels(posSavefile,negSavefile)
        print(self.predict(line).toString())

# model = TfidfModels()
# model.demo()
