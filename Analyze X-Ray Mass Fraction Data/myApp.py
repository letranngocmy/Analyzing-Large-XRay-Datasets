from myDesign import *
import functions as ftns
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

class MyApp(Ui_MainWindow):

    def __init__(self,window):
        self.setupUi(window)
        self.mainWindow = window
        import time
        self.now = time.time()
        self.tempDir = None
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        self.toolButton_1to21.setVisible(False)
        self.toolButton_1to22.setVisible(False)
        self.toolButton_quit1.clicked.connect(self.quit)
        self.toolButton_quit2.clicked.connect(self.quit)
        self.toolButton_quit3.clicked.connect(self.quit)
        self.radioButton_directory.toggled.connect(self.btnstate)
        self.radioButton_directory.setChecked(True)
        self.toolButton_browse1.clicked.connect(self.browse)
        self.toolButton_browse2.clicked.connect(self.browseDirectory)
        self.doubleSpinBox_thresholdData.setMinimum(0)
        self.doubleSpinBox_thresholdData.setMaximum(10000)
        self.doubleSpinBox_thresholdData.setValue(0)
        self.label_error.setText("")
        self.label_warning.setText("")
        self.saveTo = None
        self.elementBook = None
        self.toolButton_checkInputs.clicked.connect(self.checkInputs)
        self.toolButton_1to21.clicked.connect(lambda:self.setCurrentTab(1))
        self.toolButton_1to22.clicked.connect(lambda:self.setCurrentTab(2))
        self.toolButton_21to22.clicked.connect(lambda:self.setCurrentTab(2))
        self.toolButton_21to1.clicked.connect(lambda:self.setCurrentTab(0))
        self.toolButton_22to21.clicked.connect(lambda:self.setCurrentTab(1))
        self.toolButton_22to1.clicked.connect(lambda:self.setCurrentTab(0))
        self.label_image1.setText("")
        self.label_image2.setText("")
        self.label_errorPlot.setVisible(False)
        self.widget_message.setVisible(False)
        self.comboBox_clusteringMethods.activated.connect(self.changeState)
        self.comboBox_clusteringMethods.setCurrentText("Clustering by the Concentrations of an Element and the Pixel Locations")
        index = self.comboBox_images.findText("Clusters on Scatterplot")
        if index != -1:
            self.comboBox_images.removeItem(index)
        self.widget_clusters1.setVisible(True)
        self.widget_clusters2.setVisible(False)
        self.widget_clusters3.setVisible(False)
        self.doubleSpinBox_thresholdClusters1.setMinimum(0)
        self.doubleSpinBox_thresholdClusters1.setMaximum(100)
        self.doubleSpinBox_thresholdClusters1.setValue(0)
        self.spinBox_maxClusters.setMinimum(3)
        self.spinBox_maxClusters.setMaximum(100)
        self.spinBox_maxClusters.setValue(10)
        self.images = []
        self.currentImage1 = None
        self.currentImage2 = None
        self.label_save1.setText("")
        self.label_save2.setText("")
        self.toolButton_savePlot.setVisible(False)
        self.toolButton_saveClusters.setVisible(False)
        self.toolButton_savePlot.clicked.connect(lambda: self.saveImage(1))
        self.toolButton_saveClusters.clicked.connect(lambda: self.saveImage(2))
        self.toolButton_plotData.clicked.connect(self.plotData)
        self.toolButton_findClusters.clicked.connect(self.findClusters)
        self.comboBox_images.setCurrentText("Clusters on Actual Scan")
        self.comboBox_images.activated.connect(self.displayImage)

    def quit(self):
        if self.tempDir != None:
            import os
            import shutil
            for filename in os.listdir(self.tempDir):
                if os.path.getmtime(os.path.join(self.tempDir, filename)) > self.now:
                    if os.path.isfile(os.path.join(self.tempDir, filename)):
                        os.remove(os.path.join(self.tempDir, filename))
            if len(os.listdir(self.tempDir)) == 0:  # Check if the folder is empty
                shutil.rmtree(self.tempDir)
        self.mainWindow.close()

    def btnstate(self):
        if self.radioButton_directory.isChecked() == True:
            self.widget_thresholdData.setVisible(True)
            self.label6.setVisible(True)
        else:
            self.widget_thresholdData.setVisible(False)
            self.label6.setVisible(False)

    def browse(self):
        if self.radioButton_directory.isChecked() == True:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName = QFileDialog.getExistingDirectory(None, "Select a Directory",options=QFileDialog.ShowDirsOnly)
            self.lineEdit_path1.setText(fileName)
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None,"Select a Pickle File", "","Pickle Files (*.pckl)", options=options)
            self.lineEdit_path1.setText(fileName)

    def browseDirectory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(None, "Select a Directory", options=QFileDialog.ShowDirsOnly)
        self.lineEdit_path2.setText(fileName)

    def checkInputs(self):
        self.tempDir = None
        self.saveTo = None
        self.elementBook = None
        self.images = []
        self.currentImage1 = None
        self.currentImage2 = None
        self.label_image1.clear()
        self.label_image2.clear()
        self.label_save1.setText("")
        self.label_save2.setText("")
        self.toolButton_savePlot.setVisible(False)
        self.toolButton_saveClusters.setVisible(False)
        self.comboBox_clusteringMethods.setCurrentText("Clustering by the Concentrations of an Element and the Pixel Locations")
        index = self.comboBox_images.findText("Clusters on Scatterplot")
        if index != -1:
            self.comboBox_images.removeItem(index)
        self.spinBox_maxClusters.setValue(10)
        self.spinBox_maxClusters.setMinimum(3)
        self.widget_clusters1.setVisible(True)
        self.widget_clusters2.setVisible(False)
        self.widget_clusters3.setVisible(False)
        self.doubleSpinBox_thresholdClusters1.setValue(0)
        self.spinBox_maxClusters.setValue(10)
        self.checkBox_normalize.setChecked(False)
        self.label_errorPlot.setVisible(False)
        self.widget_message.setVisible(False)
        self.comboBox_images.setCurrentText("Clusters on Actual Scan")
        self.label_warning.setText("")
        self.comboBox_elementPlot.clear()
        self.comboBox_elementClusters1.clear()
        self.comboBox_element1Clusters2.clear()
        self.comboBox_element2Clusters2.clear()
        self.checkableComboBox.clear()
        if self.radioButton_directory.isChecked() == True:
            directory = self.lineEdit_path1.text()
            if len(directory) != 0:
                if directory[0] != "/":
                    directory = "/" + directory
                while directory[-1] == "/":
                    directory = directory[:-1]
                import os
                if os.path.isdir(directory) == False:
                    self.label_error.setText("The path to the source directory is invalid.")
                else:
                    arr = ftns.getTxtFileNames(directory)
                    if len(arr) == 0:
                        self.label_error.setText("There is no .txt file in the source directory.")
                    else:
                        self.saveTo = self.lineEdit_path2.text()
                        if len(self.saveTo) != 0:
                            if self.saveTo[0] != "/":
                                self.saveTo = "/" + self.saveTo
                            while self.saveTo[-1] == "/":
                                self.saveTo = self.saveTo[:-1]
                            temp = self.saveTo.replace(" ", "")
                            strings = temp.split("/")
                            if len(strings) == 0:
                                self.saveTo = None
                        else:
                            self.saveTo = None
                        if self.saveTo != None:
                            import distutils.dir_util
                            distutils.dir_util.mkpath(self.saveTo)
                        else:
                            self.label_warning.setText(
                                "Images will not be saved because no valid folder has been selected for saving.")
                        self.tempDir = ftns.createFolder(directory)
                        from ElementBook import ElementBook
                        self.elementBook = ElementBook(self.tempDir)
                        threshold = self.doubleSpinBox_thresholdData.value()
                        bool = True
                        nRow = 0
                        nCol = 0
                        from Element import Element
                        for f in arr:
                            element = Element(f, directory)
                            if element.getElementName() != None:
                                if nRow == 0 and nCol == 0:
                                    nRow = element.getNRow()
                                    nCol = element.getNCol()
                                    self.elementBook.insertElement(element, threshold)
                                else:
                                    if nRow != element.getNRow() or nCol != element.getNCol():
                                        bool = False
                                        break
                                    else:
                                        self.elementBook.insertElement(element, threshold)
                            else:
                                bool = False
                                break
                        if bool == True:
                            self.label_error.setText("Data read successfully.")
                            fileName = self.tempDir + "/elementBook.pckl"
                            ftns.saveVar(self.elementBook, fileName)
                            if self.saveTo != None:
                                import shutil
                                shutil.copy(fileName, self.saveTo)
                            elementNames = self.elementBook.getElementNames()
                            emissionLines = self.elementBook.getEmissionLines()
                            elements = []
                            for i in range(0, len(elementNames)):
                                elements.append(elementNames[i] + " " + emissionLines[i] + " Line")
                            if len(elements) != 0:
                                self.comboBox_elementPlot.addItems(elements)
                                self.comboBox_elementClusters1.addItems(elements)
                                self.comboBox_element1Clusters2.addItems(elements)
                                self.comboBox_element2Clusters2.addItems(elements)
                                self.comboBox_elementPlot.setCurrentText(elements[0])
                                self.comboBox_elementClusters1.setCurrentText(elements[0])
                                self.comboBox_element1Clusters2.setCurrentText(elements[0])
                                self.comboBox_element2Clusters2.setCurrentText(elements[0])
                                for i in range(0, len(elements)):
                                    self.checkableComboBox.addItem(elements[i])
                                    self.checkableComboBox.setItemChecked(i, True)
                            self.toolButton_1to21.setVisible(True)
                            self.toolButton_1to22.setVisible(True)
                        else:
                            self.label_error.setText("One or more .txt files have the name or data not in the correct format.")
                            self.label_warning.setText("")
            else:
                self.label_error.setText("The source directory has not been provided.")
        else:
            path = self.lineEdit_path1.text()
            if len(path) != 0:
                if path[0] != "/":
                    path = "/" + path
                import os
                if os.path.isfile(path) == False or path[-5:] != ".pckl":
                    self.label_error.setText("The path to the .pckl file is invalid.")
                else:
                    try:
                        elementBook = ftns.getVar(path)
                        from ElementBook import ElementBook
                        import os
                        temp = ElementBook(os.getcwd())
                        if elementBook is not temp:
                            self.label_error.setText("This .pckl file does not store a variable of the desired type.")
                        else:
                            self.elementBook = elementBook
                            self.label_error.setText("Data read successfully.")
                            self.saveTo = self.lineEdit_path2.text()
                            if len(self.saveTo) != 0:
                                if self.saveTo[0] != "/":
                                    self.saveTo = "/" + self.saveTo
                                while self.saveTo[-1] == "/":
                                    self.saveTo = self.saveTo[:-1]
                                temp = self.saveTo.replace(" ", "")
                                strings = temp.split("/")
                                if len(strings) == 0:
                                    self.saveTo = None
                            else:
                                self.saveTo = None
                            if self.saveTo != None:
                                import distutils.dir_util
                                distutils.dir_util.mkpath(self.saveTo)
                            else:
                                self.label_warning.setText(
                                    "Images will not be saved because no valid folder has been selected for saving.")
                            self.tempDir = self.elementBook.getPath()
                            elementNames = self.elementBook.getElementNames()
                            emissionLines = self.elementBook.getEmissionLines()
                            elements = []
                            for i in range(0, len(elementNames)):
                                elements.append(elementNames[i] + " " + emissionLines[i] + " Line")
                            if len(elements) != 0:
                                self.comboBox_elementPlot.addItems(elements)
                                self.comboBox_elementClusters1.addItems(elements)
                                self.comboBox_element1Clusters2.addItems(elements)
                                self.comboBox_element2Clusters2.addItems(elements)
                                self.comboBox_elementPlot.setCurrentText(elements[0])
                                self.comboBox_elementClusters1.setCurrentText(elements[0])
                                self.comboBox_element1Clusters2.setCurrentText(elements[0])
                                self.comboBox_element2Clusters2.setCurrentText(elements[0])
                                for i in range(0, len(elements)):
                                    self.checkableComboBox.addItem(elements[i])
                                    self.checkableComboBox.setItemChecked(i, True)
                            self.toolButton_1to21.setVisible(True)
                            self.toolButton_1to22.setVisible(True)
                    except ImportError:
                        self.label_error.setText("This .pckl file contains more than one variable or does not store a variable of the desired type.")
            else:
                self.label_error.setText("The .pckl file has not been provided.")

    def setCurrentTab(self,i):
        self.tabWidget.setCurrentIndex(i)
        if i == 0:
            self.tabWidget.setTabEnabled(0, True)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, False)
        elif i == 1:
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, False)
        else:
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, True)

    def changeState(self):
        text = self.comboBox_clusteringMethods.currentText()
        if text == "Clustering by the Concentrations of an Element and the Pixel Locations":
            self.widget_clusters1.setVisible(True)
            index = self.comboBox_images.findText("Clusters on Scatterplot")
            if index != -1:
                self.comboBox_images.removeItem(index)
            if self.spinBox_maxClusters.value() == 2:
                self.spinBox_maxClusters.setValue(3)
            self.spinBox_maxClusters.setMinimum(3)
        else:
            self.widget_clusters1.setVisible(False)
            index = self.comboBox_images.findText("Clusters on Scatterplot")
            if index == -1:
                self.comboBox_images.addItem("Clusters on Scatterplot")
            self.spinBox_maxClusters.setMinimum(2)
        if text == "Clustering With a Pair of Elements by Their Concentrations":
            self.widget_clusters2.setVisible(True)
        else:
            self.widget_clusters2.setVisible(False)
        if text == "Clustering by the Sum of Concentrations of Elements in a Set":
            self.widget_clusters3.setVisible(True)
        else:
            self.widget_clusters3.setVisible(False)

    def saveImage(self,i):
        if self.saveTo != None:
            if i == 1:
                if self.currentImage1 != None:
                    import shutil
                    shutil.copy(self.currentImage1, self.saveTo)
                    self.label_save1.setText("Image Saved Succesfully.")
                else:
                    self.label_save1.setText("")
            else:
                if self.currentImage2 != None:
                    import shutil
                    shutil.copy(self.currentImage2, self.saveTo)
                    self.label_save2.setText("Image Saved Succesfully.")
                else:
                    self.label_save2.setText("")

    def plotData(self):
        self.label_errorPlot.setVisible(False)
        self.toolButton_savePlot.setVisible(False)
        self.label_save1.setText("")
        self.label_image1.clear()
        substrings = self.comboBox_elementPlot.currentText().split(" ")
        elementName = substrings[0]
        emissionLine = substrings[1]
        self.elementBook.plotConcentrationsByElement(elementName, emissionLine)
        if self.elementBook.getText() != None:
            self.label_errorPlot.setText(self.elementBook.getText())
            self.label_errorPlot.setVisible(True)
        else:
            self.currentImage1 = self.tempDir + "/" + elementName + "-" + emissionLine + ".png"
            pixmap = QPixmap(self.currentImage1)  # show image
            self.label_image1.setPixmap(pixmap)
            self.label_image1.setMask(pixmap.mask())
            if self.saveTo != None:
                self.toolButton_savePlot.setVisible(True)

    def findClusters(self):
        self.toolButton_saveClusters.setVisible(False)
        self.label_save2.setText("")
        self.widget_message.setVisible(False)
        self.images = []
        self.currentImage2 = None
        maxClusters = self.spinBox_maxClusters.value()
        text = self.comboBox_clusteringMethods.currentText()
        if text == "Clustering by the Concentrations of an Element and the Pixel Locations":
            threshold = self.doubleSpinBox_thresholdClusters1.value()
            substrings = self.comboBox_elementClusters1.currentText().split(" ")
            object = self.elementBook.getObjectType(substrings[0],substrings[1])
            locations, values = object.prepareDataForClustering(threshold)
            self.elementBook.clusteringByPixelLocations_OneElement(object, locations, values, threshold, maxClusters)
            result = self.elementBook.getText()
            if result == None:
                string = self.elementBook.getString()
                self.images.append(self.tempDir + "/Locations_ElbowMethod_" + string + ".png")
                self.images.append(self.tempDir + "/Locations_SilhouetteCoefs_" + string + ".png")
                self.images.append(self.tempDir + "/Locations_Clusters_" + string + ".png")
            else:
                self.label_message.setText(result)
                self.widget_message.setVisible(True)
            self.displayImage()
        elif text == "Clustering With a Pair of Elements by Their Concentrations":
            element1 = self.comboBox_element1Clusters2.currentText()
            element2 = self.comboBox_element2Clusters2.currentText()
            substrings1 = element1.split(" ")
            object1 = self.elementBook.getObjectType(substrings1[0], substrings1[1])
            if element1 != element2:
                substrings2 = element2.split(" ")
                object2 = self.elementBook.getObjectType(substrings2[0], substrings2[1])
            else:
                object2 = object1
            self.elementBook.clusteringByConcentrations_OneElementPair(object1,object2,maxClusters)
            result = self.elementBook.getText()
            if result == None:
                string = self.elementBook.getString()
                self.images.append(self.tempDir + "/Concentrations_ElbowMethod_" + string + ".png")
                self.images.append(self.tempDir + "/Concentrations_SilhouetteCoefs_" + string + ".png")
                self.images.append(self.tempDir + "/Concentrations_Clusters_scatter_" + string + ".png")
                self.images.append(self.tempDir + "/Concentrations_Clusters_pcolor_" + string + ".png")
            else:
                self.label_message.setText(result)
                self.widget_message.setVisible(True)
            self.displayImage()
        else:
            elements = self.checkableComboBox.checkedItems()
            if len(elements) != 0:
                indices = []
                for e in elements:
                    substrings = e.split(" ")
                    indices.append(self.elementBook.getIndex(substrings[0], substrings[1]))
                self.elementBook.findClustersBySumConcentrations(indices, maxClusters,
                                                                 self.checkBox_normalize.isChecked())
                result = self.elementBook.getText()
                if result == None:
                    string = self.elementBook.getString()
                    self.images.append(self.tempDir + "/SumConcentrations_ElbowMethod_" + string + ".png")
                    self.images.append(self.tempDir + "/SumConcentrations_SilhouetteCoefs_" + string + ".png")
                    self.images.append(self.tempDir + "/SumConcentrations_Clusters_scatter_" + string + ".png")
                    self.images.append(self.tempDir + "/SumConcentrations_Clusters_pcolor_" + string + ".png")
                else:
                    self.label_message.setText(result)
                    self.widget_message.setVisible(True)
            else:
                self.label_message.setText("None of the elements has been selected.")
                self.widget_message.setVisible(True)
            self.displayImage()

    def displayImage(self):
        if len(self.images) != 0:
            text = self.comboBox_images.currentText()
            if text == "Results of Elbow Method":
                self.currentImage2 = self.images[0]
            elif text == "Silhouette Coefficients":
                self.currentImage2 = self.images[1]
            else:
                if len(self.images) == 3:
                    self.currentImage2 = self.images[2]
                else:
                    if text == "Clusters on Scatterplot":
                        self.currentImage2 = self.images[2]
                    else:
                        self.currentImage2 = self.images[3]
            if self.saveTo != None:
                self.toolButton_saveClusters.setVisible(True)
            pixmap = QPixmap(self.currentImage2) # show image
            self.label_image2.setPixmap(pixmap)
            self.label_image2.setMask(pixmap.mask())
        else:
            self.toolButton_saveClusters.setVisible(False)
            self.label_image2.clear()



# from CheckableComboBox import CheckableComboBox
# self.checkableComboBox = CheckableComboBox(self.widget_clusters3)
# sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
# sizePolicy.setHorizontalStretch(110)
# sizePolicy.setVerticalStretch(0)
# sizePolicy.setHeightForWidth(self.checkableComboBox.sizePolicy().hasHeightForWidth())
# self.checkableComboBox.setSizePolicy(sizePolicy)
# self.checkableComboBox.setMaximumSize(QtCore.QSize(110, 16777215))
# self.checkableComboBox.setObjectName("checkableComboBox")
# self.horizontalLayout_15.addWidget(self.checkableComboBox)
