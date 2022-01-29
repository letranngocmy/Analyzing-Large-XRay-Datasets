class ElementBook:

    def __init__(self,path):
        self.path = path
        self.elements = []
        self.text = None
        self.string = None
        self.count = 0

    def getPath(self):
        return self.path

    def getElements(self):
        return self.elements

    def getText(self):
        return self.text

    def getString(self):
        return self.string

    def getElementNames(self):
        names = []
        for i in range(0, len(self.elements)):
            names.append(self.elements[i].getElementName())
        return names

    def getEmissionLines(self):
        emissionLines = []
        for i in range(0, len(self.elements)):
            emissionLines.append(self.elements[i].getEmissionLine())
        return emissionLines

    def insertElement(self, element, threshold):
        element.denoise(threshold)
        self.elements.append(element)

    def getIndex(self,elementName,emissionLine):
        indices = []
        for i in range(0,len(self.elements)):
            if self.elements[i].getElementName() == elementName:
                indices.append(i)
        if len(indices) == 0:
            print("The chosen dataset does not contain the data of " + elementName + " " + emissionLine + " Line.")
            return -1
        else:
            for i in indices:
                if self.elements[i].getEmissionLine() == emissionLine:
                    return i
            print("The chosen dataset does not contain the data of " + elementName + " " + emissionLine + " Line.")
            return -1

    def getObjectType(self,elementName,emissionLine):
        index = self.getIndex(elementName,emissionLine)
        if index != -1:
            return self.elements[index]
        else:
            return None

    def getConcentrationsByElement(self,elementName,emissionLine):
        i = self.getIndex(elementName,emissionLine)
        if i == -1:
            return None
        else:
            return self.elements[i].getConcentrations()

    def getConcentrationsOfPixel(self,row,col):
        concentrations = []
        for e in self.elements:
            concentrations.append(e.getConcentrations()[row][col])
        return concentrations

    def plotConcentrationsByElementIndex(self,i):
        self.text = None
        e = self.elements[i]
        concentrations = e.getConcentrations()
        if concentrations == []:
            self.text = "Data unavailable."
            print(self.text)
        else:
            elementName = e.getElementName()
            emissionLine = e.getEmissionLine()
            if e.getNPositive() == 0:
                self.text = "The signal of " + elementName + " " + emissionLine + " Line is not found."
                print(self.text)
            else:
                print("The signal of " + elementName + " " + emissionLine + " Line is found.")
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                p = ax.imshow(concentrations)
                cb = plt.colorbar(p, shrink=0.5)
                ax.set_xlabel('Column')
                ax.set_ylabel('Row')
                cb.set_label('Concentration')
                plt.title("Concentrations of " + elementName + " " + emissionLine + " Line")
                fileName = self.path + "/" + elementName + "-" + emissionLine + ".png"
                plt.savefig(fileName)
                plt.close(fig)
                self.count += 1

    def plotConcentrationsByElement(self, elementName, emissionLine):
        index = self.getIndex(elementName,emissionLine)
        if index != -1:
            self.plotConcentrationsByElementIndex(index)

    def plotAllElementsConcentrations(self):
        self.count = 0
        for i in range(0,len(self.elements)):
            self.plotConcentrationsByElementIndex(i)

    def getCount(self):
        return self.count

    def getNRow(self):
        return len(self.elements[0].getConcentrations())

    def getNCol(self):
        return len(self.elements[0].getConcentrations()[0])

    def getSSE(self, data,values,maxClusters):  # Elbow method
        from sklearn.cluster import KMeans
        kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
        sse = []  # A list holds the SSE values for each k
        n = maxClusters+1
        if n > len(data) + 1:
            n = len(data) + 1
        for k in range(1, n):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            if values != None:
                kmeans.fit(data, sample_weight=values)
            else:
                kmeans.fit(data)
            sse.append(kmeans.inertia_)
        return sse

    def getSilhouetteCoefs(self, data, values, maxClusters):
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
        silhouette_coefficients = []
        n = maxClusters+1
        if n > len(data):
            n = len(data)
        for k in range(2, n):  # Start at 2 clusters for silhouette coefficient
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            if values != None:
                kmeans.fit(data, sample_weight=values)
            else:
                kmeans.fit(data)
            silhouette_coefficients.append(silhouette_score(data, kmeans.labels_))
        return silhouette_coefficients

    def getClusteringData(self,data,values,k):
        from sklearn.cluster import KMeans
        kmeans = KMeans(init="random", n_clusters=k, n_init=10, max_iter=300)
        if values != None:
            kmeans.fit(data, sample_weight=values)
        else:
            kmeans.fit(data)
        return kmeans.predict(data), kmeans.cluster_centers_ #y_kmeans, centers

    def clusteringByPixelLocations_OneElement(self, object, locations, values, threshold, maxClusters):
        self.text = None
        name = object.getElementName()
        emissionLine = object.getEmissionLine()
        if (len(locations) > 1):
            string = name + " " + emissionLine + " Line"
            self.string = name + "-" + emissionLine + "_threshold" + str(threshold) + "_maxNClusters" + str(maxClusters)
            import matplotlib.pyplot as plt
            sse = self.getSSE(locations, values,maxClusters-1)
            from kneed import KneeLocator
            kl = KneeLocator(range(1, len(sse) + 1), sse, curve="convex", direction="decreasing")
            K = kl.elbow
            plt.plot(range(1, len(sse) + 1), sse)
            plt.xticks(range(1, len(sse) + 1))
            plt.xlim(1, len(sse))
            plt.xlabel("Number of Clusters")
            plt.ylabel("SSE")
            plt.title("Results of Elbow Method From Positive Concentrations of " + string + ": k = " + str(K))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.path + "/Locations_ElbowMethod_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            silhouetteCoefs = self.getSilhouetteCoefs(locations, values,maxClusters-1)
            newK = silhouetteCoefs.index(max(silhouetteCoefs)) + 2
            plt.plot(range(2, len(silhouetteCoefs) + 2), silhouetteCoefs)
            plt.xticks(range(2, len(silhouetteCoefs) + 2))
            plt.xlim(2, len(silhouetteCoefs) + 1)
            plt.xlabel("Number of Clusters")
            plt.ylabel("Silhouette Coefficient")
            plt.title("Silhouette Coefficients Resulting From Positive Concentrations of " + string + ": k = " + str(newK))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.path + "/Locations_SilhouetteCoefs_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            if K == None or K < newK:
                K = newK
            y_kmeans, centers = self.getClusteringData(locations, values, K)
            allLabels = [[0 for j in range(self.getNCol())] for i in range(self.getNRow())]
            for n in range(0, len(locations)):
                j = locations[n][0]
                i = locations[n][1]
                allLabels[i][j] = y_kmeans[n] + 1
            import numpy as np
            cmap = plt.get_cmap('RdBu', np.max(allLabels) - np.min(allLabels) + 1)
            mat = plt.matshow(allLabels, cmap=cmap, vmin=np.min(allLabels) - .5, vmax=np.max(allLabels) + .5)
            cax = plt.colorbar(mat, ticks=np.arange(np.min(allLabels), np.max(allLabels) + 1))
            plt.xlabel("Column")
            plt.ylabel("Row")
            cax.set_label('Cluster')
            plt.title("K-Means Clustering With " + string)
            fileName = self.path + "/Locations_Clusters_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            # import pandas as pd
            # df1 = pd.DataFrame({'column': locations[:, 0], 'row': locations[:, 1], 'cluster': y_kmeans, 'concentration': values})
            # df1['cluster'] = df1['cluster'].astype(str)
            # df2 = pd.DataFrame({'column': centers[:, 0], 'row': centers[:, 1]})
            # import plotnine as p9
            # myPlot = p9.ggplot() + \
            #          p9.geom_point(data=df1,mapping=p9.aes(x='column', y='row', color='cluster', size='concentration'),alpha=0.4) + \
            #          p9.geom_point(data=df2,mapping=p9.aes(x='column',y='row'), color='black',size=3, shape=',') + \
            #          p9.scale_color_discrete(name="Cluster") + p9.scale_size_continuous(name="Normalized Concentration") + \
            #          p9.scale_y_reverse(lim=[self.getNRow() - 1, 0]) + p9.scale_x_continuous(limits=[0, self.getNCol() - 1]) + \
            #          p9.xlab("Column") + p9.ylab("Row") + p9.theme_bw() + \
            #          p9.ggtitle("K-Means Clustering With " + string)
            # fileName = self.path + "/Locations_Clusters_" + self.string + ".png"
            # myPlot.save(fileName)
            # plt.close()
        elif len(locations) == 1:
            self.text = "After denoising, only one pixel (" + str(locations[0][1]) + ", " + str(locations[0][0]) + ") shows signal of " + name + " " + emissionLine + " Line."
            print(self.text)
        else:
            self.text = "After denoising, no pixel shows signal of " + name + " " + emissionLine + " Line."
            print(self.text)

    def findClustersByPixelLocations_AllElements(self,threshold,maxClusters):
        self.count = 0
        for object in self.elements:
            if object.getNPositive() > 0:
                locations, values = object.prepareDataForClustering(threshold)
                self.clusteringByPixelLocations_OneElement(object, locations, values, threshold,maxClusters)
                self.count += 1
            else:
                print("After denoising, no pixel shows signal of " + object.getElementName() + " " + object.getEmissionLine() + " Line.")

    def clusteringByConcentrations_OneElementPair(self, element1, element2, maxClusters):
        self.text = None
        try:
            import matplotlib.pyplot as plt
            concentrations1 = element1.getConcentrations()
            concentrations2 = element2.getConcentrations()
            from itertools import chain
            concentrations1 = list(chain.from_iterable(concentrations1))
            concentrations2 = list(chain.from_iterable(concentrations2))
            import numpy as np
            data = np.array(list(zip(concentrations1, concentrations2)))
            name1 = element1.getElementName()
            name2 = element2.getElementName()
            emissionLine1 = element1.getEmissionLine()
            emissionLine2 = element2.getEmissionLine()
            string = name1 + " " + emissionLine1 + " Line and " + name2 + " " + emissionLine2 + " Line"
            self.string = name1 + "-" + emissionLine1 + "_" + name2 + "-" + emissionLine2 + "_maxNClusters" + str(
                maxClusters)
            sse = self.getSSE(data, None, maxClusters)
            from kneed import KneeLocator
            kl = KneeLocator(range(1, len(sse) + 1), sse, curve="convex", direction="decreasing")
            K = kl.elbow
            plt.plot(range(1, len(sse) + 1), sse)
            plt.xticks(range(1, len(sse) + 1))
            plt.xlim(1, len(sse))
            plt.xlabel("Number of Clusters")
            plt.ylabel("SSE")
            plt.title("Elbow Method With " + string + ": k = " + str(K))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.getPath() + "/Concentrations_ElbowMethod_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            silhouetteCoefs = self.getSilhouetteCoefs(data, None, maxClusters)
            newK = silhouetteCoefs.index(max(silhouetteCoefs)) + 2
            plt.plot(range(2, len(silhouetteCoefs) + 2), silhouetteCoefs)
            plt.xticks(range(2, len(silhouetteCoefs) + 2))
            plt.xlim(2, len(silhouetteCoefs) + 1)
            plt.xlabel("Number of Clusters")
            plt.ylabel("Silhouette Coefficient")
            plt.title("Silhouette Coefficients Resulting From " + string + ": k = " + str(newK))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.getPath() + "/Concentrations_SilhouetteCoefs_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            if K == None or K < newK:
                K = newK
            y_kmeans, centers = self.getClusteringData(data, None, K)
            import pandas as pd
            df1 = pd.DataFrame({'element1': concentrations1, 'element2': concentrations2, 'cluster': y_kmeans})
            df1['cluster'] = df1['cluster'].astype(str)
            df2 = pd.DataFrame({'element1': centers[:, 0], 'element2': centers[:, 1]})
            import plotnine as p9
            myPlot = p9.ggplot() + \
                     p9.geom_point(data=df1, mapping=p9.aes(x='element1', y='element2', color='cluster'), alpha=0.4) + \
                     p9.scale_color_discrete(name="Cluster") + p9.theme_bw() + \
                     p9.geom_point(data=df2, mapping=p9.aes(x='element1', y='element2'), color='black', size=3,
                                   shape=',') + \
                     p9.xlab("Concentration of " + name1 + " " + emissionLine1 + " Line") + p9.ylab(
                "Concentration of " + name2 + " " + emissionLine2 + " Line") + \
                     p9.ggtitle("K-Means Clustering With " + string)
            fileName = self.getPath() + "/Concentrations_Clusters_scatter_" + self.string + ".png"
            myPlot.save(fileName)
            plt.close()
            allLabels = np.array(y_kmeans).reshape((self.getNRow(), self.getNCol()))
            cmap = plt.get_cmap('RdBu', np.max(allLabels) - np.min(allLabels) + 1)
            mat = plt.matshow(allLabels, cmap=cmap, vmin=np.min(allLabels) - .5, vmax=np.max(allLabels) + .5)
            cax = plt.colorbar(mat, ticks=np.arange(np.min(allLabels), np.max(allLabels) + 1))
            plt.xlabel("Column")
            plt.ylabel("Row")
            cax.set_label('Cluster')
            plt.title("K-Means Clustering With " + string)
            fileName = self.getPath() + "/Concentrations_Clusters_pcolor_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
        except:
            self.text = "The data of at least one of the selected elements is unavailable."
            print(self.text)

    def findClustersByConcentrations_AllElementPairs(self,maxClusters):
        self.count = 0
        for i in range(0, len(self.elements)-1):
            if self.elements[i].getNPositive() > 0:
                j = i+1
                while j < len(self.elements):
                    if self.elements[j].getNPositive() > 0:
                        self.clusteringByConcentrations_OneElementPair(self.elements[i],self.elements[j],maxClusters)
                        self.count += 1
                    else:
                        if i == 0:
                            print("After denoising, no pixel shows signal of " + self.elements[j].getElementName() + " " +
                                self.elements[j].getEmissionLine() + " Line.")
                    j += 1
            else:
                if i == 0:
                    print("After denoising, no pixel shows signal of " + self.elements[0].getElementName() + " " +
                          self.elements[0].getEmissionLine() + " Line.")

    def findClustersBySumConcentrations(self, indices, maxClusters, normalize):
        self.text = None
        try:
            indices.sort()
            listOfElementNames = self.getElementNames()
            listOfEmissionLines = self.getEmissionLines()
            string = listOfElementNames[indices[0]] + " " + listOfEmissionLines[indices[0]] + " Line"
            self.string = listOfElementNames[indices[0]] + "-" + listOfEmissionLines[indices[0]]
            if len(indices) == 2:
                string = string + " and " + listOfElementNames[indices[1]] + " " + listOfEmissionLines[
                    indices[1]] + " Line"
                self.string = self.string + "_" + listOfElementNames[indices[1]] + "-" + listOfEmissionLines[indices[1]]
            elif len(indices) > 2:
                for i in range(1, len(indices) - 1):
                    string = string + ", " + listOfElementNames[indices[i]] + " " + listOfEmissionLines[
                        indices[i]] + " Line"
                    self.string = self.string + "_" + listOfElementNames[indices[i]] + "-" + listOfEmissionLines[
                        indices[i]]
                string = string + ", and " + listOfElementNames[indices[-1]] + " " + listOfEmissionLines[
                    indices[-1]] + " Line"
                self.string = self.string + "_" + listOfElementNames[indices[-1]] + "-" + listOfEmissionLines[
                    indices[-1]]
            import matplotlib.pyplot as plt
            from itertools import chain
            import numpy as np
            if normalize == False:
                concentrations = self.elements[indices[0]].getConcentrations()
                if len(indices) > 1:
                    for i in range(1, len(indices)):
                        new_concentrations = self.elements[indices[i]].getConcentrations()
                        concentrations = [[sum(x) for x in zip(concentrations[n], new_concentrations[n])] for n in
                                          range(len(concentrations))]
                    string3 = "Sum of Concentrations of Selected Elements"
                else:
                    string3 = "Concentration of Selected Element"
            else:
                self.string = self.string + "_normalized"
                concentrations = self.elements[indices[0]].getConcentrations()
                from sklearn import preprocessing
                concentrations = preprocessing.normalize(concentrations, norm='max')
                if len(indices) > 1:
                    for i in range(1, len(indices)):
                        new_concentrations = preprocessing.normalize(self.elements[indices[i]].getConcentrations(),
                                                                     norm='max')
                        concentrations = [[sum(x) for x in zip(concentrations[n], new_concentrations[n])] for n in
                                          range(len(concentrations))]
                    string3 = "Normalized Sum of Concentrations of Selected Elements"
                else:
                    string3 = "Normalized Concentration of Selected Element"
            self.string = self.string + "_maxNClusters" + str(maxClusters)
            concentrations = list(chain.from_iterable(concentrations))
            data = np.array(list(zip(concentrations, concentrations)))
            sse = self.getSSE(data, None, maxClusters)
            from kneed import KneeLocator
            kl = KneeLocator(range(1, len(sse) + 1), sse, curve="convex", direction="decreasing")
            K = kl.elbow
            plt.plot(range(1, len(sse) + 1), sse)
            plt.xticks(range(1, len(sse) + 1))
            plt.xlim(1, len(sse))
            plt.xlabel("Number of Clusters")
            plt.ylabel("SSE")
            plt.title("Elbow Method With " + string + ": k = " + str(K))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.getPath() + "/SumConcentrations_ElbowMethod_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            silhouetteCoefs = self.getSilhouetteCoefs(data, None, maxClusters)
            newK = silhouetteCoefs.index(max(silhouetteCoefs)) + 2
            plt.plot(range(2, len(silhouetteCoefs) + 2), silhouetteCoefs)
            plt.xticks(range(2, len(silhouetteCoefs) + 2))
            plt.xlim(2, len(silhouetteCoefs) + 1)
            plt.xlabel("Number of Clusters")
            plt.ylabel("Silhouette Coefficient")
            plt.title("Silhouette Coefficients Resulting From " + string + ": k = " + str(newK))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.getPath() + "/SumConcentrations_SilhouetteCoefs_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            if K == None or K < newK:
                K = newK
            y_kmeans, centers = self.getClusteringData(data, None, K)
            import pandas as pd
            df1 = pd.DataFrame({'sumConcentrations': concentrations, 'cluster': y_kmeans})
            df1['cluster'] = df1['cluster'].astype(str)
            df2 = pd.DataFrame({'sumConcentrations1': centers[:, 0], 'sumConcentrations2': centers[:, 1]})
            import plotnine as p9
            myPlot = p9.ggplot() + \
                     p9.geom_point(data=df1,
                                   mapping=p9.aes(x='sumConcentrations', y='sumConcentrations', color='cluster'),
                                   alpha=0.4) + \
                     p9.scale_color_discrete(name="Cluster") + p9.theme_bw() + \
                     p9.geom_point(data=df2, mapping=p9.aes(x='sumConcentrations1', y='sumConcentrations2'),
                                   color='black', size=3, shape=',') + \
                     p9.xlab(string3) + p9.ylab(string3) + \
                     p9.ggtitle("K-Means Clustering With " + string)
            fileName = self.getPath() + "/SumConcentrations_Clusters_scatter_" + self.string + ".png"
            myPlot.save(fileName)
            plt.close()
            allLabels = np.array(y_kmeans).reshape((self.getNRow(), self.getNCol()))
            cmap = plt.get_cmap('RdBu', np.max(allLabels) - np.min(allLabels) + 1)
            mat = plt.matshow(allLabels, cmap=cmap, vmin=np.min(allLabels) - .5,
                              vmax=np.max(allLabels) + .5)  # set limits .5 outside true range
            cax = plt.colorbar(mat, ticks=np.arange(np.min(allLabels),
                                                    np.max(allLabels) + 1))  # tell the colorbar to tick at integers
            plt.xlabel("Column")
            plt.ylabel("Row")
            cax.set_label('Cluster')
            plt.title("K-Means Clustering With " + string)
            fileName = self.getPath() + "/SumConcentrations_Clusters_pcolor_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
        except:
            self.text = "The data of at least one of the selected elements is unavailable."
            print(self.text)
