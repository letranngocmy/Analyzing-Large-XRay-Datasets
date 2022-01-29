print("This program is to analyze X-Ray spectral data of an object of interest. Users will be asked to provide a path to "
      "a source directory or a Pickle file (.pckl) that stores the data required for the analysis.")
print("If users choose to provide a source directory, it should contain a number of .edf files, each of which gives the "
      "spectral data of every pixel on a column of the scan. The spectral data of every pixel is a set of intensities of "
      "signals detected in a fixed energy range (users will be asked to provide the information of the energy range), "
      "and so the elements in the set must be convertible to non-negative real numbers. Note that the set of intensities "
      "of all pixels in the scan are of the same length, and all the .edf files contain the data of the same number of "
      "pixels (i.e. the number of pixels on a column must be constant). Additionally, the name of every .edf file must "
      "give information on the column number.")
print("If users choose to provide a .pckl file, it should contain only one variable which is an object of class "
      "ElementBook (please consult the file ElementBook.py in this project for more detailed information).")

answer1 = input("Continue or Quit? ")
strings = answer1.lower().split(" ")
while (strings[0] != "continue" and strings[0] != "quit") or len(strings) != 1:
    print("Invalid answer.")
    answer1 = input("Continue or Quit? ")
    strings = answer1.lower().split(" ")
if answer1.lower().split(" ")[0] == "continue":
    answer2 = input("Open Desktop App? (Yes/No) ")
    strings = answer2.lower().split(" ")
    while (strings[0] != "yes" and strings[0] != "no") or len(strings) != 1:
        print("Invalid answer.")
        answer2 = input("Open Desktop App? (Yes/No) ")
        strings = answer2.lower().split(" ")
    if answer2.lower().split(" ")[0] == "yes":
        from myDesign import *
        import sys
        from myApp import MyApp
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = MyApp(MainWindow) # create an instance of our app
        MainWindow.setWindowTitle('Analyze X-Ray Spectral Data')
        MainWindow.show() # show the window and start the app
        app.exec_()
    else:
        answer3 = input("Enter 1 to work with a new set of .edf files or 2 to load old data stored in a .pckl file: ")
        strings = answer3.lower().split(" ")
        while (strings[0] != "1" and strings[0] != "2") or len(strings) != 1:
            print("Invalid input.")
            answer3 = input("Enter 1 to work with a new set of .edf files or 2 to load old data stored in a .pckl file: ")
            strings = answer3.lower().split(" ")
        import functions as ftns
        if answer3.lower().split(" ")[0] == "1":
            ftns.useDirectory()
        else:
            ftns.usePcklFile()



# ftns.useDirectory("/Users/letranngocmy/Downloads/XRF Data for Paint Swatches/Paint_Mockups_data/Paint_mockup_iron")
# ftns.useDirectory("/Users/letranngocmy/Downloads/XRF Data for Paint Swatches/Paint_Mockups_data/Paint_mockup_azurite")
# ftns.useDirectory("/Users/letranngocmy/Downloads/XRF Data for Paint Swatches/Paint_Mockups_data/Paint_mockup_peakoverlaps")
