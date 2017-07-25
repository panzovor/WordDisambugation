__author__ = 'E440'
from src.Tools.SeperateWords import wordSegment
from ProjectDir import ProjectDir
from src.Preprocess.Duplicate import Dupicate
from src.Preprocess.ExtractSentenceFromText import ExtractSentenceFromText

#
# words = wordSegment()
# print(words.carwords)
extractor = ExtractSentenceFromText()
line ="精致/跨界/大空间 高尔夫风神AX3高清图解	pos"
cars = set()
extractor.findCarWordsFromSentence(cars,line)
print(cars)