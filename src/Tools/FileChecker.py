__author__ = 'E440'

import os

class FileChecker:
    def checkFile(self,filepath):
        exits = os.path.exists(filepath)
        if exits:
            return
        else:
            filepathDir = os.path.dirname(filepath)

            if os.path.exists(filepathDir):
                 return
            else:
                os.makedirs(filepathDir)
                return

