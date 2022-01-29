## Get the list of file names
def getEdfFileNames(directory):
    import os
    arr = os.listdir(directory)
    i = len(arr)-1
    while i >= 0:
        if arr[i][-4:] != ".edf":
            arr.remove(arr[i])
        i -= 1
    arr.sort()
    return arr

## Get the list of columns
def getColumns(arr):
    listsOfNumbers = []
    for s in arr:
        newstr = ''.join((ch if ch in '0123456789' else ' ') for ch in s)
        listsOfNumbers.append([int(i) for i in newstr.split()])
    cols = []
    if len(listsOfNumbers[0]) > 1:
        numbers = []
        for n in listsOfNumbers[0]:
            numbers.append([n,1])
        for i in range(1, 10):
            for j in range(0, len(numbers)):
                if listsOfNumbers[i][j] == numbers[j][0]: # compare numbers of the same index
                    numbers[j][1] += 1
        for j in range(0, len(numbers)):
            if numbers[j][1] < 10:
                for n in listsOfNumbers:
                    cols.append(int(n[j]))
    elif len(listsOfNumbers[0]) == 1:
        for n in listsOfNumbers:
            cols.append(int(n[0]))
    return cols

## Find missing files
def findMissing(cols, arr):
    missingCols = set(range(min(cols), max(cols))) - set(cols) # list of indices missing
    missingFiles = []
    if len(missingCols) == 1:
        index = str(cols[-1])
        head = arr[-1].split(index)[0]
        tail = arr[-1].split(index)[1]
        missingFiles.append(head + str(missingCols[0]) + tail)
        print("One .edf file is missing.")
        print("Missing file: ", missingFiles[0])
    elif len(missingCols) > 1:
        index = str(cols[-1])
        head = arr[-1].split(index)[0]
        tail = arr[-1].split(index)[1]
        for m in missingCols:
            missingFiles.append(head + str(m) + tail)
        print(len(missingCols)," .edf files are missing.")
        print("List of missing files: ", missingFiles)
    return missingCols, missingFiles

## Create a folder in the current directory to save plots
def createFolder(directory):
    import os
    name = directory.split("/")[-1]
    currentDirectory = os.getcwd()
    if not os.path.exists(name):
        os.mkdir(os.path.join(currentDirectory, name))
    return currentDirectory + "/" + name

## Save a variable
def saveVar(var,fileName):
    import pickle
    f = open(fileName, 'wb')
    pickle.dump(var, f)
    f.close()

## Get a saved variable
def getVar(fileName):
    import pickle
    f = open(fileName, 'rb')
    var = pickle.load(f)
    f.close()
    return var

