__author__ = 'E440'
import jieba.posseg as jieba_posseg
import jieba
import re
import codecs
from ProjectDir import ProjectDir

def test(sentence):
    word = list(jieba_posseg.cut(sentence))
    for w in word:
        print(w.word,w.flag)


def observe_carwords():
    filepath = ProjectDir.resourceDir+"dict/百度汽车相关词库.txt"
    content  =codecs.open(filepath,"r","utf-8").read()
    lines = []
    for con in content.split("\r\n"):
        lines.append(con)
    result =[]
    # print(content)
    for con in lines:
        if con.__len__() >3:
            result.extend(list(jieba.cut(con)))
        else:
            result.extend(con)
    all_words = {}
    for word in result:
        if word.__len__() >1:
            if word not in all_words.keys():
                all_words[word] =0
            all_words[word]+=1
    result =set()
    for word in all_words.keys():
        if all_words[word] >3:
            result.add(word)

    print(result)


# observe_carwords()
# words = list(jieba.cut("雨刷喷水管"))
# print(words)

#
# file = ProjectDir.resourceDir+"dict/absolute_words"
# words = codecs.open(file,"r","utf-8").read()
# print(words)



word = [0.9,0.3,1.0,0.5]
word.sort(reverse = True)
print(str(word)[1:-1])
print(word)