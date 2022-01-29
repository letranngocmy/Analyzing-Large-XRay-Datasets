from myDesign import *
import functions as ftns
from Pixel import Pixel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap

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
        self.doubleSpinBox_thresholdData.setValue(5)
        self.checkBox_unknown.clicked.connect(self.doCheck1)
        self.checkBox_unknown.setChecked(False)
        self.checkBox_updateEnergy.clicked.connect(self.doCheck2)
        self.checkBox_updateEnergy.setChecked(False)
        self.widget_energyInputs2.setVisible(False)
        self.label_error.setText("")
        self.label_warning1.setText("")
        self.label_warning2.setText("")
        self.saveTo = None
        self.elementBook = None
        self.toolButton_checkInputs.clicked.connect(self.checkInputs)
        self.toolButton_1to21.clicked.connect(lambda: self.setCurrentTab(1))
        self.toolButton_1to22.clicked.connect(lambda: self.setCurrentTab(2))
        self.toolButton_21to22.clicked.connect(lambda: self.setCurrentTab(2))
        self.toolButton_21to1.clicked.connect(lambda: self.setCurrentTab(0))
        self.toolButton_22to21.clicked.connect(lambda: self.setCurrentTab(1))
        self.toolButton_22to1.clicked.connect(lambda: self.setCurrentTab(0))
        self.label_image1.setText("")
        self.label_image2.setText("")
        self.widget_message1.setVisible(False)
        self.widget_message2.setVisible(False)
        self.comboBox_plottingMethods.activated.connect(self.changeState1)
        self.comboBox_plottingMethods.setCurrentText("Plot the Total Intensities in the Energy Range of an Element")
        self.widget_plot1.setVisible(True)
        self.widget_plot2.setVisible(False)
        self.widget_plot3.setVisible(False)
        self.comboBox_clusteringMethods.activated.connect(self.changeState2)
        self.comboBox_clusteringMethods.setCurrentText("Clustering by the Intensities of an Element and the Pixel Locations")
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
            self.widget_energy.setVisible(True)
            self.widget_thresholdData.setVisible(True)
            self.widget_updateEnergy.setVisible(False)
            self.label11.setVisible(True)
            self.label12.setVisible(True)
            self.label14.setVisible(True)
        else:
            self.widget_energy.setVisible(False)
            self.widget_thresholdData.setVisible(False)
            self.widget_updateEnergy.setVisible(True)
            self.label11.setVisible(False)
            self.label12.setVisible(False)
            self.label14.setVisible(False)

    def browse(self):
        if self.radioButton_directory.isChecked() == True:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName = QFileDialog.getExistingDirectory(None, "Select a Directory", options=QFileDialog.ShowDirsOnly)
            self.lineEdit_path1.setText(fileName)
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None, "Select a Pickle File", "", "Pickle Files (*.pckl)",options=options)
            self.lineEdit_path1.setText(fileName)

    def browseDirectory(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getExistingDirectory(None, "Select a Directory", options=QFileDialog.ShowDirsOnly)
        self.lineEdit_path2.setText(fileName)

    def doCheck1(self):
        if self.checkBox_unknown.isChecked():
            self.widget_energyInputs1.setVisible(False)
        else:
            self.widget_energyInputs1.setVisible(True)

    def doCheck2(self):
        if self.checkBox_updateEnergy.isChecked():
            self.widget_energyInputs2.setVisible(True)
        else:
            self.widget_energyInputs2.setVisible(False)

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
        self.comboBox_plottingMethods.setCurrentText("Plot the Total Intensities in the Energy Range of an Element")
        self.comboBox_clusteringMethods.setCurrentText("Clustering by the Intensities of an Element and the Pixel Locations")
        index = self.comboBox_images.findText("Clusters on Scatterplot")
        if index != -1:
            self.comboBox_images.removeItem(index)
        self.spinBox_maxClusters.setValue(10)
        self.spinBox_maxClusters.setMinimum(3)
        self.widget_plot1.setVisible(True)
        self.widget_plot2.setVisible(False)
        self.widget_plot3.setVisible(False)
        self.widget_clusters1.setVisible(True)
        self.widget_clusters2.setVisible(False)
        self.widget_clusters3.setVisible(False)
        self.doubleSpinBox_thresholdClusters1.setValue(0)
        self.checkBox_normalize.setChecked(False)
        self.widget_message1.setVisible(False)
        self.widget_message2.setVisible(False)
        self.comboBox_images.setCurrentText("Clusters on Actual Scan")
        self.lineEdit_energy.setText("")
        self.lineEdit_startEnergy.setText("")
        self.lineEdit_endEnergy.setText("")
        self.label_warning1.setText("")
        self.label_warning2.setText("")
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
                    arr = ftns.getEdfFileNames(directory)
                    if len(arr) == 0:
                        self.label_error.setText("There is no .edf file in the source directory.")
                    else:
                        bool = False
                        if self.checkBox_unknown.isChecked() == False:
                            minEnergy = str(self.lineEdit_minEnergy1.text())
                            maxEnergy = str(self.lineEdit_maxEnergy1.text())
                            if len(minEnergy) != 0 and len(maxEnergy) != 0:
                                minEnergy.replace(" ","")
                                maxEnergy.replace(" ", "")
                                try:
                                    minEnergy = float(minEnergy)
                                    maxEnergy = float(maxEnergy)
                                    if minEnergy >= 0 and maxEnergy >= 0:
                                        if minEnergy < maxEnergy:
                                            bool = True
                                        else:
                                            self.label_error.setText("The maximum energy must be higher than the minimum energy.")
                                    else:
                                        self.label_error.setText("The energies must be non-negative.")
                                except:
                                    self.label_error.setText("Invalid inputs for the energy range.")
                            else:
                                self.label_error.setText("The energy range has not been provided.")
                        else:
                            bool = True
                        if bool == True:
                            cols = ftns.getColumns(arr)
                            missingCols, missingFiles = ftns.findMissing(cols, arr)
                            if len(missingCols) == 1:
                                self.label_warning1.setText("Found one missing file: " + missingFiles[0])
                            elif len(missingCols) > 1:
                                if len(missingCols) == 2:
                                    string = missingFiles[0] + " and " + missingFiles[1]
                                else:
                                    string = missingFiles[0]
                                    for i in range(1, len(missingCols) - 1):
                                        string = string + ", " + missingFiles[i]
                                    string = string + ", and " + missingFiles[-1]
                                self.label_warning1.setText(
                                    "Found " + str(len(missingCols)) + " missing files: " + string)
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
                                if self.label_warning1.text() == "":
                                    self.label_warning1.setText(
                                        "Images will not be saved because no valid folder has been selected for saving.")
                                else:
                                    self.label_warning2.setText(
                                        "Images will not be saved because no valid folder has been selected for saving.")
                            self.tempDir = ftns.createFolder(directory)
                            from PyMca5.PyMcaIO.EdfFile import EdfFile
                            edf = EdfFile(directory + "/" + arr[0], "r")
                            nRow = len(edf.GetData(0))
                            nCol = len(cols)
                            length = len(edf.GetData(0)[0])
                            if nRow != 0 and length != 0:
                                from Scan import Scan
                                if self.checkBox_unknown.isChecked() == False:
                                    scan = Scan(self.tempDir, nRow, nCol, minEnergy, maxEnergy)
                                else:
                                    scan = Scan(self.tempDir, nRow, nCol, -1, -1)
                                l = sorted(zip(arr,cols), key=lambda x: x[1])
                                arr = [f for f, c in l]
                                bool = False
                                threshold = self.doubleSpinBox_thresholdData.value()
                                for j in range(0, nCol):
                                    file = directory + "/" + arr[j]
                                    edf = EdfFile(file, "r")
                                    if len(edf.GetData(0)) != nRow:
                                        bool = True
                                        break
                                    else:
                                        try:
                                            for i in range(0, nRow):
                                                if len(edf.GetData(0)[i]) == length and all(
                                                        (float(item) >= 0) for item in
                                                        edf.GetData(0)[i]):
                                                    pixel = Pixel(edf.GetData(0)[i])
                                                    scan.insertPixel(pixel, i, j, threshold)
                                                else:
                                                    bool = True
                                                    break
                                        except:
                                            bool = True
                                        if bool == True:
                                            break
                                if bool == False:
                                    self.label_error.setText("Data read successfully.")
                                    from ElementBook import ElementBook
                                    self.elementBook = ElementBook(scan)
                                    fileName = self.tempDir + "/elementBook.pckl"
                                    ftns.saveVar(self.elementBook, fileName)
                                    if self.saveTo != None:
                                        import shutil
                                        shutil.copy(fileName, self.saveTo)
                                    elements = self.elementBook.getElementNames()
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
                                    self.label_error.setText("The data in one or more .edf files are not in the correct format.")
                                    self.label_warning1.setText("")
                                    self.label_warning2.setText("")
                            else:
                                self.label_error.setText("The data in one or more .edf files are not in the correct format.")
                                self.label_warning1.setText("")
                                self.label_warning2.setText("")
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
                        temp = ElementBook(None)
                        if elementBook is not temp:
                            self.label_error.setText("This .pckl file does not store a variable of the desired type.")
                        else:
                            bool = False
                            if self.checkBox_updateEnergy.isChecked() == True:
                                minEnergy = str(self.lineEdit_minEnergy2.text())
                                maxEnergy = str(self.lineEdit_maxEnergy2.text())
                                if len(minEnergy) != 0 and len(maxEnergy) != 0:
                                    minEnergy.replace(" ", "")
                                    maxEnergy.replace(" ", "")
                                    try:
                                        minEnergy = float(minEnergy)
                                        maxEnergy = float(maxEnergy)
                                        if minEnergy >= 0 and maxEnergy >= 0:
                                            if minEnergy < maxEnergy:
                                                elementBook.updateEnergyRange(minEnergy,maxEnergy)
                                                bool = True
                                            else:
                                                self.label_error.setText("The maximum energy must be higher than the minimum energy.")
                                        else:
                                            self.label_error.setText("The energies must be non-negative.")
                                    except:
                                        self.label_error.setText("Invalid inputs for the energy range.")
                                else:
                                    self.label_error.setText("The energy range has not been provided.")
                            else:
                                bool = True
                            if bool == True:
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
                                    self.label_warning1.setText(
                                        "Images will not be saved because no valid folder has been selected for saving.")
                                self.tempDir = self.elementBook.getScan().getPath()
                                fileName = self.tempDir + "/elementBook.pckl"
                                ftns.saveVar(self.elementBook, fileName)
                                if self.saveTo != None:
                                    import shutil
                                    shutil.copy(fileName, self.saveTo)
                                elements = self.elementBook.getElementNames()
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

    def changeState1(self):
        text = self.comboBox_plottingMethods.currentText()
        if text == "Plot the Total Intensities in the Energy Range of an Element":
            self.widget_plot1.setVisible(True)
        else:
            self.widget_plot1.setVisible(False)
        if text == "Plot the Intensities at an Energy":
            self.widget_plot2.setVisible(True)
        else:
            self.widget_plot2.setVisible(False)
        if text == "Plot the Total Intensities in a Customized Energy Range":
            self.widget_plot3.setVisible(True)
        else:
            self.widget_plot3.setVisible(False)

    def changeState2(self):
        text = self.comboBox_clusteringMethods.currentText()
        if text == "Clustering by the Intensities of an Element and the Pixel Locations":
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
        if text == "Clustering With a Pair of Elements by Their Intensities":
            self.widget_clusters2.setVisible(True)
        else:
            self.widget_clusters2.setVisible(False)
        if text == "Clustering by the Sum of Intensities of Elements in a Set":
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
        self.toolButton_savePlot.setVisible(False)
        self.label_save1.setText("")
        self.widget_message1.setVisible(False)
        self.currentImage1 = None
        self.label_image1.clear()
        text = self.comboBox_plottingMethods.currentText()
        if text == "Plot the Total Intensities in the Energy Range of an Element":
            element = self.comboBox_elementPlot.currentText()
            self.elementBook.plotTotalIntensitiesByElement(element)
            if self.elementBook.getText() == None:
                self.currentImage1 = self.tempDir + "/" + element + ".png"
                pixmap = QPixmap(self.currentImage1)  # show image
                self.label_image1.setPixmap(pixmap)
                self.label_image1.setMask(pixmap.mask())
                if self.saveTo != None:
                    self.toolButton_savePlot.setVisible(True)
            else:
                self.label_message1.setText(self.elementBook.getText())
                self.widget_message1.setVisible(True)
        elif text == "Plot the Intensities at an Energy":
            energy = str(self.lineEdit_energy.text())
            if len(energy) != 0:
                energy.replace(" ", "")
                try:
                    energy = float(energy)
                    if energy <= self.elementBook.getScan().getMaxEnergy() and energy >= self.elementBook.getScan().getMinEnergy():
                        self.elementBook.getScan().plotIntensitiesAtEnergy(energy)
                        self.currentImage1 = self.tempDir + "/" + str(energy)+"eV" + ".png"
                        pixmap = QPixmap(self.currentImage1)  # show image
                        self.label_image1.setPixmap(pixmap)
                        self.label_image1.setMask(pixmap.mask())
                        if self.saveTo != None:
                            self.toolButton_savePlot.setVisible(True)
                    else:
                        self.label_message1.setText("The energy entered is out of range.")
                        self.widget_message1.setVisible(True)
                except:
                    self.label_message1.setText("Invalid input for the energy.")
                    self.widget_message1.setVisible(True)
            else:
                self.label_message1.setText("The energy has not been provided.")
                self.widget_message1.setVisible(True)
        else:
            startEnergy = str(self.lineEdit_startEnergy.text())
            endEnergy = str(self.lineEdit_endEnergy.text())
            if len(startEnergy) != 0 and len(endEnergy) != 0:
                startEnergy.replace(" ", "")
                endEnergy.replace(" ", "")
                try:
                    startEnergy = float(startEnergy)
                    endEnergy = float(endEnergy)
                    minEnergy = self.elementBook.getScan().getMinEnergy()
                    maxEnergy = self.elementBook.getScan().getMaxEnergy()
                    if startEnergy >= minEnergy and endEnergy >= minEnergy and startEnergy <= maxEnergy and endEnergy <= maxEnergy:
                        if startEnergy < endEnergy:
                            self.elementBook.getScan().plotTotalIntensitiesInEnergyRange(startEnergy, endEnergy)
                            self.currentImage1 = self.tempDir + "/" + str(startEnergy) + "eV_" + str(
                                endEnergy) + "eV" + ".png"
                            pixmap = QPixmap(self.currentImage1)  # show image
                            self.label_image1.setPixmap(pixmap)
                            self.label_image1.setMask(pixmap.mask())
                            if self.saveTo != None:
                                self.toolButton_savePlot.setVisible(True)
                        else:
                            self.label_message1.setText("The end energy must be higher than the start energy.")
                            self.widget_message1.setVisible(True)
                    else:
                        self.label_message1.setText("The energy range must be between the minimum energy and the maximum energy.")
                        self.widget_message1.setVisible(True)
                except:
                    self.label_message1.setText("Invalid inputs for the energy range.")
                    self.widget_message1.setVisible(True)
            else:
                self.label_message1.setText("The energy range has not been provided.")
                self.widget_message1.setVisible(True)

    def findClusters(self):
        self.toolButton_saveClusters.setVisible(False)
        self.label_save2.setText("")
        self.widget_message2.setVisible(False)
        self.images = []
        self.currentImage2 = None
        maxClusters = self.spinBox_maxClusters.value()
        text = self.comboBox_clusteringMethods.currentText()
        if text == "Clustering by the Intensities of an Element and the Pixel Locations":
            threshold = self.doubleSpinBox_thresholdClusters1.value()
            element = self.comboBox_elementClusters1.currentText()
            object = self.elementBook.getObjectType(element)
            locations, values = object.prepareDataForClustering(threshold)
            self.elementBook.clusteringByPixelLocations_OneElement(object, locations, values, threshold, maxClusters)
            if self.elementBook.getText() == None:
                string = self.elementBook.getString()
                self.images.append(self.tempDir + "/Locations_ElbowMethod_" + string + ".png")
                self.images.append(self.tempDir + "/Locations_SilhouetteCoefs_" + string + ".png")
                self.images.append(self.tempDir + "/Locations_Clusters_" + string + ".png")
            else:
                self.label_message2.setText(self.elementBook.getText())
                self.widget_message2.setVisible(True)
            self.displayImage()
        elif text == "Clustering With a Pair of Elements by Their Intensities":
            element1 = self.comboBox_element1Clusters2.currentText()
            element2 = self.comboBox_element2Clusters2.currentText()
            object1 = self.elementBook.getObjectType(element1)
            if element1 != element2:
                object2 = self.elementBook.getObjectType(element2)
            else:
                object2 = object1
            self.elementBook.clusteringByIntensities_OneElementPair(object1, object2, maxClusters)
            if self.elementBook.getText() == None:
                string = self.elementBook.getString()
                self.images.append(self.tempDir + "/Intensities_ElbowMethod_" + string + ".png")
                self.images.append(self.tempDir + "/Intensities_SilhouetteCoefs_" + string + ".png")
                self.images.append(self.tempDir + "/Intensities_Clusters_scatter_" + string + ".png")
                self.images.append(self.tempDir + "/Intensities_Clusters_pcolor_" + string + ".png")
            else:
                self.label_message2.setText(self.elementBook.getText())
                self.widget_message2.setVisible(True)
            self.displayImage()
        else:
            elements = self.checkableComboBox.checkedItems()
            if len(elements) != 0:
                indices = []
                for e in elements:
                    indices.append(self.elementBook.getElementIndex(e))
                self.elementBook.findClustersBySumIntensities(indices, maxClusters,self.checkBox_normalize.isChecked())
                if self.elementBook.getText() == None:
                    string = self.elementBook.getString()
                    self.images.append(self.tempDir + "/SumIntensities_ElbowMethod_" + string + ".png")
                    self.images.append(self.tempDir + "/SumIntensities_SilhouetteCoefs_" + string + ".png")
                    self.images.append(self.tempDir + "/SumIntensities_Clusters_scatter_" + string + ".png")
                    self.images.append(self.tempDir + "/SumIntensities_Clusters_pcolor_" + string + ".png")
                else:
                    self.label_message2.setText(self.elementBook.getText())
                    self.widget_message2.setVisible(True)
            else:
                self.label_message2.setText("None of the elements has been selected.")
                self.widget_message2.setVisible(True)
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
# sizePolicy.setHorizontalStretch(0)
# sizePolicy.setVerticalStretch(0)
# sizePolicy.setHeightForWidth(self.checkableComboBox.sizePolicy().hasHeightForWidth())
# self.checkableComboBox.setSizePolicy(sizePolicy)
# self.checkableComboBox.setMaximumSize(QtCore.QSize(75, 16777215))
# self.checkableComboBox.setObjectName("checkableComboBox")
# self.horizontalLayout_15.addWidget(self.checkableComboBox)
