__author__ = 'E440'

class ClassfiierResult:
    string =""
    classType = None
    predict = False
    detailInfo =""

    def toString(self):
        tmp="";
        tmp +=self.string+"\t"
        # tmp += self.detailInfo+"\t"
        # tmp += "realType\t"+str(self.classType)+"\t"
        tmp += "predict\t"+str(self.predict)+"\t"
        tmp += self.detailInfo
        return  tmp
