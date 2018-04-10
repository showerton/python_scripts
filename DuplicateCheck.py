'''Simple program to take a file having one column of IDs and check for duplicate IDs in file.
Rudimentary at best...
Written by Stacy Howerton, last modified 1 April 2015'''

#INPUT: 1) a .txt file having one column of IDs to use.  Other columns don't matter
#OUTPUT: counts uniques/duplicates to screen.  Files for each written                                                                                                      

#!/usr/bin/python
import os.path

def main():
    origFileName = input(R'Enter the name of file:')
    listMembers = parseFile(readFile(origFileName))
    compareIDs(listMembers, origFileName)

def compareIDs(AList, OrigFile):
    ListTotal, ListUniques, ListDuplicates = [], [], []
    for item in AList:
        if item not in ListTotal: ListTotal.append(item) 
        else:
            if item not in ListDuplicates: ListDuplicates.append(item)
    for AnItem in ListTotal:
        if AnItem not in ListDuplicates: ListUniques.append(AnItem)
    print("There are %s total IDs in file"%(len(ListTotal)))
    print("There are %s duplicate IDs"%(len(ListDuplicates)))
    print("There are %s unique IDs"%(len(ListUniques)))
    duplicates = createOutput(ListDuplicates, OrigFile, "duplicates")
    uniques = createOutput (ListUniques, OrigFile, "uniques")
    print("Files %s and %s contain these results"%(duplicates, uniques))

def createOutput(AList, origFileName, flag):
    #Creates output file from list as input, naming it after the original file
    modifier = "_" + flag + ".txt"
    outputfile = origFileName.replace(".txt", modifier)
    output = open(outputfile, "w")
    for item in AList: output.write(item + "\n")
    output.close()
    return outputfile

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
        else:
            if item[i - 1] == '': pass
            else: listInfo.append(item[i - 1].strip())
        it = it + 1
    return listInfo
    


if __name__ == "__main__": main()
