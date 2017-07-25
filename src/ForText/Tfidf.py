__author__ = 'E440'
import jieba
import math

import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class Tfidf:

  def __init__(self):
    self.weight=None
    # self.idf =None
    self.wordbag= {}

  def getTfidf(self,corpus):
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tf = vectorizer.fit_transform(corpus)
    # print(tf.toarray())
    tfidf=transformer.fit_transform(tf)#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
    # self.idf = transformer.idf_
    # print(self.idf)
    for i in range(len(word)):
      self.wordbag[word[i]] = i
    self.weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    # for i in range(len(self.weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    #   print(u"-------这里输出第",i,u"类文本的词语tf-idf权重------")
    #   for j in range(len(word)):
    #     print (word[j],self.weight[i][j])

  def getVector(self,index,corpus):
    result ={}
    for word in corpus.split(" "):
      if word in self.wordbag:
        result[word] = self.weight[index][self.wordbag[word]]
    return result




# corpus =["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开
#     "他 来到 了 网易 杭研 大厦",#第二类文本的切词结果
#     "小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果
#     "我 爱 北京 天安门 天安门"]
# tfidf = Tfidf()
# tfidf.getTfidf(corpus)
# result = tfidf.getVector(1,"我 来到 北京 清华大学")
# print(result)
#
# print((1/3) * math.log(2))
# print((2/3) * math.log(4))
# print(0.78528827571/1.91)
# print(tfidf.wordbag)
# print(tfidf.idf)