def getDirectory():
    answer2 = input("Browse for a source directory that contains .edf files or type a path to it? (Browse/Type) ")
    strings = answer2.lower().split(" ")
    while (strings[0] != "browse" and strings[0] != "type") or len(strings) != 1:
        print("Invalid answer.")
        answer2 = input("Browse for a source directory that contains .edf files or type a path to it? (Browse/Type) ")
        strings = answer2.lower().split(" ")
    if answer2.lower().split(" ")[0] == "browse":
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(None, "Select a Directory", options=QFileDialog.ShowDirsOnly)
    else:
        directory = input("Enter a path to the source directory: ")
    import os
    while len(directory) == 0 or os.path.isdir(directory) == False:
        print("The path entered is invalid.")
        answer1 = input("Continue or quit? ")
        strings = answer1.lower().split(" ")
        while (strings[0] != "continue" and strings[0] != "quit") or len(strings) != 1:
            print("Invalid answer.")
            answer1 = input("Continue or quit? ")
            strings = answer1.lower().split(" ")
        if answer1.lower().split(" ")[0] == "continue":
            directory, pixels = getDirectory()
            arr = getEdfFileNames(directory)
            while len(arr) == 0:
                print("There is no .edf file in the selected source directory.")
                answer1 = input("Continue or quit? ")
                while answer1.lower().split(" ")[0] != "continue" and answer1.lower().split(" ")[0] != "quit":
                    print("Invalid answer.")
                    answer1 = input("Continue or quit? ")
                if answer1.lower().split(" ")[0] == "continue":
                    directory, pixels = getDirectory()
                    arr = getEdfFileNames(directory)
                else:
                    return None, None
            cols = getColumns(arr)
            l = zip(arr, cols)
            l.sort(key=lambda x: x[1])
            arr = [f for f, c in l]
            from PyMca5.PyMcaIO.EdfFile import EdfFile
            edf = EdfFile(directory + "/" + arr[0], "r")
            nRow = len(edf.GetData(0))
            nCol = len(cols)
            length = len(edf.GetData(0)[0])
            bool = False
            pixels = [[None for j in range(nCol)] for i in range(nRow)]
            from Pixel import Pixel
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
                                    (float(item) >= 0) for item in edf.GetData(0)[i]):
                                pixels[i][j] = Pixel(edf.GetData(0)[i])
                            else:
                                bool = True
                                break
                    except:
                        bool = True
                    if bool == True:
                        break
            if bool == False:
                return directory, pixels
            else:
                print("One or more .edf files have the name or data not in the correct format.")
                answer1 = input("Continue or quit? ")
                while answer1.lower().split(" ")[0] != "continue" and answer1.lower().split(" ")[0] != "quit":
                    print("Invalid answer.")
                    answer1 = input("Continue or quit? ")
                if answer1.lower().split(" ")[0] == "continue":
                    directory, pixels = getDirectory()
                else:
                    return None, None
        else:
            return None, None

def getPcklFile():
    answer2 = input("Browse for a .pckl file that stores a variable of class ElementBook or type a path to it? (Browse/Type) ")
    strings = answer2.lower().split(" ")
    while (strings[0] != "browse" and strings[0] != "type") or len(strings) != 1:
        print("Invalid answer.")
        answer2 = input("Browse for a .pckl file that stores a variable of class ElementBook or type a path to it? (Browse/Type) ")
        strings = answer2.lower().split(" ")
    if answer2.lower().split(" ")[0] == "browse":
        from PyQt5.QtWidgets import QFileDialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(None, "Select a Pickle File", "", "Pickle Files (*.pckl)", options=options)
    else:
        path = input("Enter a path to the .pckl file: ")
    import os
    while len(path) == 0 or os.path.isfile(path) == False or (len(path) >= 5 and path[-5:] != ".pckl"):
        print("The path provided is invalid.")
        answer1 = input("Continue or quit? ")
        strings = answer1.lower().split(" ")
        while (strings[0] != "continue" and strings[0] != "quit") or len(strings) != 1:
            print("Invalid answer.")
            answer1 = input("Continue or quit? ")
            strings = answer1.lower().split(" ")
        if answer1.lower().split(" ")[0] == "continue":
            path = getPcklFile()
            try:
                elementBook = getVar(path)
                from Scan import Scan
                import os
                temp1 = Scan(os.getcwd(), 2, 2, -1, -1)
                from ElementBook import ElementBook
                temp2 = ElementBook(temp1)
                while elementBook is not temp2:
                    print("This .pckl file does not store a variable of the desired type.")
                    answer3 = input("Continue or quit? ")
                    while answer3.lower().split(" ")[0] != "continue" and answer3.lower().split(" ")[0] != "quit":
                        print("Invalid answer.")
                        answer3 = input("Continue or quit? ")
                    if answer3.lower().split(" ")[0] == "continue":
                        path = getPcklFile()
                        elementBook = getVar(path)
                    else:
                        return None
                return path
            except ImportError:
                print("This .pckl file contains more than one variable or does not store a variable of the desired type.")
                answer3 = input("Continue or quit? ")
                while answer3.lower().split(" ")[0] != "continue" and answer3.lower().split(" ")[0] != "quit":
                    print("Invalid answer.")
                    answer3 = input("Continue or quit? ")
                if answer3.lower().split(" ")[0] == "continue":
                    path = getPcklFile()
                else:
                    return None
        else:
            return None

