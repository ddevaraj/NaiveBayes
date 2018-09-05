import sys, string,math

mainDict = dict()
priors = dict()
probFake,probTrue, probPos, probNeg = 0,0,0,0

stopWords = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]

def readModel():
    lineNo = 0
    with open("nbmodel.txt","r") as f:
        for line in f:
            if ':' in line:
                key, val = line.split(':',1)
                if(lineNo <=4):
                    priors[key]= val.strip(' ')
                else:
                    val = val.strip('[').replace(']','')
                    mainDict[key] = [(token.strip(' ')) for token in val.split(',')]
            lineNo +=1


def naiveBayes():
    global probFake,probTrue, probPos, probNeg
    outputFile = open("nboutput.txt",'w')
    with open("dev-text.txt", "r") as readFile :
        for line in readFile:
            lineID = line[:line.find(" ")]
            # lineIDList.append(lineID)
            newLine = " ".join(line.split()[3:-1])
            newLine = newLine.translate(None, string.punctuation).lower()
            tokenList = [word for word in newLine.split() if ((word not in stopWords))]
            finalList = ' '.join(tokenList)
            finalList = ''.join([i for i in finalList if not i.isdigit()])  # remove words which start or end with digits
            finalList = finalList.split()
            probFake, probTrue, probPos, probNeg = 0,0,0,0
            for token in finalList:
                if token in mainDict:
                    probFake += math.log(float(mainDict[token][0]))
                    probTrue += math.log(float(mainDict[token][1]))
                    probPos += math.log(float(mainDict[token][2]))
                    probNeg += math.log(float(mainDict[token][3]))
            probFake += math.log(float(priors['Fake']))
            probTrue += math.log(float(priors['True']))
            probPos += math.log(float(priors['Pos']))
            probNeg += math.log(float(priors['Neg']))
            if probFake > probTrue:
                class1 = "Fake"
            else:
                class1 = "True"
            if probPos > probNeg:
                class2 = "Pos"
            else:
                class2 = "Neg"
            # class1 = probFake > probTrue and "Fake" or "True"
            # class2 = probPos > probNeg and "Pos" or "Neg"
            outputFile.write((lineID.strip()) + " "+ class1+ " " +class2 + "\n")


def main():
    readModel()
    naiveBayes()

if __name__ == "__main__":
    main()