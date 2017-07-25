__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment as wordSegment
from ProjectDir import ProjectDir

class ArffGenerator:
    possible = {}
    pos ={}
    neg ={}
    wordTools = wordSegment()

    def loadPossibleData(self,filepath):
        content = self.wordTools.readFileWityDict_(filepath)
        for string in content:
            # print(content[string])
            pos = content[string][0]
            neg = content[string][1]
            if pos  == 0: pos =1
            if neg  ==0 : neg =1
            content[string].append((pos)/(pos+neg))
        content[""]=[1,1,0.5]
        self.possible  = content

    def countTfidf(self,intersection,corpos):
        result =0
        for line in intersection:
            result+= float(corpos[line])
        return result;

    def getCarWords(self,intersection):
        for word in intersection:
            if word in self.wordTools.carwords:
                return word
        return ""

    def generateWithTfidf_num_possible(self,dataFiles,posfile,negfile,possiblefile,savefile=""):
        self.pos = self.wordTools.readFileWityDict(posfile)
        self.neg = self.wordTools.readFileWityDict(negfile)
        if possiblefile != "":
            self.loadPossibleData(possiblefile)
        data=[]
        for dataFile in dataFiles:
            data.extend( self.wordTools.readFile(dataFile))
        arffContent ="pos_num,pos_tfidf,neg_num,neg_tfidf,possible,class\n"

        for line in data:
            tmp = self.wordTools.seperatewords(line)
            pos_intersection = set(self.pos).intersection(set(tmp))
            neg_intersection = set(self.neg).intersection(set(tmp))
            arffContent+= str(pos_intersection.__len__())+","
            arffContent+= str(self.countTfidf(pos_intersection,self.pos))+","
            arffContent+= str(neg_intersection.__len__())+","
            arffContent+= str(self.countTfidf(neg_intersection,self.neg))+","
            if self.getCarWords(tmp) in self.possible:
                arffContent+= str(self.possible[self.getCarWords(tmp)][2])+","
            else:
                arffContent+="0.5,"
            if line.find("pos") >0 : arffContent+="1\n"
            else: arffContent+="0\n"
        if savefile !="":
            self.wordTools.saveIntoFile(savefile,arffContent,"utf-8")
        print(arffContent)


pos_file = ProjectDir.resourceDir+"TfidfModel/pos.txt"
neg_file = ProjectDir.resourceDir+"TfidfModel/neg.txt"
possible_file = ProjectDir.resourceDir+"TfidfModel\data1.csv"
datafile =ProjectDir.resourceDir+"Corpus\数据2.txt"
savefile = ProjectDir.resourceDir+"TfidfModel/arff_data2.csv"
arffgenerator  = ArffGenerator()
arffgenerator.generateWithTfidf_num_possible(datafile,pos_file,neg_file,possible_file,savefile)


