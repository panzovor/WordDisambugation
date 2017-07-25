__author__ = 'E440'
from src.Model.Model import Model

class GraphModel(Model):

    posTrainData =[]
    negTrainData =[]
    WordBag = {}
    posGraph = None
    negGraph = None

    def initWordBag(self,filepaths):
        self.loadFiles(filepaths)
        for posline in self.posCorpos:
            tmpwords = self.wordTools.seperatewords(posline)
            self.posTrainData.append(tmpwords)
            for word in tmpwords:
                if word in self.WordBag: continue
                else: self.WordBag[word] = self.WordBag.__len__()+1
        for negline in self.negCorpos:
            tmpwords = self.wordTools.seperatewords(negline)
            self.negTrainData.append(tmpwords)
            for word in tmpwords:
                if word in self.WordBag: continue
                else: self.WordBag[word] = self.WordBag.__len__()+1

        self.posGraph = [[0 for col in range(self.WordBag.__len__())] for row in range(self.WordBag.__len__())]
        self.negGraph = [[0 for col in range(self.WordBag.__len__())] for row in range(self.WordBag.__len__())]

    def buildGraph(self,filepaths):
        if self.posGraph == None or self.negGraph ==None:
            self.initWordBag(filepaths)
        for words in self.posTrainData:
                    for index in range(1,words.__len__()):
                        self.posGraph[words[index]][words[index-1]] +=1
        for words in self.negTrainData:
                    for index in range(1,words.__len__()):
                        self.negGraph[words[index]][words[index-1]] +=1



    def buildModel(self,filepaths):
        self.initWordBag(filepaths)
        self.buildGraph(filepaths)



    def saveModel(self,wordBagFile,GraphFile):
        wordBagContent =""
        for word in self.WordBag:
            wordBagContent+=word+","+str(self.WordBag[word])+"\n"
        self.wordTools.saveIntoFile(wordBagFile,wordBagContent,"utf-8")
        graphContent = ""
        for index in range(self.posGraph.__len__()):
            for indey in range(self.posCorpos.__len__()):
                graphContent+=str(self.posGraph[index][indey])+","
            graphContent = graphContent[0: graphContent.__len__()-1]+'\n'
        graphContent +="========\n"
        for index in range(self.negGraph.__len__()):
            for indey in range(self.negGraph.__len__()):
                graphContent += str(self.negGraph[index][indey])+","
            graphContent = graphContent[0: graphContent.__len__()-1]+"\n"
        self.wordTools.saveIntoFile(GraphFile,graphContent,"utf-8")


            

    def loadModel(self,wordBagPath, graphFilePath):
        graphcontent = self.wordTools.readFile(graphFilePath)
        self.wordTools.readFileWithDict(wordBagPath)
        index =0
        indey = 0
        for graphlin in graphcontent:
            for tmp in graphlin.split(","):
                self.posGraph[index][indey] = float(tmp)
                indey+=1
            index+=1

    # def predict(self,line):
    #     words = self.wordTools.seperatewords(line)
    #     for word in words:
    #
    #
    #
    # def test(self):