__author__ = 'E440'
from src.Model.DiscriminationModel import  DiscriminationModel
from src.Model.TfIdfModels import TfidfModels
from src.Model.TfPerCarModel import TFPerCarModel
from src.Model.MultiModels import MultiModels
from ProjectDir import ProjectDir
from src.Model.MultiModel_tfidf_vector import MultiModel_tfidf_vector
from src.Model.VectorSpace import VectorSpace
import os
from src.Tools.SeperateWords import wordSegment as wordSegment

def predictSingleLine(line):
    model = TfidfModels()
    posSavefile = ProjectDir.resourceDir+"TfidfModel/pos.txt"
    negSavefile = ProjectDir.resourceDir+"TfidfModel/neg.txt"
    model.loadModel(posSavefile,negSavefile)
    return model.predict(line)


# result = predictSingleLine("话说回来，目前除了大众等少数几家品牌以外，其余双离合都能挑出几页纸的bug")
# print(result.toString())

def testModel(model ,trainData,testData,resultlog):
    result = model.test(trainData,testData)
    content = model.saveEvaluationResult(resultlog)
    # print(type(result))
    # print(result)
    return result+"\n"
    # print(content)

def GetFileNameAndExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return shotname,extension

def testAll():
    filpaths = [
        ProjectDir.resourceDir+"Corpus\data12\data\\file0"
        ,ProjectDir.resourceDir+"Corpus\data12\data\\file1"
        ,ProjectDir.resourceDir+"Corpus\data12\data\\file2"
        ,ProjectDir.resourceDir+"Corpus\data12\data\\file3"
        ,ProjectDir.resourceDir+"Corpus\data12\data\\file4"
    # ProjectDir.resourceDir+"Corpus\数据1.txt"
    # ProjectDir.resourceDir+"Corpus\数据2.txt"
    # ,ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt"
    # ,ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"
    # ,ProjectDir.resourceDir+"Corpus/noauto_filterResult.txt"
    # ,ProjectDir.resourceDir+"Corpus\文章2000篇_扩充.txt"
    # ProjectDir.resourceDir+"Corpus\seperate_allData_train.txt"
    # ,ProjectDir.resourceDir+"Corpus\seperate_allData_test.txt"
    ]
    bak = filpaths.copy()
    content =""
    for i in range(bak.__len__()):
        testFile = [filpaths[i]]
        name =GetFileNameAndExt(filpaths[i])[0]
        filpaths.remove(filpaths[i])

        # print(name)
        prefix =ProjectDir.resourceDir+"Corpus/data12/observationOfResult//crossvalidationResult/"
        evalationDetails =  prefix+"/new_tfPerCar_"+name+".txt"
        evalationDetails1 =  prefix+"/new_tfidf_"+name+".txt"
        evalationDetails2 =  prefix+"/new_disc_"+name+".txt"
        evalationDetails3 =  prefix+"/new_vector_"+name+".txt"
        evalationDetails4 =  prefix+"/new_mult_tfidf_vect_"+name+".txt"
        model = TFPerCarModel()
        content += testModel(model, filpaths,testFile,evalationDetails)
        model = TfidfModels()
        content += testModel(model, filpaths,testFile,evalationDetails1)
        model = DiscriminationModel()
        content += testModel(model, filpaths,testFile,evalationDetails2)
        model = VectorSpace()
        content += testModel(model, filpaths,testFile,evalationDetails3)
        model = MultiModel_tfidf_vector()
        content += testModel(model, filpaths,testFile,evalationDetails4)
        filpaths = bak.copy()
    print(content)
    resultfile  = prefix+"result.txt"
    wordTools = wordSegment()
    wordTools.saveIntoFile(resultfile,content,"utf-8")

testAll()

#
# filpaths = [
#     ProjectDir.resourceDir+"Corpus\数据1.txt"
#     # ,ProjectDir.resourceDir+"Corpus\数据2.txt"
#     ,ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt"
#     ,ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"
#     # ,ProjectDir.resourceDir+"Corpus/noauto_filterResult.txt"
#     # ,ProjectDir.resourceDir+"Corpus\文章2000篇_扩充.txt"
#     # ProjectDir.resourceDir+"Corpus\seperate_allData_train.txt"
#     ]
# testFile = [
#     # ProjectDir.resourceDir+"Corpus\数据1.txt",
#     ProjectDir.resourceDir+"Corpus\数据2.txt"
# # ProjectDir.resourceDir+"Corpus\seperate_allData_test.txt"
# #     ProjectDir.resourceDir+"Corpus\数据3—duplicate.txt"
# #     ProjectDir.resourceDir+"Corpus\数据5—duplicate.txt"
#     # ,ProjectDir.resourceDir+"Corpus/noauto_filterResult.txt"
#     # ,ProjectDir.resourceDir+"Corpus\文章2000篇_扩充.txt"
#     ]
# # evalationDetails = ProjectDir.resourceDir+"ModelEvaluationResult/new_tfPerCar.txt"
# # evalationDetails1 = ProjectDir.resourceDir+"ModelEvaluationResult/new_tfidf.txt"
# # evalationDetails2 = ProjectDir.resourceDir+"ModelEvaluationResult/new_disc.txt"
# evalationDetails3 = ProjectDir.resourceDir+"ModelEvaluationResult/new_vector.txt"
# # evalationDetails4 = ProjectDir.resourceDir+"ModelEvaluationResult/new_mult_tfidf_vect.txt"
# #
# # model = TFPerCarModel()
# # # testModel(model, filpaths,testFile,evalationDetails)
# # # model = TfidfModels()
# # # testModel(model, filpaths,testFile,evalationDetails1)
# # # model = DiscriminationModel()
# # # testModel(model, filpaths,testFile,evalationDetails2)
# model = VectorSpace()
# testModel(model, filpaths,testFile,evalationDetails3)
# # # model = MultiModel_tfidf_vector()
# # testModel(model, filpaths,testFile,evalationDetails4)
#

