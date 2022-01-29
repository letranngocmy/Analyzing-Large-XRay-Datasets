print("This program is to analyze X-Ray mass fraction data of an object of interest. Users will be asked to provide a "
      "path to a source directory or a Pickle file (.pckl) that stores the data required for the analysis.")
print("If users choose to provide a source directory, it should contain a number of .txt files, each of which gives data "
      "on the concentration of an element detected at every pixel on a scan using the energy of a particular emission "
      "line. Note that the name of every .txt file must start with E_L_, where E denotes the element (e.g. Na and S) and "
      "L denotes the emission line (e.g. K and L). All .txt files must have the same number of rows, and all the rows in "
      "these files must have the data of the same number of pixels since this program only supports analyzing one scan "
      "of one object each time. The data in the .txt files must be convertible to non-negative real numbers.")
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
        MainWindow.setWindowTitle('Analyze X-Ray Mass Fraction Data')
        MainWindow.show() # show the window and start the app
        app.exec_()
    else:
        answer3 = input("Enter 1 to work with a new set of .txt files or 2 to load old data stored in a .pckl file: ")
        strings = answer3.lower().split(" ")
        while (strings[0] != "1" and strings[0] != "2") or len(strings) != 1:
            print("Invalid input.")
            answer3 = input("Enter 1 to work with a new set of .txt files or 2 to load old data stored in a .pckl file: ")
            strings = answer3.lower().split(" ")
        import functions as ftns
        if answer3.lower().split(" ")[0] == "1":
            ftns.useDirectory()
        else:
            ftns.usePcklFile()



# ftns.useDirectory("/Users/letranngocmy/Downloads/tailings_6342_1")
# ftns.useDirectory("/Users/letranngocmy/Downloads/tailings_6340_2_3")
