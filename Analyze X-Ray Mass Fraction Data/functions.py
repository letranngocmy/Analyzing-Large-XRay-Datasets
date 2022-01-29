## Get the list of file names
def getTxtFileNames(directory):
    import os
    arr = os.listdir(directory)
    i = len(arr) - 1
    while i >= 0:
        if arr[i][-4:] != ".txt":
            arr.remove(arr[i])
        i -= 1
    arr.sort()
    return arr

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

## Create a folder in the current directory to save plots
def createFolder(directory):
    import os
    name = directory.split("/")[-1]
    currentDirectory = os.getcwd()
    if not os.path.exists(name):
        os.mkdir(os.path.join(currentDirectory, name))
    return currentDirectory + "/" + name

def getDirectory():
    answer2 = input("Browse for a source directory that contains .txt files or type a path to it? (Browse/Type) ")
    strings = answer2.lower().split(" ")
    while (strings[0] != "browse" and strings[0] != "type") or len(strings) != 1:
        print("Invalid answer.")
        answer2 = input("Browse for a source directory that contains .txt files or type a path to it? (Browse/Type) ")
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
            directory, elements = getDirectory()
            arr = getTxtFileNames(directory)
            while len(arr) == 0:
                print("There is no .txt file in the selected source directory.")
                answer1 = input("Continue or quit? ")
                while answer1.lower().split(" ")[0] != "continue" and answer1.lower().split(" ")[0] != "quit":
                    print("Invalid answer.")
                    answer1 = input("Continue or quit? ")
                if answer1.lower().split(" ")[0] == "continue":
                    directory,elements = getDirectory()
                    arr = getTxtFileNames(directory)
                else:
                    return None, None
            bool = False
            elements = []
            from Element import Element
            for f in arr:
                element = Element(f, directory)
                if element.getElementName() != None:
                    if len(elements) == 0:
                        nRow = element.getNRow()
                        nCol = element.getNCol()
                        elements.append(element)
                    else:
                        if nRow != element.getNRow() or nCol != element.getNCol():
                            bool = True
                            break
                        else:
                            elements.append(element)
                else:
                    bool = True
                    break
            if bool == False:
                return directory,elements
            else:
                print("One or more .txt files have the name or data not in the correct format.")
                answer1 = input("Continue or quit? ")
                while answer1.lower().split(" ")[0] != "continue" and answer1.lower().split(" ")[0] != "quit":
                    print("Invalid answer.")
                    answer1 = input("Continue or quit? ")
                if answer1.lower().split(" ")[0] == "continue":
                    directory, elements = getDirectory()
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
        path, _ = QFileDialog.getOpenFileName(None, "Select a Pickle File", "", "Pickle Files (*.pckl)",options=options)
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
                from ElementBook import ElementBook
                import os
                temp = ElementBook(os.getcwd())
                while elementBook is not temp:
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
    directory,elements = getDirectory()
    if directory != None:
        print("Please provide a threshold value for reducing noises in the data. The threshold value must be a "
              "non-negative number and in the unit of the concentrations. All the concentrations in this dataset which "
              "are lower than the threshold value will be set to zero.")
        threshold1 = input("Enter a threshold value: ")
        bool = False
        while bool == False:
            threshold1.replace(" ", "")
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
        from ElementBook import ElementBook
        elementBook = ElementBook(path)
        from Element import Element
        for element in elements:
            elementBook.insertElement(element, threshold1)
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
        distutils.dir_util.mkpath(elementBook.getPath())
        selectAction(elementBook)

def getAnElementIndex(elementBook):
    string = input("Enter an element name and the corresponding emission line: ")
    s = string.split(" ")
    if len(s) == 2:
        index = elementBook.getIndex(s[0],s[1])
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

