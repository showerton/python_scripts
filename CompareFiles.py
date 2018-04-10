'''Simple program to take a file having one column of IDs and check for duplicate IDs in file.
Rudimentary at best...
Written by Stacy Howerton, last modified 1 April 2015'''

#INPUT: 1) a .txt file having one column of IDs to use.  Other columns don't matter
#OUTPUT: results to screen                                                                                                        

#!/usr/bin/python
import os.path

def main():
    listMembers = parseFile(readFile(input(R'Enter the name of file:')))
    compareIDs(listMembers)

def compareIDs(AFile):
    ListUniques, ListDuplicates = [], []
    for item in AFile:
        if item not in ListUniques: ListUniques.append(item) 
        else: ListDuplicates.append(item)
    print ("There are %s duplicate IDs"%s(count(ListDuplicates)))
    

def readFile(AFileName):
    resultsLines = []
    if os.path.isfile(AFileName):
        results = open(AFileName, "r")
        resultsLines = results.readlines()
        results.close()
        return resultsLines
    else:
        print(R'Unable to find that file')
        exit(0)
    
def parseFile(content):
    i = int(input(R'What column are your IDs in? (number 1 - n)'))
    listInfo = []
    it = 0
    for line in content:
        item = line.split("\t")
        if it == 0: pass
        else: listInfo.append(item[i - 1].strip())
        it = it + 1
    return listInfo
    


if __name__ == "__main__": main()
