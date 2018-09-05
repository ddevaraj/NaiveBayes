import sys, string

mainDict = dict()
labelDict = {}
noFake, noTrue, noPos, noNeg = 0,0,0,0
priors = {}

stopWords = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]

def addToDict(list, val):
    for token in list:
        if(token in mainDict):
            mainDict[token][val] = mainDict[token][val] + 1
        else:
            mainDict[token] = [0,0,0,0]
            mainDict[token][val] = mainDict[token][val] + 1


def delLowFreqWords():
    for key,val in mainDict.items():
        if sum(val) <= 1:
            del mainDict[key]

def assignLabel(lineid, clas, finalList):
    #print("HElp", labelDict.get(lineid).get(clas))
    if labelDict.get(lineid).get(clas) == "Fake":
        addToDict(finalList, 0)
    if labelDict.get(lineid).get(clas) == "True":
        addToDict(finalList, 1)
    if labelDict.get(lineid).get(clas) == "Pos":
        addToDict(finalList, 2)
    if labelDict.get(lineid).get(clas) == "Neg":
        addToDict(finalList, 3)
    #print("labelDict",labelDict.__len__())

def smoothing():
    for key,val in mainDict.items():
        for i in range(0,4):
            mainDict[key][i] = mainDict[key][i]+1

def calLikelihood():
    global noFake,noTrue,noNeg,noPos
    print(mainDict)
    for key,val in mainDict.items():
        noFake = noFake + val[0]
        noTrue += val[1]
        noPos += val[2]
        noNeg += val[3]
    print(noFake,noTrue)
    classOneTotal = noFake + noTrue
    classTwoTotal = noPos + noNeg
    for key, val in mainDict.items():
        mainDict[key][0] = (mainDict[key][0]/float(noFake))
        mainDict[key][1] = (mainDict[key][1]/float(noTrue))
        mainDict[key][2] = (mainDict[key][2]/float(noPos))
        mainDict[key][3] = (mainDict[key][3]/float(noNeg))

def calPriors():
    classOneTotal = noFake + noTrue
    classTwoTotal = noPos + noNeg
    priors['Fake'] = float(noFake)/float(classOneTotal)
    priors['True'] = float(noTrue)/float(classOneTotal)
    priors['Pos'] = float(noPos)/float(classTwoTotal)
    priors['Neg'] = float(noNeg)/float(classTwoTotal)

def readData():
    with open("train-labeled.txt", "r") as f:
        for line in f:
            lineID = line[:line.find(" ")]
            #lineIDList.append(lineID)
            labelDict[lineID] = {'C1': line.split()[1], 'C2': line.split()[2]}
            newLine = " ".join(line.split()[3:-1])
            newLine = newLine.translate(string.punctuation).lower()
            tokenList = [word for word in newLine.split() if((word not in stopWords) and (word.isalnum()))]
            finalList = ' '.join(tokenList)
            finalList = ''.join([i for i in finalList if not i.isdigit()])  # remove words which start or end with digits
            finalList = finalList.split()
        #for lineid in lineIDList:
            if (lineID in labelDict.keys()):
                assignLabel(lineID, 'C1', finalList)
                assignLabel(lineID, 'C2', finalList)


def writeData():
    with open("nbmodel.txt",'w') as f:
        f.write("** Prior Probablities **\n")
        for key,val in priors.items():
            f.write('%s:%s\n' %(key,val))
        f.write("** Likelihood **\n")
        for key, val in mainDict.items():
            f.write('%s:%s\n' %(key,val))

def main():
   readData()
   delLowFreqWords()
   smoothing()
   calLikelihood()
   calPriors()
   writeData()





if __name__ == "__main__":
    main()