def useDirectory():
    directory,pixels = getDirectory()
    if directory != None:
        print("Please provide the information on the energy range in which the data was recorded. The energies in the "
              "range must be non-negative and written in eV, and the maximum energy must be higher than the minimum "
              "energy. Please enter -1 for both the minimum energy and the maximum energy if the energy range is unknown "
              "- the program will set a temporary energy range with the lower bound of 0eV and the step of 1eV.")
        minEnergy = input("Enter the minimum energy: ")
        maxEnergy = input("Enter the maximum energy: ")
        bool = False
        skip = "No"
        while bool == False and skip.lower().split(" ")[0] != "yes":
            minEnergy.replace(" ","")
            maxEnergy.replace(" ","")
            try:
                minEnergy = float(minEnergy)
                maxEnergy = float(maxEnergy)
                if minEnergy < maxEnergy and minEnergy >= 0:
                    bool = True
                elif minEnergy == -1 and maxEnergy == -1:
                    print("The program has set a temporary energy range with the lower bound of 0eV and the step of 1eV.")
                else:
                    print("Invalid input(s).")
                    skip = input("Skip inserting the energy range? (Yes/No) ")
                    while skip.lower().split(" ")[0] != "no" and skip.lower().split(" ")[0] != "yes":
                        print("Invalid input.")
                        skip = input("Skip inserting the energy range? (Yes/No) ")
                    if skip.lower().split(" ")[0] == "no":
                        minEnergy = input("Enter the minimum energy: ")
                        maxEnergy = input("Enter the maximum energy: ")
                    elif skip.lower().split(" ")[0] == "yes":
                        minEnergy = -1
                        maxEnergy = -1
                        print("The program has set a temporary energy range with the lower bound of 0eV and the step of 1eV.")
            except:
                print("Invalid input(s).")
                skip = input("Skip inserting the energy range? (Yes/No) ")
                while skip.lower().split(" ")[0] != "no" and skip.lower().split(" ")[0] != "yes":
                    print("Invalid input.")
                    skip = input("Skip inserting the energy range? (Yes/No) ")
                if skip.lower().split(" ")[0] == "no":
                    minEnergy = input("Enter the minimum energy: ")
                    maxEnergy = input("Enter the maximum energy: ")
                elif skip.lower().split(" ")[0] == "yes":
                    minEnergy = -1
                    maxEnergy = -1
                    print("The program has set a temporary energy range with the lower bound of 0eV and the step of 1eV.")
        print("Please provide a threshold value for reducing noises in the X-Ray signals. The threshold value must be a "
              "non-negative number and in the unit of the intensities. All the intensities in this dataset which are "
              "lower than the threshold value will be set to zero.")
        threshold1 = input("Enter a threshold value: ")
        bool = False
        while bool == False:
            threshold1.replace(" ","")
            try:
                threshold1 = float(threshold1)
                if threshold1 >= 0:
                    bool = True
                else:
                    print("Invalid input.")
                    threshold1 = input("Enter a threshold value: ")
            except:
                print("Invalid input.")
                threshold1 = input("Enter a threshold value: ")
        path = createFolder(directory)
        from Scan import Scan
        scan = Scan(path, len(pixels), len(pixels[0]), minEnergy, maxEnergy)
        for j in range(0, len(pixels[0])):
            for i in range(0, len(pixels)):
                scan.insertPixel(pixels[i][j], i, j, threshold1)
        from ElementBook import ElementBook
        elementBook = ElementBook(scan)
        fileName = path + "/elementBook.pckl"
        saveVar(elementBook, fileName)
        print("Data read successfully.")
        selectAction(elementBook)

def usePcklFile():
    path = getPcklFile()
    if path != None:
        elementBook = getVar(path)
        print("Data read successfully.")
        import distutils.dir_util
        distutils.dir_util.mkpath(elementBook.getScan().getPath())
        selectAction(elementBook)

