__author__ = 'E440'
import os
class ProjectDir():

    projectDir = os.path.dirname(os.path.abspath(__file__))
    projectDir = projectDir.replace("\\","/")
    resourceDir = projectDir+"/resources/"



