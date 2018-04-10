'''Simple program to take combined SQL query output that may
contain duplicates and find the duplicates, and the unique category counts
to a .txt file that can be used to compare.  Not elegant but quickly done...
Written by Stacy Howerton, 15 Oct 2014'''

#INPUT: a .txt file of all results that we want to get unique counts from
#OUTPUT: a .txt file with [category] \t [count] \n

#!/usr/bin/python
import os.path

dictMembers = {}
numDups = 0
file = ''
listMembers = []

def main():
    parseFile(readFile(input(R'Enter the name of your file:')))
    createOutput()
    output2 = open("UniqueMembers.txt", "w")
    for item in listMembers:
        output2.write(item.strip() + "\n")
    output2.close()

def createOutput():
    #Can count how many of each MemberType there are in results, non dups, put in file
    outputfile = file.replace(".txt", "_UniquesAnalysis.txt")
    output = open(outputfile, "w")

    for key in dictMembers.keys():
        #print(key, len(dictMembers[key]))
        output.write(key + "\t" + str(len(dictMembers[key]))+ "\n")

    output.close()
    print("The file %s was written"%(outputfile)) 
    
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
        memberNum, memberType = item[1].strip(), item[5].strip()
        if not memberNum.isdigit(): pass
        else: buildDict(memberNum, memberType)

def buildDict(mnum, mtype):
    if mtype in dictMembers:
        members = dictMembers[mtype]
        if mnum not in members:
            dictMembers[mtype].append(mnum)
            listMembers.append(mnum)
        else:
            global numDups
            numDups = numDups + 1
    else:
        dictMembers[mtype] = []
        dictMembers[mtype].append(mnum)
        listMembers.append(mnum)   


if __name__ == "__main__": main()