def getAnElementIndex(elementBook):
    string = input("Enter an element name (e.g. Na): ")
    s = string.split(" ")
    if len(s) == 1:
        index = elementBook.getElementIndex(s[0])
        if index != -1:
            return index
        else:
            answer = input("Reenter the input or quit? (Reenter/Quit) ")
            strings = answer.lower().split(" ")
            while (strings[0] != "reenter" and strings[0] != "quit") or len(strings) != 1:
                print("Invalid answer.")
                answer = input("Reenter the input or quit? (Reenter/Quit) ")
                strings = answer.lower().split(" ")
            if answer.lower().split(" ")[0] == "reenter":
                return getAnElementIndex(elementBook)
            else:
                return -1
    else:
        print("Invalid input.")
        answer = input("Reenter the input or quit? (Reenter/Quit) ")
        strings = answer.lower().split(" ")
        while (strings[0] != "reenter" and strings[0] != "quit") or len(strings) != 1:
            print("Invalid answer.")
            answer = input("Reenter the input or quit? (Reenter/Quit) ")
            strings = answer.lower().split(" ")
        if answer.lower().split(" ")[0] == "reenter":
            return getAnElementIndex(elementBook)
        else:
            return -1

def getElementIndices(elementBook,bool): # If bool == True, return a list of 2 indices.
    string = input("Enter the element names: ")
    substrings = string.split(",")
    if len(substrings[-1].split(" ")) == 0:
        del substrings[-1]
    indices = []
    for item in substrings:
        s = item.split(" ")
        if len(s) == 1:
            index = elementBook.getElementIndex(s[0])
            if index != -1:
                indices.append(index)
            else:
                answer = input("Reenter the input or quit? (Reenter/Quit) ")
                strings = answer.lower().split(" ")
                while (strings[0] != "reenter" and strings[0] != "quit") or len(strings) != 1:
                    print("Invalid answer.")
                    answer = input("Reenter the input or quit? (Reenter/Quit) ")
                    strings = answer.lower().split(" ")
                if answer.lower().split(" ")[0] == "reenter":
                    return getElementIndices(elementBook)
                else:
                    return None
        else:
            print("Invalid input.")
            answer = input("Reenter the input or quit? (Reenter/Quit) ")
            strings = answer.lower().split(" ")
            while (strings[0] != "reenter" and strings[0] != "quit") or len(strings) != 1:
                print("Invalid answer.")
                answer = input("Reenter the input or quit? (Reenter/Quit) ")
                strings = answer.lower().split(" ")
            if answer.lower().split(" ")[0] == "reenter":
                return getElementIndices(elementBook)
            else:
                return None
    if len(indices) == 0:
        print("None of the elements has been selected.")
        answer = input("Reenter the input or quit? (Reenter/Quit) ")
        strings = answer.lower().split(" ")
        while (strings[0] != "reenter" and strings[0] != "quit") or len(strings) != 1:
            print("Invalid answer.")
            answer = input("Reenter the input or quit? (Reenter/Quit) ")
            strings = answer.lower().split(" ")
        if answer.lower().split(" ")[0] == "reenter":
            return getElementIndices(elementBook)
        else:
            return None
    elif len(indices) != 2 and bool == True:
        print("The number of elements must be 2.")
        answer = input("Reenter the input or quit? (Reenter/Quit) ")
        strings = answer.lower().split(" ")
        while (strings[0] != "reenter" and strings[0] != "quit") or len(strings) != 1:
            print("Invalid answer.")
            answer = input("Reenter the input or quit? (Reenter/Quit) ")
            strings = answer.lower().split(" ")
        if answer.lower().split(" ")[0] == "reenter":
            return getElementIndices(elementBook)
        else:
            return None
    return indices

