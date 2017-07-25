__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment as wordSegment
from ProjectDir import ProjectDir

class Dupicate:

    def dupicate(self,data):
        result =[]
        for val in set(data):
            if val.strip() != "":
                result.append(val)
        return  result


# data = [" 神州半岛三面环海，面积24平方公里，气候温和，是一个四季如春的阳光型半岛，也是大型旅游风景名胜区,pos"
#     ," 神州半岛三面环海，面积24平方公里，气候温和，是一个四季如春的阳光型半岛，也是大型旅游风景名胜区,pos"
#     ," 神州半岛三面环海，面积24平方公里，气候温和，是一个四季如春的阳光型半岛，也是大型旅游风景名胜区,pos"]
# du = Dupicate()
# print(du.dupicate(data))


def duplicateData3():
    du = Dupicate()
    wordTools = wordSegment()
    data = wordTools.readFile(ProjectDir.resourceDir+"Corpus/数据3.txt")
    result = du.dupicate(data)
    filepath =ProjectDir.resourceDir+"Corpus/数据3—duplicate.txt"
    wordTools.saveIntoFile_list(filepath,result)


def duplicateData5():
    du = Dupicate()
    wordTools = wordSegment()
    data = wordTools.readFile(ProjectDir.resourceDir+"Corpus/数据5.txt")
    result = du.dupicate(data)
    filepath =ProjectDir.resourceDir+"Corpus/数据5—duplicate.txt"
    wordTools.saveIntoFile_list(filepath,result)

def duplicateAllData(files,savepath):
    data =[]
    du = Dupicate()
    wordTools = wordSegment()
    for file in files:
        data += wordTools.readFile(file)
    result = du.dupicate(data)
    wordTools.saveIntoFile_list(savepath,result)


# duplicateData3()
# duplicateData5()

# files = [
#     ProjectDir.resourceDir+"Corpus/数据1.txt",
#     ProjectDir.resourceDir+"Corpus/数据2.txt",
#     ProjectDir.resourceDir+"Corpus/数据3.txt",
#     ProjectDir.resourceDir+"Corpus/数据5.txt"
# ]
# savepath = ProjectDir.resourceDir+"Corpus/allData.txt"
# duplicateAllData(files,savepath)