def getElementIndices(elementBook):
    string = input("Enter the element names and the corresponding emission lines: ")
    substrings = string.split(",")
    if len(substrings[-1].split(" ")) == 0:
        del substrings[-1]
    indices = []
    for item in substrings:
        s = item.split(" ")
        if len(s) == 2:
            index = elementBook.getIndex(s[0], s[1])
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
        answer2 = input("Plot the data of all elements in the dataset? (Yes/No) ")
        strings = answer2.lower().split(" ")
        while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
            print("Invalid answer.")
            answer2 = input("Plot the data of all elements in the dataset? (Yes/No) ")
            strings = answer2.lower().split(" ")
        if answer2.lower().split(" ")[0] == "yes":
            elementBook.plotAllElementsConcentrations()
            count = elementBook.getCount()
            if count == 1:
                print("One plot is successfully saved in " + elementBook.getPath() + ".")
            elif count > 1:
                print("Plots are successfully saved in " + elementBook.getPath() + ".")
        else:
            print("Please provide an element name and the corresponding emission line in format E[space]L, where E "
                  "denotes the element name and L denotes the emission line (e.g. Na K).")
            index = getAnElementIndex(elementBook)
            if index != -1:
                elementBook.plotConcentrationsByElementIndex(index)
                if elementBook.getText() == None:
                    print("The plot is successfully saved in " + elementBook.getPath() + ".")
        selectAction(elementBook)
    elif answer1.lower().split(" ")[0] == "2":
        print("There are three clustering methods. Method 1 is to find clusters by concentrations of one single element "
              "at all pixels and the pixel locations. Method 2 is to find clusters with a pair of elements by their "
              "concentrations at all pixels. Method 3 is to find clusters by the sum of concentrations of elements in a "
              "set at all pixels.")
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
                print("Please provide a threshold value in percent for data cleaning. After normalizing the "
                      "concentrations of an element to the range between 0 and 100, all the concentrations which are "
                      "lower than the threshold value will be set to zero. Note that the threshold value must be between "
                      "0 and 100.")
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
                print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 2 since all the pixels with concentrations of zero form one cluster.")
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
                    print("Plots are successfully saved in " + elementBook.getPath() + ".")
            else:
                print("Please provide an element name and the corresponding emission line in format E[space]L, where E "
                      "denotes the element name and L denotes the emission line (e.g. Na K).")
                index = getAnElementIndex(elementBook)
                if index != -1:
                    print("Please provide a threshold value in percent for data cleaning. After normalizing the "
                          "concentrations of an element to the range between 0 and 100, all the concentrations which are "
                          "lower than the threshold value will be set to zero. Note that the threshold value must be between "
                          "0 and 100.")
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
                    print("Please provide the maximum number of clusters. The maximum number of clusters must be an integer higher than 2 since all the pixels with concentrations of zero form one cluster.")
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
                    object = elementBook.getElements()[index]
                    locations, values = object.prepareDataForClustering(threshold2)
                    elementBook.clusteringByPixelLocations_OneElement(object, locations, values, threshold2, maxClusters)
                    if elementBook.getText() == None:
                        print("Plots are successfully saved in " + elementBook.getPath() + ".")
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
                    maxClusters.replace(" ","")
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
                elementBook.findClustersByConcentrations_AllElementPairs(maxClusters)
                if elementBook.getCount() > 0:
                    print("Plots are successfully saved in " + elementBook.getPath() + ".")
            else:
                print("Please provide a set of two element names and the corresponding emission lines. A pair of an "
                      "element name and an emission line must be written in format E[space]L, where E denotes the "
                      "element name and L denotes the emission line. The two pairs must be separated by a comma (e.g. Na "
                      "K, Ca L).")
                indices = getElementIndices(elementBook, True)
                if indices != None and len(indices) == 2:
                    element1 = elementBook.getElements()[min(indices)]
                    element2 = elementBook.getElements()[max(indices)]
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
                    elementBook.clusteringByConcentrations_OneElementPair(element1, element2, maxClusters)
                    if elementBook.getText() == None:
                        print("Plots are successfully saved in " + elementBook.getPath() + ".")
            selectAction(elementBook)
        else:
            print("Please provide a set of element names and the corresponding emission lines. A pair of an element name "
                  "and an emission line must be written in format E[space]L, where E denotes the element name and L "
                  "denotes the emission line, and two consecutive pairs must be separated by a comma (e.g. Na K, Ca L, "
                  "Br K).")
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
                answer3 = input("Normalize the concentrations of each element before finding clusters? (Yes/No) ")
                strings = answer3.lower().split(" ")
                while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
                    print("Invalid answer.")
                    answer3 = input("Normalize the concentrations of each element before finding clusters? (Yes/No) ")
                    strings = answer3.lower().split(" ")
                if answer3.lower().split(" ")[0] == "yes":
                    elementBook.findClustersBySumConcentrations(indices, maxClusters, True)
                else:
                    elementBook.findClustersBySumConcentrations(indices, maxClusters, False)
                if elementBook.getText() == None:
                    print("Plots are successfully saved in " + elementBook.getPath() + ".")
            selectAction(elementBook)