def selectAction(elementBook):
    answer1 = input("Enter 1 to plot data, 2 to find clusters, or 3 to quit the program: ")
    strings = answer1.lower().split(" ")
    while (strings[0] != "1" and strings[0] != "2" and strings[0] != "3") or len(strings) != 1:
        print("Invalid input.")
        answer1 = input("Enter 1 to plot data, 2 to find clusters, or 3 to quit the program: ")
        strings = answer1.lower().split(" ")
    if answer1.lower().split(" ")[0] == "1":
        print("There are three plotting modes. Mode 1 plots the total intensities in the energy range of an element at "
              "all pixels. Mode 2 plots the intensities at an energy at all pixels. Mode 3 plots the total intensities "
              "in a customized energy range at all pixels.")
        answer2 = input("Enter 1 to select Mode 1, 2 to select Mode 2, or 3 to select Mode 3: ")
        strings = answer2.lower().split(" ")
        while (strings[0] != "1" and strings[0] != "2" and strings[0] != "3") or len(strings) != 1:
            print("Invalid input.")
            answer2 = input("Enter 1 to select Mode 1, 2 to select Mode 2, or 3 to select Mode 3: ")
            strings = answer2.lower().split(" ")
        if answer2.lower().split(" ")[0] == "1":
            answer3 = input("Plot the data of all elements in the dataset? (Yes/No) ")
            strings = answer3.lower().split(" ")
            while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
                print("Invalid answer.")
                answer3 = input("Plot the data of all elements in the dataset? (Yes/No) ")
                strings = answer3.lower().split(" ")
            if answer3.lower().split(" ")[0] == "yes":
                elementBook.plotTotalIntensities_AllElements()
                count = elementBook.getCount()
                if count == 1:
                    print("One plot is successfully saved in " + elementBook.getScan().getPath() + ".")
                elif count > 1:
                    print("Plots are successfully saved in " + elementBook.getScan().getPath() + ".")
            else:
                index = getAnElementIndex(elementBook)
                if index != -1:
                    elementBook.plotTotalIntensitiesByIndex(index)
                    if elementBook.getText() == None:
                        print("The plot is successfully saved in " + elementBook.getScan().getPath() + ".")
            selectAction(elementBook)
        elif answer2.lower().split(" ")[0] == "2":
            print("In this mode, users need to provide the energy at which the intensities detected at all the pixels "
                  "will be collected to create a plot. The energy must be in eV and between the minimum energy and the "
                  "maximum energy.")
            energy = input("Enter an energy: ")
            bool = False
            scan = elementBook.getScan()
            while bool == False:
                energy.replace(" ", "")
                try:
                    energy = float(energy)
                    if energy >= scan.getMinEnergy() and energy <= scan.getMaxEnergy():
                        bool = True
                    else:
                        print("Invalid input.")
                        energy = input("Enter an energy: ")
                except:
                    print("Invalid input.")
                    energy = input("Enter an energy: ")
            scan.plotIntensitiesAtEnergy(energy)
            print("The plot is successfully saved in " + scan.getPath() + ".")
            selectAction(elementBook)
        else:
            print("In this mode, users will be asked to provide an energy range in which the total intensities at all "
                  "the pixels will be computed and used to create a plot. The energy range must be in eV and between the "
                  "minimum energy and the maximum energy, and the end energy must be higher than the start energy.")
            startEnergy = input("Enter the start energy: ")
            endEnergy = input("Enter the end energy: ")
            bool = False
            scan = elementBook.getScan()
            while bool == False:
                startEnergy.replace(" ", "")
                endEnergy.replace(" ", "")
                try:
                    startEnergy = float(startEnergy)
                    endEnergy = float(endEnergy)
                    if startEnergy >= scan.getMinEnergy() and endEnergy <= scan.getMaxEnergy() and startEnergy < endEnergy:
                        bool = True
                    else:
                        print("Invalid input(s).")
                        startEnergy = input("Enter the start energy: ")
                        endEnergy = input("Enter the end energy: ")
                except:
                    print("Invalid input(s).")
                    startEnergy = input("Enter the start energy: ")
                    endEnergy = input("Enter the end energy: ")
            scan.plotTotalIntensitiesInEnergyRange(startEnergy,endEnergy)
            print("The plot is successfully saved in " + scan.getPath() + ".")
            selectAction(elementBook)
    elif answer1.lower().split(" ")[0] == "2":
        print("There are three clustering methods. Method 1 is to find clusters by intensities of one single element at "
              "all pixels and the pixel locations. Method 2 is to find clusters with a pair of elements by their "
              "intensities at all pixels. Method 3 is to find clusters by the sum of intensities of elements in a set at "
              "all pixels.")
        answer2 = input("Enter 1 to select Method 1, 2 to select Method 2, or 3 to select Method 3: ")
        strings = answer2.lower().split(" ")
        while (strings[0] != "1" and strings[0] != "2" and strings[0] != "3") or len(strings) != 1:
            print("Invalid input.")
            answer2 = input("Enter 1 to select Method 1, 2 to select Method 2, or 3 to select Method 3: ")
            strings = answer2.lower().split(" ")
        if answer2.lower().split(" ")[0] == "1":
            answer3 = input("Find clusters using the data of all elements in the dataset? (Yes/No) ")
            strings = answer3.lower().split(" ")
            while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
                print("Invalid answer.")
                answer3 = input("Find clusters using the data of all elements in the dataset? (Yes/No) ")
                strings = answer3.lower().split(" ")
            if answer3.lower().split(" ")[0] == "yes":
                print("Please provide a threshold value in percent for data cleaning. After normalizing the intensities "
                      "of an element to the range between 0 and 100, all the intensities which are lower than the "
                      "threshold value will be set to zero. Note that the threshold value must be between 0 and 100.")
                threshold2 = input("Enter a threshold value: ")
                bool = False
                while bool == False:
                    threshold2.replace(" ", "")
                    try:
                        threshold2 = float(threshold2)
                        if threshold2 >= 0 and threshold2 <= 100:
                            bool = True
                        else:
                            print("Invalid input.")
                            threshold2 = input("Enter a threshold value: ")
                    except:
                        print("Invalid input.")
                        threshold2 = input("Enter a threshold value: ")
                print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 2 since all the pixels with intensities of zero form one cluster.")
                maxClusters = input("Enter the maximum number of clusters: ")
                bool = False
                while bool == False:
                    maxClusters.replace(" ", "")
                    try:
                        maxClusters = int(maxClusters)
                        if maxClusters > 2:
                            bool = True
                        else:
                            print("Invalid input.")
                            maxClusters = input("Enter the maximum number of clusters: ")
                    except:
                        print("Invalid input.")
                        maxClusters = input("Enter the maximum number of clusters: ")
                elementBook.findClustersByPixelLocations_AllElements(threshold2, maxClusters)
                if elementBook.getCount() > 0:
                    print("Plots are successfully saved in " + elementBook.getScan().getPath() + ".")
            else:
                index = getAnElementIndex(elementBook)
                if index != -1:
                    print("Please provide a threshold value in percent for data cleaning. After normalizing the "
                          "intensities of an element to the range between 0 and 100, all the intensities which are lower "
                          "than the threshold value will be set to zero. Note that the threshold value must be between 0 "
                          "and 100.")
                    threshold2 = input("Enter a threshold value: ")
                    bool = False
                    while bool == False:
                        threshold2.replace(" ", "")
                        try:
                            threshold2 = float(threshold2)
                            if threshold2 >= 0 and threshold2 <= 100:
                                bool = True
                            else:
                                print("Invalid input.")
                                threshold2 = input("Enter a threshold value: ")
                        except:
                            print("Invalid input.")
                            threshold2 = input("Enter a threshold value: ")
                    print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 2 since all the pixels with intensities of zero form one cluster.")
                    maxClusters = input("Enter the maximum number of clusters: ")
                    bool = False
                    while bool == False:
                        maxClusters.replace(" ", "")
                        try:
                            maxClusters = int(maxClusters)
                            if maxClusters > 2:
                                bool = True
                            else:
                                print("Invalid input.")
                                maxClusters = input("Enter the maximum number of clusters: ")
                        except:
                            print("Invalid input.")
                            maxClusters = input("Enter the maximum number of clusters: ")
                    object = elementBook.getDF().at[index, 'Object_Type']
                    locations, values = object.prepareDataForClustering(threshold2)
                    elementBook.clusteringByPixelLocations_OneElement(object, locations, values, threshold2, maxClusters)
                    if elementBook.getText() == None:
                        print("Plots are successfully saved in " + elementBook.getScan().getPath() + ".")
            selectAction(elementBook)
        elif answer2.lower().split(" ")[0] == "2":
            answer3 = input("Find clusters using the data of all element pairs in the dataset? (Yes/No) ")
            strings = answer3.lower().split(" ")
            while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
                print("Invalid answer.")
                answer3 = input("Find clusters using the data of all element pairs in the dataset? (Yes/No) ")
                strings = answer3.lower().split(" ")
            if answer3.lower().split(" ")[0] == "yes":
                print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 1.")
                maxClusters = input("Enter the maximum number of clusters: ")
                bool = False
                while bool == False:
                    maxClusters.replace(" ", "")
                    try:
                        maxClusters = int(maxClusters)
                        if maxClusters > 1:
                            bool = True
                        else:
                            print("Invalid input.")
                            maxClusters = input("Enter the maximum number of clusters: ")
                    except:
                        print("Invalid input.")
                        maxClusters = input("Enter the maximum number of clusters: ")
                elementBook.findClustersByIntensities_AllElementPairs(maxClusters)
                if elementBook.getCount() > 0:
                    print("Plots are successfully saved in " + elementBook.getScan().getPath() + ".")
            else:
                print("Please provide a set of two elements. Note that the elements must be separated by a comma (e.g. "
                      "Na, Br).")
                indices = getElementIndices(elementBook,True)
                if indices != None and len(indices) == 2:
                    element1 = elementBook.getDF().at[min(indices), 'Object_Type']
                    element2 = elementBook.getDF().at[max(indices), 'Object_Type']
                    print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 1.")
                    maxClusters = input("Enter the maximum number of clusters: ")
                    bool = False
                    while bool == False:
                        maxClusters.replace(" ", "")
                        try:
                            maxClusters = int(maxClusters)
                            if maxClusters > 1:
                                bool = True
                            else:
                                print("Invalid input.")
                                maxClusters = input("Enter the maximum number of clusters: ")
                        except:
                            print("Invalid input.")
                            maxClusters = input("Enter the maximum number of clusters: ")
                    elementBook.clusteringByIntensities_OneElementPair(element1, element2, maxClusters)
                    if elementBook.getText() == None:
                        print("Plots are successfully saved in " + elementBook.getScan().getPath() + ".")
            selectAction(elementBook)
        else:
            print("Please provide a set of element names. Note that two consecutive elements must be separated by a "
                  "comma (e.g. Na, Br, K).")
            indices = getElementIndices(elementBook, False)
            if indices != None:
                print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 1.")
                maxClusters = input("Enter the maximum number of clusters: ")
                bool = False
                while bool == False:
                    maxClusters.replace(" ", "")
                    try:
                        maxClusters = int(maxClusters)
                        if maxClusters > 1:
                            bool = True
                        else:
                            print("Invalid input.")
                            maxClusters = input("Enter the maximum number of clusters: ")
                    except:
                        print("Invalid input.")
                        maxClusters = input("Enter the maximum number of clusters: ")
                answer3 = input("Normalize the intensities of each element before finding clusters? (Yes/No) ")
                strings = answer3.lower().split(" ")
                while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
                    print("Invalid answer.")
                    answer3 = input("Normalize the intensities of each element before finding clusters? (Yes/No) ")
                    strings = answer3.lower().split(" ")
                if answer3.lower().split(" ")[0] == "yes":
                    elementBook.findClustersBySumIntensities(indices, maxClusters, True)
                else:
                    elementBook.findClustersBySumIntensities(indices, maxClusters, False)
                if elementBook.getText() == None:
                    print("Plots are successfully saved in " + elementBook.getScan().getPath() + ".")
            selectAction(elementBook)
