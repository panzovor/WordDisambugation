__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment
from src.Preprocess.Duplicate import Dupicate
import math
from ProjectDir import ProjectDir

class TfidfPreProcess:
    dupicate = Dupicate()
    wordTools = wordSegment()
    posCorpos =[]
    negCorpos =[]

    pos_tf = {}
    idf={}
    neg_tf = {}
    pos={}
    neg= {}


    def loadFiles(self,posfile,negfile):
        allFile =[]
        allFile.append(posfile)
        allFile.append(negfile)
        for filepath in allFile:
            if filepath== posfile:
                self.posCorpos.extend(self.wordTools.readFile(filepath))
            elif filepath==negfile:
                self.negCorpos.extend(self.wordTools.readFile(filepath))
            else:
                # print("other")
                for line in self.wordTools.readFile(filepath):
                    if(line.find("pos")>0):
                        self.posCorpos.append(line)
                    else :
                        self.negCorpos.append(line)
        self.posCorpos = self.dupicate.dupicate(self.posCorpos)
        self.negCorpos = self.dupicate.dupicate(self.negCorpos)
        print(self.posCorpos.__len__())
        print(self.negCorpos.__len__())

    def tf_idf(self):
        all =0
        counter = 0
        for line in self.posCorpos:
            counter+=1
            print("pos:"+str(counter)+"/"+str(self.posCorpos.__len__()))
            all = all+1
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
        counter =0
        for line in self.negCorpos:
            counter+=1
            print("neg:"+str(counter)+"/"+str(self.negCorpos.__len__()))
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

    def saveModels(self,posFilepath):

        # self.pos_tf= sorted(self.pos_tf.items(), key=lambda d:d[1], reverse = True)
        self.wordTools.saveDictIntoFile(posFilepath,self.pos_tf,"utf-8")
        # self.wordTools.saveDictIntoFile(negFilepath,self.neg_tf,"utf-8")

    def loadData(self,file):
        self.pos_tf = self.wordTools.readFileWityDict(file)

    def generateArff(self,posfile,negfile,tfidffile,savefile):
        self.loadData(tfidffile)
        self.loadFiles(posfile,negfile)
        title =""
        for string in self.pos_tf.keys():
            title+=string+","
        content = []
        content.append(title+",class\n")
        counter=0;
        for string in self.posCorpos:
            counter+=1
            print("pos"+str(counter)+"/"+str(self.posCorpos.__len__()))
            # line =""
            words = self.wordTools.seperatewords(string);
            for key in self.pos_tf.keys():
                if key in words:
                    content.append("1,")
                else:
                    content.append("0,")
            content.append("1")
            content.append("\n")
        counter =0
        for string in self.negCorpos:
            counter+=1
            print("neg"+str(counter)+"/"+str(self.negCorpos.__len__()))
            line =""
            words = self.wordTools.seperatewords(string);
            for key in self.pos_tf.keys():
                if key in words:
                    content.append("1,")
                else:
                    content.append("0,")
            content.append("0")
            content.append("\n")
        self.wordTools.saveIntoFile(savefile,"".join(content))





corposfile_pos = ProjectDir.resourceDir+"Corpus\文章2000篇_扩充.txt"
corposfile_neg = "E:\汽车消歧\数据\文章/noauto.txt"
filepath = ProjectDir.resourceDir+"TxtTfidf/tfidf.csv"
tfidfPreprocess = TfidfPreProcess()
# tfidfPreprocess.loadFiles(corposfile_pos,corposfile_neg);
# tfidfPreprocess.tf_idf();
# tfidfPreprocess.saveModels(filepath)

filepath1 = ProjectDir.resourceDir+"TxtTfidf/tfidf_arff.txt"
tfidfPreprocess.generateArff(corposfile_pos,corposfile_neg,filepath,filepath1)