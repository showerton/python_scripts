'''Simple program to find duplicate ID in list
Written by Stacy Howerton, 16 Oct 2014'''

#INPUT: a .txt file of IDs where each one is on its own line
#OUTPUT: print to screen the duplicate IDs

#!/usr/bin/python
import os.path

membList, dupList = [], []
numDups = 0

def main():
    parseFile(readFile(input(R'Enter the name of your file:')))
    createOutput()

def createOutput():

    for ID in dupList:
        print("Duplicate ID: %s"%(ID)) 
    
def readFile(AFileName):
    if(os.path.isfile(AFileName)):
        results = open(AFileName, "r")
        resultsLines = results.readlines()
        results.close()
        global file
        file = AFileName
        
    else: readFile(input(R'Unable to find that file, please re-enter your file:'))
    return resultsLines

def parseFile(content):
    #Parse file contents, store in dictionary that is memberType: MemberNumber
    #Keep track of number of duplicates
    for line in content:
        item = line.split("\t")
        ID = item[0]
        if not ID.isdigit(): pass
        else: buildList(ID)

def buildList(ID):
    if ID not in membList: membList.append(ID)
    else:
        global numDups
        numDups = numDups + 1
        if ID in dupList: pass
        else:
            dupList.append(ID)
    

if __name__ == "__main__": main()
