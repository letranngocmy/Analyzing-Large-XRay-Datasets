class Element:

    def __init__(self,fileName,directory):
        try:
            self.concentrations = []
            f = open(directory + "/" + fileName, "r")
            bool = False
            self.nRow = 0
            self.nCol = 0
            for line in f:
                self.nRow += 1
                nCol = 0
                numbers = []
                strs = line.split(" ")
                for str in strs:
                    nCol += 1
                    substrs = str.split("e")
                    if float(substrs[0]) >= 0:
                        if len(substrs) == 1:
                            numbers.append(round(float(substrs[0]), 10))
                        else:
                            numbers.append(round(float(substrs[0]) * (10 ** float(substrs[1])), 10))
                    else:
                        bool = True
                        break
                if bool == True:
                    break
                else:
                    if self.nCol == 0 and nCol != 0:
                        self.nCol = nCol
                    else:
                        if self.nCol == nCol:
                            self.concentrations.append(numbers)
                        else:
                            bool = True
                            break
            if bool == False and self.concentrations != []:
                substrs = fileName.split("_")
                self.elementName = substrs[0]
                self.emissionLine = substrs[1]
                from itertools import chain
                concentrations = list(chain.from_iterable(self.concentrations))
                self.nPositive = len(list(filter(lambda x: (x > 0), concentrations)))
                self.sumConcentrations = sum(concentrations)
            else:
                self.concentrations = []
                self.elementName = None
                self.emissionLine = None
                self.nPositive = None
                self.sumConcentrations = None
                self.nRow = 0
                self.nCol = 0
        except:
            self.concentrations = []
            self.elementName = None
            self.emissionLine = None
            self.nPositive = None
            self.sumConcentrations = None
            self.nRow = 0
            self.nCol = 0

    def getNRow(self):
        return self.nRow

    def getNCol(self):
        return self.nCol

    def getNPositive(self):
        return self.nPositive

    def getSumConcentrations(self):
        return self.sumConcentrations

    def getElementName(self):
        return self.elementName

    def getEmissionLine(self):
        return self.emissionLine

    def getConcentrations(self):
        return self.concentrations

    def denoise(self,threshold):
        for i in range(0,len(self.concentrations)):
            for j in range(0,len(self.concentrations[0])):
                if self.concentrations[i][j] < threshold:
                    self.concentrations[i][j] = 0

    def prepareDataForClustering(self,threshold):
        from sklearn import preprocessing
        normalized = preprocessing.normalize(self.concentrations, norm='max')
        normalized = [x * 100 for x in normalized]
        X = []
        Y = []
        values = []
        for i in range(0, len(normalized)):
            for j in range(0, len(normalized[0])):
                if normalized[i][j] > 0 and normalized[i][j] >= threshold:
                    X.append(j)
                    Y.append(i)
                    values.append(normalized[i][j])
        import numpy as np
        return np.array(list(zip(X, Y))), values
