from Element import *

class ElementBook:

    def __init__(self,scan):
        import pandas
        df = pandas.read_csv('X-Ray Data.csv')
        df[['Atomic_Number', 'Element']] = df.Element.str.split(expand=True)
        df = df[['Element', 'K_alpha1']]
        df = df.loc[df['K_alpha1'] != '—']
        df['K_alpha1'] = df['K_alpha1'].astype(float)
        df['Object_Type'] = None
        df['Number_Positive'] = None
        df['Sum_Areas'] = None
        self.originalDF = df
        self.scan = scan
        if scan != None:
            self.df = df[df.K_alpha1 < scan.getMaxEnergy() + 25]
            for i in range(0, len(self.df)):
                energy = self.df.at[i, 'K_alpha1']
                object = Element(self.df.at[i, 'Element'],
                                 self.scan.getTotalIntensitiesInEnergyRange(energy - 25, energy + 25))
                self.df.at[i, 'Object_Type'] = object
                Count, Sum = object.summarizeData()
                self.df.at[i, 'Number_Positive'] = Count
        self.text = None
        self.string = None
        self.count = 0

    def getText(self):
        return self.text

    def getString(self):
        return self.string

    def getElementNames(self):
        return self.df['Element'].tolist()

    def getElementIndex(self,element):
        listOfElements = self.df['Element'].tolist()
        if element in listOfElements:
            return listOfElements.index(element)
        else:
            print("The chosen dataset does not contain the data of " + element + ".")
            return -1

    def getObjectType(self,element):
        i = self.getElementIndex(element)
        if i != -1:
            return self.df.at[self.getElementIndex(element), 'Object_Type']
        else:
            return None

    def updateEnergyRange(self,minEnergy,maxEnergy):
        self.scan.updateEnergyRange(minEnergy,maxEnergy)
        self.df = self.originalDF[self.originalDF.K_alpha1 < self.scan.getMaxEnergy() + 25]
        for i in range(0, len(self.df)):
            energy = self.df.at[i, 'K_alpha1']
            object = Element(self.df.at[i, 'Element'], self.scan.getTotalIntensitiesInEnergyRange(energy - 25, energy + 25))
            self.df.at[i, 'Object_Type'] = object
            Count, Sum = object.summarizeData()
            self.df.at[i, 'Number_Positive'] = Count

    def getDF(self):
        return self.df

    def getScan(self):
        return self.scan

    def getEnergies(self):
        return self.scan.getEnergies()

    def plotTotalIntensitiesByIndex(self,i):
        self.text = None
        name = self.df.at[i, 'Element']
        if self.df.at[i, 'Number_Positive'] == 0:
            self.text = "The signal of " + name + " is not found."
            print(self.text)
        else:
            print("The signal of " + name + " is found.")
            object = self.df.at[i, 'Object_Type']
            total = object.getTotalIntensities()
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            p = ax.imshow(total)
            cb = plt.colorbar(p, shrink=0.5)
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            cb.set_label('Total Intensity')
            plt.title("Total Intensities of " + name)
            self.string = self.scan.getPath() + "/" + name + ".png"
            plt.savefig(self.string)
            plt.close(fig)
            self.count += 1

    def plotTotalIntensitiesByElement(self,element):
        index = self.getElementIndex(element)
        if index != -1:
            self.plotTotalIntensitiesByIndex(index)

    def plotTotalIntensities_AllElements(self):
        self.count = 0
        for i in range(0,len(self.df)):
            self.plotTotalIntensitiesByIndex(i)

    def getCount(self):
        return self.count

    def getTotalIntensities_Pixel(self,row,col):
        total = []
        for i in range(0,len(self.df)):
            total.append(self.df.at[i,'Object_Type'].getTotalIntensities()[row][col])
        return total

    def getSSE(self,data,values,maxNClusters): # Elbow method
        from sklearn.cluster import KMeans
        kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
        sse = []  # A list holds the SSE values for each k
        n = maxNClusters+1
        if n > len(data)+1:
            n = len(data)+1
        for k in range(1, n):
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            if values != None:
                kmeans.fit(data,sample_weight=values)
            else:
                kmeans.fit(data)
            sse.append(kmeans.inertia_)
        return sse

    def getSilhouetteCoefs(self,data,values,maxNClusters):
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300, "random_state": 42}
        silhouette_coefficients = []
        n = maxNClusters+1
        if n > len(data):
            n = len(data)
        for k in range(2, n):  # Start at 2 clusters for silhouette coefficient
            kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
            if values != None:
                kmeans.fit(data,sample_weight=values)
            else:
                kmeans.fit(data)
            silhouette_coefficients.append(silhouette_score(data, kmeans.labels_))
        return silhouette_coefficients

    def getClusteringData(self,data,values,k):
        from sklearn.cluster import KMeans
        kmeans = KMeans(init="random", n_clusters=k, n_init=10, max_iter=300)
        if values != None:
            kmeans.fit(data,sample_weight=values)
        else:
            kmeans.fit(data)
        y_kmeans = kmeans.predict(data)
        centers = kmeans.cluster_centers_  # Final locations of the centroid
        return y_kmeans,centers

    def clusteringByPixelLocations_OneElement(self, object, locations, values, threshold, maxNClusters):
        self.text = None
        name = object.getName()
        if len(locations) > 1:
            self.string = name + "_threshold" + str(threshold) + "_maxNClusters" + str(maxNClusters)
            import matplotlib.pyplot as plt
            sse = self.getSSE(locations, values, maxNClusters - 1)
            from kneed import KneeLocator
            kl = KneeLocator(range(1, len(sse) + 1), sse, curve="convex", direction="decreasing")
            K = kl.elbow
            plt.plot(range(1, len(sse) + 1), sse)
            plt.xticks(range(1, len(sse) + 1))
            plt.xlim(1, len(sse))
            plt.xlabel("Number of Clusters")
            plt.ylabel("SSE")
            plt.title("Results of Elbow Method From Positive Intensities of " + name + ": k = " + str(K))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-',alpha = 0.3)
            fileName = self.scan.getPath() + "/Locations_ElbowMethod_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            silhouetteCoefs = self.getSilhouetteCoefs(locations, values, maxNClusters - 1)
            newK = silhouetteCoefs.index(max(silhouetteCoefs)) + 2
            plt.plot(range(2, len(silhouetteCoefs) + 2), silhouetteCoefs)
            plt.xticks(range(2, len(silhouetteCoefs) + 2))
            plt.xlim(2, len(silhouetteCoefs) + 1)
            plt.xlabel("Number of Clusters")
            plt.ylabel("Silhouette Coefficient")
            plt.title("Silhouette Coefficients Resulting From Positive Intensities of " + name + ": k = " + str(newK))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-',alpha = 0.3)
            fileName = self.scan.getPath() + "/Locations_SilhouetteCoefs_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            if K == None or K < newK:
                K = newK
            y_kmeans, centers = self.getClusteringData(locations, values, K)
            allLabels = [[0 for j in range(self.scan.getNCol())] for i in range(self.scan.getNRow())]
            for n in range(0,len(locations)):
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
            plt.title("K-Means Clustering With " + name)
            fileName = self.scan.getPath() + "/Locations_Clusters_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            # import pandas as pd
            # df1 = pd.DataFrame({'column': locations[:, 0], 'row': locations[:, 1], 'cluster': y_kmeans, 'intensity': values})
            # df1['cluster'] = df1['cluster'].astype(str)
            # df2 = pd.DataFrame({'column': centers[:, 0], 'row': centers[:, 1]})
            # import plotnine as p9
            # myPlot = p9.ggplot() + \
            #          p9.geom_point(data=df1,mapping=p9.aes(x='column', y='row', color='cluster', size='intensity'),alpha=0.4) + \
            #          p9.scale_color_discrete(name="Cluster") + p9.scale_size_continuous(name="Normalized Intensity") + \
            #          p9.geom_point(data=df2,mapping=p9.aes(x='column',y='row'),color='black',size=3, shape=',') + \
            #          p9.scale_y_reverse(lim=[self.scan.getNRow() - 1, 0]) + p9.scale_x_continuous(limits=[0, self.scan.getNCol() - 1]) + \
            #          p9.xlab("Column") + p9.ylab("Row") + p9.theme_bw() + \
            #          p9.ggtitle("K-Means Clustering With " + name)
            # fileName = self.scan.getPath() + "/Locations_Clusters_" + self.string + ".png"
            # myPlot.save(fileName)
            # plt.close()
        elif len(locations) == 1:
            self.text = "After denoising, only one pixel (" + str(locations[0][1]) + ", " + str(locations[0][0]) + ") shows signal of " + name + "."
            print(self.text)
        else:
            self.text = "After denoising, no pixel shows signal of " + name + "."
            print(self.text)

    def findClustersByPixelLocations_AllElements(self,threshold, maxNClusters):
        self.count = 0
        for i in range(0, len(self.df)):
            if self.df.at[i, 'Number_Positive'] > 0:
                object = self.df.at[i, 'Object_Type']
                locations, values = object.prepareDataForClustering(threshold)
                self.clusteringByPixelLocations_OneElement(object, locations, values, threshold, maxNClusters)
                self.count += 1
            else:
                print("After denoising, no pixel shows signal of " + self.df.at[i, 'Element'] + ".")

    def clusteringByIntensities_OneElementPair(self, element1, element2, maxNClusters):
        self.text = None
        try:
            import matplotlib.pyplot as plt
            areas1 = element1.getTotalIntensities()
            areas2 = element2.getTotalIntensities()
            from itertools import chain
            areas1 = list(chain.from_iterable(areas1))
            areas2 = list(chain.from_iterable(areas2))
            import numpy as np
            data = np.array(list(zip(areas1, areas2)))
            name1 = element1.getName()
            name2 = element2.getName()
            string = name1 + " and " + name2
            self.string = name1 + "_" + name2 + "_maxNClusters" + str(maxNClusters)
            sse = self.getSSE(data, None, maxNClusters)
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
            fileName = self.scan.getPath() + "/Intensities_ElbowMethod_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            silhouetteCoefs = self.getSilhouetteCoefs(data, None, maxNClusters)
            newK = silhouetteCoefs.index(max(silhouetteCoefs)) + 2
            plt.plot(range(2, len(silhouetteCoefs) + 2), silhouetteCoefs)
            plt.xticks(range(2, len(silhouetteCoefs) + 2))
            plt.xlim(2, len(silhouetteCoefs) + 1)
            plt.xlabel("Number of Clusters")
            plt.ylabel("Silhouette Coefficient")
            plt.title("Silhouette Coefficients Resulting From " + string + ": k = " + str(newK))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.scan.getPath() + "/Intensities_SilhouetteCoefs_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            if K == None or K < newK:
                K = newK
            y_kmeans, centers = self.getClusteringData(data, None, K)
            import pandas as pd
            df1 = pd.DataFrame({'element1': areas1, 'element2': areas2, 'cluster': y_kmeans})
            df1['cluster'] = df1['cluster'].astype(str)
            df2 = pd.DataFrame({'element1': centers[:, 0], 'element2': centers[:, 1]})
            import plotnine as p9
            myPlot = p9.ggplot() + \
                     p9.geom_point(data=df1, mapping=p9.aes(x='element1', y='element2', color='cluster'), alpha=0.4) + \
                     p9.scale_color_discrete(name="Cluster") + p9.theme_bw() + \
                     p9.geom_point(data=df2, mapping=p9.aes(x='element1', y='element2'), color='black', size=3,
                                   shape=',') + \
                     p9.xlab("Intensity of " + name1) + p9.ylab("Intensity of " + name2) + \
                     p9.ggtitle("K-Means Clustering With " + string)
            fileName = self.scan.getPath() + "/Intensities_Clusters_scatter_" + self.string + ".png"
            myPlot.save(fileName)
            plt.close()
            allLabels = np.array(y_kmeans).reshape((self.scan.getNRow(), self.scan.getNCol()))
            cmap = plt.get_cmap('RdBu', np.max(allLabels) - np.min(allLabels) + 1)
            mat = plt.matshow(allLabels, cmap=cmap, vmin=np.min(allLabels) - .5, vmax=np.max(allLabels) + .5)
            cax = plt.colorbar(mat, ticks=np.arange(np.min(allLabels), np.max(allLabels) + 1))
            plt.xlabel("Column")
            plt.ylabel("Row")
            cax.set_label('Cluster')
            plt.title("K-Means Clustering With " + string)
            fileName = self.scan.getPath() + "/Intensities_Clusters_pcolor_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
        except:
            self.text = "The data of at least one of the selected elements is unavailable."
            print(self.text)

    def findClustersByIntensities_AllElementPairs(self,maxNClusters):
        self.count = 0
        temp = self.df[self.df.Number_Positive == 0]
        for i in range(0,len(temp)):
            print("After denoising, no pixel shows signal of " + temp.at[i, 'Element'] + ".")
        temp = self.df[self.df.Number_Positive > 0]
        for i in range(0, len(temp)-1):
            j = i + 1
            while j < len(self.df):
                self.clusteringByIntensities(self.df.at[i, 'Object_Type'], self.df.at[j, 'Object_Type'],maxNClusters)
                j += 1
                self.count += 1

    def findClustersBySumIntensities(self, indices, maxNClusters, normalized):
        self.text = None
        try:
            indices.sort()
            listOfElements = self.df['Element'].tolist()
            string = listOfElements[indices[0]]
            self.string = string
            if len(indices) == 2:
                string = string + " and " + listOfElements[indices[1]]
                self.string = self.string + "_" + listOfElements[indices[1]]
            elif len(indices) > 2:
                for i in range(1, len(indices) - 1):
                    string = string + ", " + listOfElements[indices[i]]
                    self.string = self.string + "_" + listOfElements[indices[i]]
                string = string + ", and " + listOfElements[indices[-1]]
                self.string = self.string + "_" + listOfElements[indices[-1]]
            import matplotlib.pyplot as plt
            from itertools import chain
            import numpy as np
            if normalized == False:
                areas = self.df.at[indices[0], 'Object_Type'].getTotalIntensities()
                if len(indices) > 1:
                    for i in range(1, len(indices)):
                        new_areas = self.df.at[indices[i], 'Object_Type'].getTotalIntensities()
                        areas = [[sum(x) for x in zip(areas[n], new_areas[n])] for n in range(len(areas))]
                    string3 = "Sum of Intensities of Selected Elements"
                else:
                    string3 = "Intensity of Selected Element"
            else:
                self.string = self.string + "_normalized"
                areas = self.df.at[indices[0], 'Object_Type'].getTotalIntensities()
                from sklearn import preprocessing
                areas = preprocessing.normalize(areas, norm='max')
                if len(indices) > 1:
                    for i in range(1, len(indices)):
                        new_areas = preprocessing.normalize(self.df.at[indices[i], 'Object_Type'].getTotalIntensities(),
                                                            norm='max')
                        areas = np.add(areas, new_areas)
                    string3 = "Normalized Sum of Intensities of Selected Elements"
                else:
                    string3 = "Normalized Intensity of Selected Element"
                areas.tolist()
            self.string = self.string + "_maxNClusters" + str(maxNClusters)
            areas = list(chain.from_iterable(areas))
            data = np.array(list(zip(areas, areas)))
            sse = self.getSSE(data, None, maxNClusters)
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
            fileName = self.scan.getPath() + "/SumIntensities_ElbowMethod_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            silhouetteCoefs = self.getSilhouetteCoefs(data, None, maxNClusters)
            newK = silhouetteCoefs.index(max(silhouetteCoefs)) + 2
            plt.plot(range(2, len(silhouetteCoefs) + 2), silhouetteCoefs)
            plt.xticks(range(2, len(silhouetteCoefs) + 2))
            plt.xlim(2, len(silhouetteCoefs) + 1)
            plt.xlabel("Number of Clusters")
            plt.ylabel("Silhouette Coefficient")
            plt.title("Silhouette Coefficients Resulting From " + string + ": k = " + str(newK))
            plt.grid(b=True, which='major', axis='both', color='gray', linestyle='-', alpha=0.3)
            fileName = self.scan.getPath() + "/SumIntensities_SilhouetteCoefs_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
            if K == None or K < newK:
                K = newK
            y_kmeans, centers = self.getClusteringData(data, None, K)
            import pandas as pd
            df1 = pd.DataFrame({'sumAreas': areas, 'cluster': y_kmeans})
            df1['cluster'] = df1['cluster'].astype(str)
            df2 = pd.DataFrame({'sumAreas1': centers[:, 0], 'sumAreas2': centers[:, 1]})
            import plotnine as p9
            myPlot = p9.ggplot() + \
                     p9.geom_point(data=df1, mapping=p9.aes(x='sumAreas', y='sumAreas', color='cluster'), alpha=0.4) + \
                     p9.scale_color_discrete(name="Cluster") + p9.theme_bw() + \
                     p9.geom_point(data=df2, mapping=p9.aes(x='sumAreas1', y='sumAreas2'), color='black', size=3,
                                   shape=',') + \
                     p9.xlab(string3) + p9.ylab(string3) + \
                     p9.ggtitle("K-Means Clustering With " + string)
            fileName = self.scan.getPath() + "/SumIntensities_Clusters_scatter_" + self.string + ".png"
            myPlot.save(fileName)
            plt.close()
            allLabels = np.array(y_kmeans).reshape((self.scan.getNRow(), self.scan.getNCol()))
            cmap = plt.get_cmap('RdBu', np.max(allLabels) - np.min(allLabels) + 1)
            mat = plt.matshow(allLabels, cmap=cmap, vmin=np.min(allLabels) - .5,
                              vmax=np.max(allLabels) + .5)  # set limits .5 outside true range
            cax = plt.colorbar(mat, ticks=np.arange(np.min(allLabels),
                                                    np.max(allLabels) + 1))  # tell the colorbar to tick at integers
            plt.xlabel("Column")
            plt.ylabel("Row")
            cax.set_label('Cluster')
            plt.title("K-Means Clustering With " + string)
            fileName = self.scan.getPath() + "/SumIntensities_Clusters_pcolor_" + self.string + ".png"
            plt.savefig(fileName)
            plt.close()
        except:
            self.text = "The data of at least one of the selected elements is unavailable."
            print(self.text)
