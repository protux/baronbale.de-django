import sys, os
from os.path import isfile

def readFile(file):
    with open(file, "rb") as in_file:
        return in_file.read()

def mergeFiles(outerFile, innerFile):
    return outerFile + innerFile
    
def saveMergedFile(data, filename):
    with open (filename, "wb") as out_file:
        out_file.write(data)

def mergeFile(outerFile, innerFile, filename):
    return mergeFiles(outerFile, innerFile)
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("usage: %s <file 1> <file 2> <new Filename>" % sys.arv[0])
        
    file = mergeFile(sys.argv[1], sys.argv[2], sys.argv[3])
    saveMergedFile(file, sys.argv[3])
