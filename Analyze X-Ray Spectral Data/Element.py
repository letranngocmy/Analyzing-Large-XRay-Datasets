class Element:

    def __init__(self,name,total):
        self.name = name
        self.total = total

    def getTotalIntensities(self):
        return self.total

    def getName(self):
        return self.name

    def summarizeData(self):
        from itertools import chain
        areas = list(chain.from_iterable(self.total))
        return len(list(filter(lambda x: (x > 0), areas))),sum(areas)

    def prepareDataForClustering(self,threshold):
        from sklearn import preprocessing
        normalized = preprocessing.normalize(self.total, norm='max')
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
